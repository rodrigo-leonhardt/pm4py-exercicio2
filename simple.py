import datetime
import pandas as pd
from pm4py.objects.log.importer.xes import importer as xes_importer
from pm4py.objects.petri import reachability_graph
from pm4py.objects.petri.exporter import exporter as pnml_exporter
from pm4py.objects.conversion.log import converter as log_converter
from pm4py.objects.log.exporter.xes import exporter as xes_exporter
from pm4py.objects.conversion.process_tree import converter as pt_converter
from pm4py.algo.discovery.inductive import algorithm as inductive_miner
from pm4py.algo.discovery.dfg import algorithm as dfg_discovery
from pm4py.algo.discovery.footprints import algorithm as footprints_discovery
from pm4py.visualization.petrinet import visualizer as pn_visualizer
from pm4py.visualization.dfg import visualizer as dfg_visualization
from pm4py.visualization.transition_system import visualizer as ts_visualizer
from pm4py.evaluation.replay_fitness import evaluator as replay_fitness
from pm4py.evaluation.generalization import evaluator as calc_generaliz
from pm4py.evaluation.precision import evaluator as calc_precision
from pm4py.evaluation.simplicity import evaluator as calc_simplic
from pm4py.algo.conformance.alignments import algorithm as alignments
from pm4py.algo.discovery.alpha import algorithm as alpha_miner
from pm4py.algo.discovery.heuristics import algorithm as heuristics_miner
from pm4py.evaluation.soundness.woflan import algorithm as woflan
from pm4py.algo.filtering.log.timestamp import timestamp_filter
from pm4py.algo.filtering.log.variants import variants_filter
from pm4py.algo.filtering.log.end_activities import end_activities_filter
from pm4py.algo.filtering.log.attributes import attributes_filter

def custom_print(text):
    print(datetime.datetime.now().strftime("%H:%M:%S") +' '+ text)

def print_statistics(net, name):  
    gviz = pn_visualizer.apply(net)
    gviz.render('petrinets/simple-'+ name, cleanup=True, format='png')

    places = net.places
    transitions = net.transitions
    arcs = net.arcs

    print('Lugares:', len(places), 'Arcos:', len(arcs), 'Transições:', len(transitions))
    
    print('Transição Inputs Outputs')
    

    for transition in transitions:
        i = len(transition.in_arcs)
        o = len(transition.out_arcs)

        if (i < 1) or (o < 1) :
            print(transition.name, i, o)  


    sP = ''

    for place in places:

        if (sP != ''):
            sP = sP +','

        sP = sP + place.name


    sT = ''

    for transition in transitions:

        if (sT != ''):
            sT = sT +','

        sT = sT + transition.name


    sF = ''

    for arc in arcs:

        if (sF != ''):
            sF = sF +','

        sF = sF +'('+ arc.source.name +','+ arc.target.name +')'


    print('Definição')  
    print('P = {'+ sP +'}')
    print('T = {'+ sT +'}')
    print('F = {'+ sF +'}')


