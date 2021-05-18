#!/usr/bin/env python
# -*-coding:utf-8 -*-
'''
@File    :   network_predict.py
@Time    :   2021/05/16 18:37:28
@Author  :   Shanto Roy 
@Version :   1.0
@Contact :   sroy10@uh.edu
@License :   (C)Copyright 2020-2021, Shanto Roy
@Desc    :   None
'''


import pandas as pd
import numpy as np
import streamlit as st
from pandas.core.algorithms import value_counts
from scipy.stats import entropy
from collections import Iterable
import random
from functools import reduce
import operator
import plotly.express as px


def flatten(lis):
    for item in lis:
        if isinstance(item, Iterable) and not isinstance(item, str):
            for x in flatten(item):
                yield x
        else:        
            yield item

            
def cartesianProduct(a,b):
    return [[i,j] for i in a for j in b]
  
    
# Function to do a cartesian 
# product of N sets 
def Cartesian(list_a, n):
    temp = list_a[0]
    for i in range(1, n):
        temp = cartesianProduct(temp, list_a[i])
    return temp
  

def entropy_calc(conf):
    pd_series = pd.Series(conf)
    counts = pd_series.value_counts()
    entropy_val = entropy(counts)
    return entropy_val


def calc_os_probability(conf):
    prob_dict = {}
    platforms = set(conf)
    for i in platforms:
        prob_dict[i] = conf.count(i)/len(conf)
    return prob_dict


def calc_net_conf_prob(true_conf, test_conf, node_prob_dict):
    node_prob_list = list(node_prob_dict.values())
    if len(true_conf) == len(test_conf):
        node_prob = []
        for i in range(len(true_conf)):
            prob = node_prob_list[i]
            if true_conf[i] == test_conf[i]:
                node_prob.append(prob)   
            else:
                node_prob.append(1-prob)   
    return node_prob


# Example input
# node_os_dict = {
#     "192.168.1.5": "Windows",
#     "192.168.1.10": "Ubuntu",
#     "192.168.1.15": "Windows"
# }
def os_list(node_os_dict):
    os_dict = {
        "Windows": 0,
        "Ubuntu": 1,
        "macOS": 2
    }
    os = list(set([os_dict[v] for k,v in node_os_dict.items() if v in os_dict.keys()]))
    true_conf = [os_dict[v] for k,v in node_os_dict.items() if v in os_dict.keys()]
    return os, true_conf


# Example Input
# node_prob_dict = {
#     "192.168.1.5": 0.8,
#     "192.168.1.10": 1,
#     "192.168.1.15": 0.7
# }
def updated_conf_prob(node_os_dict, node_prob_dict):
    os, true_conf = os_list(node_os_dict)

    num_of_node = len(node_prob_dict)
    list_a = [os for i in range(num_of_node)] 
    n = len(list_a) 

    cart = Cartesian(list_a, n)
    network_conf_list = [list(flatten(i)) for i in cart]


    network_prob_dict = {}
    new_prob_list = []
    st.write()
    st.write("########################################")
    for i in network_conf_list:
        node_prob_list = calc_net_conf_prob(true_conf, i, node_prob_dict)
        network_prob = reduce((lambda x, y: x * y), node_prob_list)
        entropy_val = entropy(i)
        new_network_prob = network_prob /entropy_val
        new_prob_list.append(round(new_network_prob, 5))
    new_prob_list = [0 if np.isnan(i) or np.isinf(i) else i for i in new_prob_list]
    # st.write(new_prob_list)
    # st.write(type(new_prob_list[1]))
    norm_prob = [i/sum(new_prob_list) for i in new_prob_list]

    st.write("Sum of final Probabilities =", round(sum(norm_prob),5))
    st.write("No. of total Configurations", len(new_prob_list))
    st.write("########################################")

    for i,j in zip(network_conf_list, norm_prob):
        network_prob_dict[str(i)] = j

    st.write()
    # for k,v in network_prob_dict.items():
    #     st.write(k, "-->", v)

    network_prob_values = list(network_prob_dict.values())
    max_conf = max(network_prob_dict.items(), key=operator.itemgetter(1))[0]
    st.write(max_conf, "-->", max(network_prob_values))

    st_fig_df = pd.DataFrame({'Configurations': list(range(len(network_prob_values))),\
                                    'Probabilities': network_prob_values})
    fig = px.scatter(st_fig_df, x = 'Configurations', y = 'Probabilities',\
                            color_continuous_scale=px.colors.sequential.Viridis)
    st.plotly_chart(fig)

    st.write("")
    st.write("########################################")
    st.write("Here...")
    st.write("0-> Windows, 1-> Ubuntu, 2-> macOS")




