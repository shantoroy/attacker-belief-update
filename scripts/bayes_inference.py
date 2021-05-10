
from pgmpy.readwrite import BIFReader
from pgmpy.inference import VariableElimination
import os
import streamlit as st
import numpy as np


# returns feature map
def observation_map(real_obs_dict):
    feature_map = {}
    
    ttl_obs_dict = {
        0:[0,65],
        1:[65,129],
        2:[129,257]
    }
    
    ws_obs_dict = {
        0:[0,20000],
        1:[20000,65537]
    }
    
    nop_obs_dict = {
        0:[0,0],
        1:[1,1]
    }
    
    feature_list = ["ttl", "ws", "nop"]
    mapping_list = [ttl_obs_dict, ws_obs_dict, nop_obs_dict]
    
    obs_feature_list = [key for key in real_obs_dict.keys()]
    
    for i,j in zip(feature_list, mapping_list):
        if i in obs_feature_list:
            for k,v in j.items():
                if real_obs_dict[i] >= v[0] and real_obs_dict[i] <= v[1]:
                    feature_map[i] = k
                    break

    return feature_map



# returns OS map
def os_map(system):
    os_dict = {
        "Windows": 0,
        "Ubuntu": 1,
        "macOS": 2
    }

    evidence = {"os": os_dict[system]}
    return evidence


# for now supports upto 6 observation feature
def query_value(kb, variable_list, evidence_dict, variable_map):
    table = kb.query(variables=variable_list, evidence = evidence_dict)
    variable_seq = table.variables
    phi = None
    if len(variable_seq) == 1:
        phi = round(table.values[variable_map[variable_seq[0]]], 7)
    if len(variable_seq) == 2:
        phi = round(table.values[variable_map[variable_seq[0]]][variable_map[variable_seq[1]]], 7)
    if len(variable_seq) == 3:
        phi = round(table.values[variable_map[variable_seq[0]]][variable_map[variable_seq[1]]]\
                            [variable_map[variable_seq[2]]], 7)
    if len(variable_seq) == 4:
        phi = round(table.values[variable_map[variable_seq[0]]][variable_map[variable_seq[1]]]\
                            [variable_map[variable_seq[2]]][variable_map[variable_seq[3]]], 7)
    if len(variable_seq) == 5:
        phi = round(table.values[variable_map[variable_seq[0]]][variable_map[variable_seq[1]]]\
                            [variable_map[variable_seq[2]]][variable_map[variable_seq[3]]]\
                            [variable_map[variable_seq[4]]], 7)
    if len(variable_seq) == 6:
        phi = round(table.values[variable_map[variable_seq[0]]][variable_map[variable_seq[1]]]\
                            [variable_map[variable_seq[2]]][variable_map[variable_seq[3]]]\
                            [variable_map[variable_seq[4]]][variable_map[variable_seq[5]]], 7)
    return phi


db_path = 'bayes_model_KB'
filename = "bayes_net_KB.bif"
target = os.path.join(db_path, filename)
reader = BIFReader(target)
model = reader.get_model()
bayes_net = VariableElimination(model)

def prob_obs_given_os(obs, system):
    variable_list = [key for key in obs.keys()]
    variable_map = observation_map(obs)
    evidence_dict = os_map(system)
    prob = query_value(bayes_net, variable_list, evidence_dict, variable_map)
    return prob



# for testing
# if __name__ == '__main__':
#     obs = {'ttl': 57, 'nop': 1, 'ws': 81}
#     system = "Windows"
#     prob = prob_obs_given_os(obs, system)
#     print(prob)

def belief_update_one_observation_BN(conf_set, obs, prior_belief_set):

    obs_given_conf_set = []
    obs_given_app_set = []

    for i in conf_set:
        if i[0] == "Windows":
            system = "Windows" 
        elif i[0] == "Ubuntu":
            system = "Ubuntu"
        else:
            system = "macOS"
        
        prob = prob_obs_given_os(obs, system)
        obs_given_conf_set.append(prob)

    obs_given_conf_set = np.array(obs_given_conf_set)
    conf_set_given_obs = [0]*len(conf_set)
    for i in range(len(conf_set)):
        numerator = obs_given_conf_set[i] * prior_belief_set[i]
        denominator = 0
        for j in range(len(conf_set)):
            denominator += (obs_given_conf_set[j] * prior_belief_set[j])
        conf_set_given_obs[i] = round(numerator/denominator, 10)
    return conf_set_given_obs

