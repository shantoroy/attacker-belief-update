#!/usr/bin/env python
# -*-coding:utf-8 -*-
'''
@File    :   main.py
@Time    :   2021/05/16 18:37:52
@Author  :   Shanto Roy 
@Version :   1.0
@Contact :   sroy10@uh.edu
@License :   (C)Copyright 2020-2021, Shanto Roy
@Desc    :   None
'''


import streamlit as st
import pandas as pd
import cufflinks as cf
import plotly
import plotly.graph_objs as go
import json
import ast
import os
import time

import sys
sys.path.append('scripts/')

from network_creation import network_creation
from network_plot import network_plot
from belief_update import initial_belief_calc, belief_update_one_observation 
from belief_update import create_observation
from instructions import st_instruction_page
from network_belief_update import create_network, create_net_observation
from network_belief_update import network_initial_configuration
from network_belief_update import st_network_belief_update

from sim_network import st_simulated_network_prediction
from real_network import st_real_network_prediction

favicon = "icon/favicon.ico"
st.set_page_config(page_title="Attacker's Belief Update", \
            page_icon = favicon, layout = 'wide', initial_sidebar_state = 'auto')

network_data = "data/network.csv"
observation_data = "data/observation.csv"
init_conf_data = "data/init_conf.csv"

def network_details(win, linux):
    network = network_creation(win, linux)
    return network


def st_create_network():
    st.subheader("Network Nodes")
    st.markdown("This page shows the nodes with corresponding Real configurations")

    win = st.sidebar.text_input("Input Number of Windows Machine", 5)
    linux = st.sidebar.text_input("Input Number of Linux Machine", 5)
    show_network = st.sidebar.selectbox(
        'Show Network', ["Plot", "Table"])
    network_df = network_details(int(win), int(linux))
    node_list = []
    num_of_nodes = int(win) + int(linux)
    for i in range(num_of_nodes):
        node_list.append("Node " + str(i + 1))
    network_df.insert(loc=0, column="Nodes", value=node_list) 
    if show_network=="Plot":
        plot_fig = network_plot(network_df)
        st.plotly_chart(plot_fig)
    if show_network=="Table":
        st.table(network_df.style.set_precision(2))
    network_df.to_csv(network_data)


def st_initial_configuration():
    st.subheader("Possible Configurations for Initial Belief")
    st.markdown("This page shows the set of all possible configurations")

    os_set = []
    os_1 = st.sidebar.checkbox("Win Server 2008")
    os_2 = st.sidebar.checkbox("Red Hat 8")
    os_3 = st.sidebar.checkbox("Win 7")
    os_4 = st.sidebar.checkbox("Ubuntu 20.04")
    if os_1:
        os_set.append("Win Server 2008")
    if os_2:
        os_set.append("Red Hat 8")
    if os_3:
        os_set.append("Win 7")
    if os_4:
        os_set.append("Ubuntu 20.04")

    app_set = []
    app_1 = st.sidebar.checkbox("Apache")
    app_2 = st.sidebar.checkbox("IIS")
    app_3 = st.sidebar.checkbox("Firefox")
    app_4 = st.sidebar.checkbox("Chrome")
    if app_1:
        app_set.append("Apache")
    if app_2:
        app_set.append("IIS")
    if app_3:
        app_set.append("Firefox")
    if app_4:
        app_set.append("Chrome")
    
    try:
        conf_set, init_belief_set = initial_belief_calc(os_set, app_set)
        df_init_conf = pd.DataFrame(conf_set, columns = ['OS', 'Apps'])
        df_init_conf["Initial Probability"] = init_belief_set
        st.table(df_init_conf)
        df_init_conf.to_csv(init_conf_data)
    except:
        pass



def st_create_observation():
    st.subheader("Create Observation for Nodes")
    st.markdown("This page shows the parameters of creating observation for a particular Node.")

    observation_conf = []
    st.sidebar.write("Choose One OS and One App")
    os_1 = st.sidebar.checkbox("Win Server 2008")
    os_2 = st.sidebar.checkbox("Red Hat 8")
    os_3 = st.sidebar.checkbox("Win 7")
    os_4 = st.sidebar.checkbox("Ubuntu 20.04")
    if os_1:
        observation_conf.append("Win Server 2008")
    if os_2:
        observation_conf.append("Red Hat 8")
    if os_3:
        observation_conf.append("Win 7")
    if os_4:
        observation_conf.append("Ubuntu 20.04")

    app_1 = st.sidebar.checkbox("Apache")
    app_2 = st.sidebar.checkbox("IIS")
    app_3 = st.sidebar.checkbox("Firefox")
    app_4 = st.sidebar.checkbox("Chrome")
    if app_1:
        observation_conf.append("Apache")
    if app_2:
        observation_conf.append("IIS")
    if app_3:
        observation_conf.append("Firefox")
    if app_4:
        observation_conf.append("Chrome")

    try:
        num_of_observation = int(st.sidebar.text_input("Input No. of Observations", "5"))
        observation_list = create_observation(observation_conf, num_of_observation)
        observation_df = pd.DataFrame(observation_list)
        st.table(observation_df)
        observation_df.to_csv(observation_data)
    except:
        pass
        



