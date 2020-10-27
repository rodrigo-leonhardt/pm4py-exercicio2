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

def custom_print(text):
    print(datetime.datetime.now().strftime("%H:%M:%S") +' '+ text)

def print_statistics(net):    
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


def discover_process_models(log_path, log_name):    
    custom_print('Importando log')

    log_complete = xes_importer.apply(log_path)    
    log = variants_filter.filter_log_variants_percentage(log_complete, 0.5)

    custom_print('Log importado')


    #Inductive Miner        
    custom_print('Iniciando Inductive Miner')

    parameters = {inductive_miner.Variants.IM.value.Parameters.CASE_ID_KEY: 'case:concept:name', inductive_miner.Variants.IM.value.Parameters.TIMESTAMP_KEY: 'time:timestamp'}    
    variant = inductive_miner.Variants.IM
    
    petrinet = inductive_miner.apply(log, parameters=parameters, variant=variant)
    print_statistics(petrinet[0])
        
    custom_print('Inductive Miner finalizado\n')


    #Inductive Miner Infrequent 0.2        
    custom_print('Iniciando Inductive Miner Infrequent 0.2')

    parameters = {inductive_miner.Variants.IMf.value.Parameters.NOISE_THRESHOLD: 0.2, inductive_miner.Variants.IMf.value.Parameters.CASE_ID_KEY: 'case:concept:name', inductive_miner.Variants.IMf.value.Parameters.TIMESTAMP_KEY: 'time:timestamp'}    
    variant = inductive_miner.Variants.IMf
    
    petrinet = inductive_miner.apply(log, parameters=parameters, variant=variant)
    print_statistics(petrinet[0])
        
    custom_print('Inductive Miner Infrequent 0.2 finalizado\n')


    #Inductive Miner Infrequent 0.5        
    custom_print('Iniciando Inductive Miner Infrequent 0.5')

    parameters = {inductive_miner.Variants.IMf.value.Parameters.NOISE_THRESHOLD: 0.5, inductive_miner.Variants.IMf.value.Parameters.CASE_ID_KEY: 'case:concept:name', inductive_miner.Variants.IMf.value.Parameters.TIMESTAMP_KEY: 'time:timestamp'}    
    variant = inductive_miner.Variants.IMf
    
    petrinet = inductive_miner.apply(log, parameters=parameters, variant=variant)
    print_statistics(petrinet[0])
        
    custom_print('Inductive Miner Infrequent 0.5 finalizado\n')


    #Inductive Miner Infrequent 0.8        
    custom_print('Iniciando Inductive Miner Infrequent 0.8')

    parameters = {inductive_miner.Variants.IMf.value.Parameters.NOISE_THRESHOLD: 0.8, inductive_miner.Variants.IMf.value.Parameters.CASE_ID_KEY: 'case:concept:name', inductive_miner.Variants.IMf.value.Parameters.TIMESTAMP_KEY: 'time:timestamp'}    
    variant = inductive_miner.Variants.IMf
    
    petrinet = inductive_miner.apply(log, parameters=parameters, variant=variant)
    print_statistics(petrinet[0])
        
    custom_print('Inductive Miner Infrequent 0.8 finalizado\n')


    #Inductive Miner Directly-Follows        
    custom_print('Iniciando Inductive Miner Directly-Follows')

    parameters = {inductive_miner.Variants.IMd.value.Parameters.CASE_ID_KEY: 'case:concept:name', inductive_miner.Variants.IMd.value.Parameters.TIMESTAMP_KEY: 'time:timestamp'}    
    variant = inductive_miner.Variants.IMd
    
    petrinet = inductive_miner.apply(log, parameters=parameters, variant=variant)
    print_statistics(petrinet[0])
        
    custom_print('Inductive Miner Infrequent Directly-Follows\n')


    #Alpha Miner        
    custom_print('Iniciando Alpha Miner')

    parameters = {}
    variant = alpha_miner.Variants.ALPHA_VERSION_CLASSIC
    
    petrinet = alpha_miner.apply(log, parameters=parameters, variant=variant)    
    print_statistics(petrinet[0])
        
    custom_print('Alpha Miner finalizado\n')


    #Heuristic Miner 0.5            
    custom_print('Iniciando Heuristic Miner 0.5')
    
    parameters = {heuristics_miner.Variants.CLASSIC.value.Parameters.DEPENDENCY_THRESH: 0.5}
    
    petrinet = heuristics_miner.apply(log, parameters=parameters)    
    print_statistics(petrinet[0])
    
    custom_print('Heuristic Miner 0.5 finalizado\n')


    #Heuristic Miner 0.5            
    custom_print('Iniciando Heuristic Miner 0.99')
    
    parameters = {heuristics_miner.Variants.CLASSIC.value.Parameters.DEPENDENCY_THRESH: 0.99}
    
    petrinet = heuristics_miner.apply(log, parameters=parameters)    
    print_statistics(petrinet[0])
    
    custom_print('Heuristic Miner 0.99 finalizado\n')


    #Heuristic Miner 0.1            
    custom_print('Iniciando Heuristic Miner 0.1')
    
    parameters = {heuristics_miner.Variants.CLASSIC.value.Parameters.DEPENDENCY_THRESH: 0.1}
    
    petrinet = heuristics_miner.apply(log, parameters=parameters)    
    print_statistics(petrinet[0])
    
    custom_print('Heuristic Miner 0.1 finalizado\n')


#input: log in XES format
custom_print('Iniciando analises')

xes_log_path = '/home/rodrigo/python/bpi2012/logs/BPI_Challenge_2012.xes'
discover_process_models(xes_log_path, 'xes')

custom_print('Analises finalizadas')