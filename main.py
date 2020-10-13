import datetime
import pandas as pd
from pm4py.objects.log.importer.xes import importer as xes_importer
from pm4py.algo.discovery.inductive import algorithm as inductive_miner
from pm4py.visualization.petrinet import visualizer as pn_visualizer
from pm4py.evaluation.replay_fitness import evaluator as replay_fitness
from pm4py.evaluation.generalization import evaluator as calc_generaliz
from pm4py.evaluation.precision import evaluator as calc_precision
from pm4py.evaluation.simplicity import evaluator as calc_simplic
from pm4py.algo.conformance.alignments import algorithm as alignments
from pm4py.algo.discovery.alpha import algorithm as alpha_miner
from pm4py.algo.discovery.heuristics import algorithm as heuristics_miner
from pm4py.objects.conversion.log import converter as log_converter
from pm4py.objects.log.exporter.xes import exporter as xes_exporter
from pm4py.objects.conversion.process_tree import converter as pt_converter
from pm4py.evaluation.soundness.woflan import algorithm as woflan
from pm4py.algo.filtering.log.timestamp import timestamp_filter
from pm4py.algo.filtering.log.variants import variants_filter

def calculate_quality_metrics_sound(petrinet, start, log, log_name, algo, parameters):
    custom_print('Renderizando rede de Petri')
    
    gviz = pn_visualizer.apply(*petrinet)
    gviz.render('petrinets/'+ log_name +'-'+ algo)
    #pn_visualizer.view(gviz)

    custom_print('Calculando alignment')
    alignments_res = alignments.apply_log(log, *petrinet, parameters=parameters)

    custom_print('Calculando fitness')
    fitness = replay_fitness.evaluate(alignments_res, variant=replay_fitness.Variants.ALIGNMENT_BASED)

    custom_print('Calculando precision')
    precision = calc_precision.apply(log, *petrinet, parameters=parameters, variant=calc_precision.Variants.ALIGN_ETCONFORMANCE)

    custom_print('Calculando generalization')
    generaliz = calc_generaliz.apply(log, *petrinet, parameters=parameters)

    custom_print('Calculando simplicity')
    simplic = calc_simplic.apply(petrinet[0])

    f_score = 2 * ((fitness['averageFitness'] * precision) / (fitness['averageFitness'] + precision))
    print(log_name + ' ' + algo + ' F:', '%.10f' % fitness['averageFitness'], ' P:', '%.10f' % precision, ' FS:', '%.10f' % f_score, ' G:', '%.10f' % generaliz, ' S:', '%.10f' % simplic)

def calculate_quality_metrics_unsound(petrinet, start, log, log_name, algo, parameters):
    custom_print('Renderizando rede de Petri')
    
    gviz = pn_visualizer.apply(*petrinet)
    gviz.render('petrinets/'+ log_name +'-'+ algo)
    #pn_visualizer.view(gviz)

    custom_print('Calculando fitness')
    fitness = replay_fitness.apply(log, *petrinet, variant=replay_fitness.Variants.TOKEN_BASED)

    custom_print('Calculando precision')    
    precision = calc_precision.apply(log, *petrinet, parameters=parameters, variant=calc_precision.Variants.ETCONFORMANCE_TOKEN)
    
    custom_print('Calculando generalization')
    generaliz = calc_generaliz.apply(log, *petrinet, parameters=parameters, variant=calc_generaliz.Variants.GENERALIZATION_TOKEN)
    
    custom_print('Calculando simplicity')
    simplic = calc_simplic.apply(petrinet[0])
    
    f_score = 2 * ((fitness['log_fitness'] * precision) / (fitness['log_fitness'] + precision))
    print(log_name + ' ' + algo + ' F:', '%.10f' % fitness['log_fitness'], ' P:', '%.10f' % precision, ' FS:', '%.10f' % f_score, ' G:', '%.10f' % generaliz, ' S:', '%.10f' % simplic)