def st_belief_update():
    st.subheader("Belief Update Process")
    st.markdown("This page shows the consecutive Belief Updates in table\
                and plot. The Belief updating procedure matures over the\
                number of Observations.")
    obs_data = pd.read_csv(observation_data)
    obs_data = obs_data.fillna(0)
    # for OS only
    observation_list = obs_data.T.to_dict().values()

    conf_data = pd.read_csv(init_conf_data)
    os_list = conf_data["OS"].tolist()
    app_list = conf_data["Apps"].tolist()
    conf_set = [[i,ast.literal_eval(j)] for i,j in zip(os_list,app_list)]
    
    # read_init_belief_set = pd.read_csv(init_conf_data)
    # init_belief_set = read_init_belief_set["Initial Probability"].tolist()
    init_belief_set = conf_data["Initial Probability"].tolist()

    update_target = st.sidebar.selectbox("Target Information (All/filtered Observations)",\
                                    ["OS", "OS+App"])

    if update_target == "OS":
        updated_belief_set = []
        initial_belief_set = init_belief_set.copy()
        for obs in observation_list:
            updated_belief_set.append(belief_update_one_observation(conf_set, obs, initial_belief_set))
            initial_belief_set = updated_belief_set[-1]

        belief_update_data = {}
        belief_update_data.update({"Configurations" : conf_set})
        belief_update_data.update({"Initial Belief" : init_belief_set})
        for i in range(len(observation_list)):
            belief_update_data.update({"obs. "+str(i+1) : updated_belief_set[i]})
        belief_update_df = pd.DataFrame(belief_update_data)

        plot_data = [init_belief_set] + updated_belief_set
        obs_list = ["initial belief"]
        for i in range(len(observation_list)):
            obs_list.append("obs " + str(i+1))
        x = range(len(obs_list))
        data = []
        fig = go.Figure()
        for k in range(len(conf_set)):
            y_list = [m[k] for m in plot_data]
            fig.add_trace(go.Scatter(x=obs_list, y=y_list,
                            mode='lines+markers',
                            name=str(conf_set[k])))
        
        fig['layout'].update(height=600, width=950)
        belief_update_output = st.sidebar.selectbox("Choose Output Type",\
                                        ["Plot", "Table"])
        if belief_update_output == "Plot":
            st.plotly_chart(fig)
        if belief_update_output == "Table":
            st.table(belief_update_df)  

    # for OS + App
    if update_target == "OS+App" and "App" in obs_data.columns:
        observation_list_app = [i for i in observation_list if i["App"] != 0]
        updated_belief_set = []
        initial_belief_set = init_belief_set.copy()
        for obs in observation_list_app:
            updated_belief_set.append(belief_update_one_observation(conf_set, obs, initial_belief_set))
            initial_belief_set = updated_belief_set[-1]

        belief_update_data = {}
        belief_update_data.update({"Configurations" : conf_set})
        belief_update_data.update({"Initial Belief" : init_belief_set})
        for i in range(len(observation_list_app)):
            belief_update_data.update({"obs. "+str(i+1) : updated_belief_set[i]})
        belief_update_df = pd.DataFrame(belief_update_data)

        plot_data = [init_belief_set] + updated_belief_set
        obs_list = ["initial belief"]
        for i in range(len(observation_list_app)):
            obs_list.append("obs " + str(i+1))
        x = range(len(obs_list))
        data = []
        fig = go.Figure()
        for k in range(len(conf_set)):
            y_list = [m[k] for m in plot_data]
            fig.add_trace(go.Scatter(x=obs_list, y=y_list,
                            mode='lines+markers',
                            name=str(conf_set[k])))
        
        fig['layout'].update(height=600, width=950)
        belief_update_output = st.sidebar.selectbox("Choose Output Type",\
                                        ["Plot", "Table"])
        if belief_update_output == "Plot":
            st.plotly_chart(fig)
        if belief_update_output == "Table":
            st.table(belief_update_df)  

    else:
        st.write("Only OS related Observations are available")



def st_node_belief_update():
    network_df = pd.read_csv(network_data)
    nodes = network_df["Nodes"].tolist()
    os_list = network_df["OS"].tolist()
    App_list = network_df["App"].tolist()
    confs = [[i,j] for i,j in zip(os_list,App_list)]
    conf_dic = dict(zip(nodes, confs))

    select_node = st.sidebar.selectbox("Choose a Node", nodes)
    if select_node:
        st.sidebar.write("Real Configuration: ", conf_dic[select_node][0]\
                                        +","+ conf_dic[select_node][1])
        sub_function = st.sidebar.selectbox("Choose from the following",\
                                ["Create Observations", "View Observations",\
                                "Updated Belief Info"])

        if sub_function == "Create Observations":
            st_create_observation()
        if sub_function == "View Observations":
            updated_obs_data = pd.read_csv(observation_data)
            del updated_obs_data["Unnamed: 0"]
            st.table(updated_obs_data)
        if sub_function == "Updated Belief Info":
            st_belief_update()



def main():
    # SideBar Settings
    st.sidebar.title("Control Panel")
    st.sidebar.info(
            "Create a Network, Input Attacker's Initial Belief Parameters\
            , Create observations, and Check Outputs"
        )

    # app functionalities
    primary_function = st.sidebar.selectbox(
        'Choose App Functionality', ["View Instructions", "Real Network Prediction", \
                    "Simulated Node Prediction", "Simulated Network Prediction"])


    # View Instructions by Default
    if primary_function == "View Instructions":
        st_instruction_page()

    if primary_function == "Real Network Prediction":
        st_real_network_prediction()

    if primary_function == "Simulated Network Prediction":
        st_simulated_network_prediction()

    if primary_function == "Simulated Node Prediction":
        function = st.sidebar.selectbox(
        'Choose Functionality', ["Create Network", \
                    "Initial Belief Config", "Node Belief Update"])

        # create network and show on the dashboard
        if function == "Create Network":
            st_create_network()

        # create initial configuration and show list to user
        if function == "Initial Belief Config":
            st_initial_configuration()


        if function == "Node Belief Update":
            st_node_belief_update()
        

if __name__ == '__main__':
    main()