def discover_process_models(log_path, log_name):    
    custom_print('Importando log')

    log_complete = xes_importer.apply(log_path)    
    log = variants_filter.filter_log_variants_percentage(log_complete, 0.9)

    #A_ACTIVATED, A_DECLINED, A_CANCELLED
    #log = attributes_filter.apply(log_complete, ["A_ACTIVATED"], parameters={attributes_filter.Parameters.ATTRIBUTE_KEY: "concept:name", attributes_filter.Parameters.POSITIVE: True})

    custom_print('Log importado')


    if (1 == 2) :
        #Inductive Miner        
        custom_print('Iniciando Inductive Miner')

        parameters = {inductive_miner.Variants.IM.value.Parameters.CASE_ID_KEY: 'case:concept:name', inductive_miner.Variants.IM.value.Parameters.TIMESTAMP_KEY: 'time:timestamp'}    
        variant = inductive_miner.Variants.IM
        
        petrinet = inductive_miner.apply(log, parameters=parameters, variant=variant)
        print_statistics(petrinet[0], 'IM')
            
        custom_print('Inductive Miner finalizado\n')


    if (1 == 2) :
        #Inductive Miner Infrequent 0.2        
        custom_print('Iniciando Inductive Miner Infrequent 0.2')

        parameters = {inductive_miner.Variants.IMf.value.Parameters.NOISE_THRESHOLD: 0.2, inductive_miner.Variants.IMf.value.Parameters.CASE_ID_KEY: 'case:concept:name', inductive_miner.Variants.IMf.value.Parameters.TIMESTAMP_KEY: 'time:timestamp'}    
        variant = inductive_miner.Variants.IMf
        
        petrinet = inductive_miner.apply(log, parameters=parameters, variant=variant)
        print_statistics(petrinet[0], 'IMf0.2')
            
        custom_print('Inductive Miner Infrequent 0.2 finalizado\n')


    if (1 == 1) :
        #Inductive Miner Infrequent 0.5        
        custom_print('Iniciando Inductive Miner Infrequent 0.5')

        parameters = {inductive_miner.Variants.IMf.value.Parameters.NOISE_THRESHOLD: 0.5, inductive_miner.Variants.IMf.value.Parameters.CASE_ID_KEY: 'case:concept:name', inductive_miner.Variants.IMf.value.Parameters.TIMESTAMP_KEY: 'time:timestamp'}    
        variant = inductive_miner.Variants.IMf
        
        petrinet, initial_marking, final_marking = inductive_miner.apply(log, parameters=parameters, variant=variant)
        print_statistics(petrinet, 'IMf0.5')
            
        custom_print('Inductive Miner Infrequent 0.5 finalizado\n')

        ts = reachability_graph.construct_reachability_graph(petrinet, initial_marking)
        gviz = ts_visualizer.apply(ts, parameters={ts_visualizer.Variants.VIEW_BASED.value.Parameters.FORMAT: "png"})
        gviz.render('petrinets/simple-reach', cleanup=True) 

        pnml_exporter.apply(petrinet, initial_marking, "petrinets/simple-petri.pnml")


    if (1 == 2) :
        #Inductive Miner Infrequent 0.8        
        custom_print('Iniciando Inductive Miner Infrequent 0.8')

        parameters = {inductive_miner.Variants.IMf.value.Parameters.NOISE_THRESHOLD: 0.8, inductive_miner.Variants.IMf.value.Parameters.CASE_ID_KEY: 'case:concept:name', inductive_miner.Variants.IMf.value.Parameters.TIMESTAMP_KEY: 'time:timestamp'}    
        variant = inductive_miner.Variants.IMf
        
        petrinet = inductive_miner.apply(log, parameters=parameters, variant=variant)
        print_statistics(petrinet[0], 'IMf0.8')
            
        custom_print('Inductive Miner Infrequent 0.8 finalizado\n')


    if (1 == 2) :
        #Inductive Miner Directly-Follows        
        custom_print('Iniciando Inductive Miner Directly-Follows')

        parameters = {inductive_miner.Variants.IMd.value.Parameters.CASE_ID_KEY: 'case:concept:name', inductive_miner.Variants.IMd.value.Parameters.TIMESTAMP_KEY: 'time:timestamp'}    
        variant = inductive_miner.Variants.IMd
        
        petrinet = inductive_miner.apply(log, parameters=parameters, variant=variant)
        print_statistics(petrinet[0], 'IMd')
            
        custom_print('Inductive Miner Infrequent Directly-Follows\n')


    if (1 == 2) :
        #Alpha Miner        
        custom_print('Iniciando Alpha Miner')

        parameters = {}
        variant = alpha_miner.Variants.ALPHA_VERSION_CLASSIC
        
        petrinet = alpha_miner.apply(log, parameters=parameters, variant=variant)    
        print_statistics(petrinet[0], 'Alpha')
            
        custom_print('Alpha Miner finalizado\n')


    if (1 == 2) :
        #Heuristic Miner 0.5            
        custom_print('Iniciando Heuristic Miner 0.5')
        
        parameters = {heuristics_miner.Variants.CLASSIC.value.Parameters.DEPENDENCY_THRESH: 0.5}
        
        petrinet = heuristics_miner.apply(log, parameters=parameters)    
        print_statistics(petrinet[0], 'HM0.5')
        
        custom_print('Heuristic Miner 0.5 finalizado\n')


    if (1 == 2) :
        #Heuristic Miner 0.99            
        custom_print('Iniciando Heuristic Miner 0.99')
        
        parameters = {heuristics_miner.Variants.CLASSIC.value.Parameters.DEPENDENCY_THRESH: 0.99}
        
        petrinet = heuristics_miner.apply(log, parameters=parameters)    
        print_statistics(petrinet[0], 'HM0.99')
        
        custom_print('Heuristic Miner 0.99 finalizado\n')


    if (1 == 2) :
        #Heuristic Miner 0.1            
        custom_print('Iniciando Heuristic Miner 0.1')
        
        parameters = {heuristics_miner.Variants.CLASSIC.value.Parameters.DEPENDENCY_THRESH: 0.1}
        
        petrinet = heuristics_miner.apply(log, parameters=parameters)    
        print_statistics(petrinet[0], 'HM0.1')
        
        custom_print('Heuristic Miner 0.1 finalizado\n')


    if (1 == 2) :
        #Heuristic Miner 1.0            
        custom_print('Iniciando Heuristic Miner 1.0')
        
        parameters = {heuristics_miner.Variants.CLASSIC.value.Parameters.DEPENDENCY_THRESH: 1.0}
        
        petrinet = heuristics_miner.apply(log, parameters=parameters)    
        print_statistics(petrinet[0], 'HM1.0')
        
        custom_print('Heuristic Miner 1.0 finalizado\n')


    if (1 == 2) :
        #DFG
        custom_print('Iniciando DFG')

        dfg = dfg_discovery.apply(log)
        parameters = {dfg_visualization.Variants.FREQUENCY.value.Parameters.FORMAT: 'png'}
        gviz = dfg_visualization.apply(dfg, log=log, variant=dfg_visualization.Variants.FREQUENCY, parameters=parameters)
        dfg_visualization.save(gviz, 'petrinets/simple-DFG.png')

        custom_print('DFG finalizado\n')


#input: log in XES format
custom_print('Iniciando analises')

xes_log_path = '/home/rodrigo/python/bpi2012/logs/BPI_Challenge_2012_reduced.xes'
discover_process_models(xes_log_path, 'xes')

custom_print('Analises finalizadas')