def custom_print(text):
    print(datetime.datetime.now().strftime("%H:%M:%S") +' '+ text)

def discover_process_models(log_path, log_name):
    start = datetime.datetime.now()
    run_woflan = False

    custom_print('Importando log')

    log_complete = xes_importer.apply(log_path)
    #log = timestamp_filter.filter_traces_contained(log_complete, "2011-10-01 00:00:00", "2012-10-31 23:59:59")
    log = variants_filter.filter_log_variants_percentage(log_complete, 0.9)

    custom_print('Log importado')


    #Inductive Miner    
    parameters = {inductive_miner.Variants.IM.value.Parameters.CASE_ID_KEY: 'case:concept:name', inductive_miner.Variants.IM.value.Parameters.TIMESTAMP_KEY: 'time:timestamp', woflan.Parameters.RETURN_ASAP_WHEN_NOT_SOUND: True, woflan.Parameters.PRINT_DIAGNOSTICS: False, woflan.Parameters.RETURN_DIAGNOSTICS: False}    
    variant = inductive_miner.Variants.IM

    custom_print('Iniciando Inductive Miner')
    petrinet = inductive_miner.apply(log, parameters=parameters, variant=variant)
    
    custom_print('Iniciando Woflan')

    if run_woflan == True:
        is_sound = woflan.apply(*petrinet, parameters=parameters)
    else:
        is_sound = False
    
    if is_sound == True:
        calculate_quality_metrics_sound(petrinet, start, log, log_name, 'IM (sound)', parameters)
    else:
        calculate_quality_metrics_unsound(petrinet, start, log, log_name, 'IM (unsound)', parameters)
    
    custom_print('Inductive Miner finalizado')


    #Alpha Miner
    parameters = {woflan.Parameters.RETURN_ASAP_WHEN_NOT_SOUND: True, woflan.Parameters.PRINT_DIAGNOSTICS: False, woflan.Parameters.RETURN_DIAGNOSTICS: False}
    variant = alpha_miner.Variants.ALPHA_VERSION_CLASSIC
    
    custom_print('Iniciando Alpha Miner')
    petrinet = alpha_miner.apply(log, parameters=parameters, variant=variant)
    
    custom_print('Iniciando Woflan')

    if run_woflan == True:
        is_sound = woflan.apply(*petrinet, parameters=parameters)
    else:
        is_sound = False
    
    if is_sound == True:
        calculate_quality_metrics_sound(petrinet, start, log, log_name, 'alpha (sound)', parameters)
    else:
        calculate_quality_metrics_unsound(petrinet, start, log, log_name, 'alpha (unsound)', parameters)
    
    custom_print('Alpha Miner finalizado')


    #Heuristic Miner    
    parameters = {heuristics_miner.Variants.CLASSIC.value.Parameters.DEPENDENCY_THRESH: 0.5, woflan.Parameters.RETURN_ASAP_WHEN_NOT_SOUND: True, woflan.Parameters.PRINT_DIAGNOSTICS: False, woflan.Parameters.RETURN_DIAGNOSTICS: False}
    
    custom_print('Iniciando Heuristic Miner')
    petrinet = heuristics_miner.apply(log, parameters=parameters)
    
    custom_print('Iniciando Woflan')

    if run_woflan == True:
        is_sound = woflan.apply(*petrinet, parameters=parameters)
    else:
        is_sound = False
    
    if is_sound == True:
        calculate_quality_metrics_sound(petrinet, start, log, log_name, 'HM-0.50 (sound)', parameters)
    else:
        calculate_quality_metrics_unsound(petrinet, start, log, log_name, 'HM-0.50 (unsound)', parameters)
    
    custom_print('Heuristic Miner finalizado')


#input: log in XES format
custom_print('Iniciando analises')

xes_log_path = '/home/rodrigo/python/bpi2012/logs/BPI_Challenge_2012.xes'
discover_process_models(xes_log_path, 'xes')

custom_print('Analises finalizadas')