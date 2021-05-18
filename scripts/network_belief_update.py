#!/usr/bin/env python
# -*-coding:utf-8 -*-
'''
@File    :   network_belief_update.py
@Time    :   2021/05/16 18:38:01
@Author  :   Shanto Roy 
@Version :   1.0
@Contact :   sroy10@uh.edu
@License :   (C)Copyright 2020-2021, Shanto Roy
@Desc    :   None
'''


import streamlit as st
import pandas as pd
import json
import ast
import os
import random
import numpy as np

import sys
sys.path.append('scripts/')

from network_creation import network_creation
from network_plot import network_plot
from belief_update import initial_belief_calc, belief_update_one_observation 
from instructions import st_instruction_page
from packetToDF import packetToCSV

network_init_conf_data = "data/sim_network_init_conf.csv"
network_observation_data = "data/sim_network_observation.csv"
real_network_init_conf_data = "data/real_network_init_conf.csv"

features = ['ip', 'ip.ttl', 'tcp.window_size', 'ip.flags.df', 'App']
winNT6_x = [128, 8192 ,1]
winNT5_x = [128, 65535, 1]
linK3_11 = [64, 5840, 1]
# cisco = [255, 4128, 0]
bsd = [64, 65535, 1]
GL = [64, 5720, 1]

#test 1
# win_apps = ["Apache", "IIS", "Firefox", "Chrome", 0]
# lin_apps = ["Apache", "Firefox", "Chrome", 0]
# test 2
win_apps = ["Apache", "IIS", 0]
lin_apps = ["Apache", 0]
# #test 3
# win_apps = [0]
# lin_apps = [0]


def create_network(num_of_nodes):
    ip_list = []
    host_id_list = random.sample(range(255), num_of_nodes)
    for j in host_id_list:
        ip_list.append("192.168.1." + str(j))
    return ip_list


obs_ip_list = []

def create_net_observation(num_of_nodes, ip_list, num_of_obs):
    global obs_ip_list
    obs_ip_list = ip_list.copy()
    list_of_obs = []
    for i in range(num_of_nodes):
        if i<=num_of_nodes/3:
            node = [ip_list[i]] + winNT6_x + [np.random.choice(win_apps)]
            obs_node = [node]*num_of_obs
            list_of_obs = list_of_obs + obs_node
        elif i>num_of_nodes/3 and i<=num_of_nodes/2:
            node = [ip_list[i]] + winNT5_x + [np.random.choice(win_apps)]
            obs_node = [node]*num_of_obs
            list_of_obs = list_of_obs + obs_node
        elif i>num_of_nodes/2 and i<=4*num_of_nodes/5:
            node = [ip_list[i]] + linK3_11 + [np.random.choice(lin_apps)]
            obs_node = [node]*num_of_obs
            list_of_obs = list_of_obs + obs_node
        # elif i>4*num_of_nodes/5 and i<=4*num_of_nodes/5+4:
        #     node = [ip_list[i]] + cisco
        #     obs_node = [node]*num_of_obs
        #     list_of_obs = list_of_obs + obs_node
        elif i>4*num_of_nodes/5 and i<=19*num_of_nodes/20:
            node = [ip_list[i]] + bsd + [np.random.choice(lin_apps)]
            obs_node = [node]*num_of_obs
            list_of_obs = list_of_obs + obs_node
        else:
            node = [ip_list[i]] + GL + [np.random.choice(lin_apps)]
            obs_node = [node]*num_of_obs
            list_of_obs = list_of_obs + obs_node
            
    df = pd.DataFrame(list_of_obs, columns=features)
    df.to_csv(network_observation_data)
    return df


# for simulated network only
def network_initial_configuration():
    st.subheader("Possible Configurations for Initial Belief")
    st.markdown("This page shows the set of all possible configurations")

    os_set = []
    os_1 = st.sidebar.checkbox("Win NT 6.x")
    os_2 = st.sidebar.checkbox("Win NT 5.x")
    os_3 = st.sidebar.checkbox("Linux Kernel 3-11")
    # os_4 = st.sidebar.checkbox("Cisco")
    os_5 = st.sidebar.checkbox("BSD")
    os_6 = st.sidebar.checkbox("Google Linux")
    if os_1:
        os_set.append("Win NT 6.x")
    if os_2:
        os_set.append("Win NT 5.x")
    if os_3:
        os_set.append("Linux_v3-11")
    # if os_4:
        # os_set.append("Cisco")
    if os_5:
        os_set.append("BSD")
    if os_6:
        os_set.append("Google Linux")

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
        df_init_conf.to_csv(network_init_conf_data)
    except:
        pass


# for real network: considering the three base OS (Win, Linux, macOS), no application
def real_network_initial_configuration():
    st.subheader("Possible Configurations for Initial Belief")
    st.markdown("This page shows the set of all possible configurations")

    os_set = []
    os_1 = st.sidebar.checkbox("Windows")
    os_2 = st.sidebar.checkbox("Ubuntu")
    os_3 = st.sidebar.checkbox("macOS")

    if os_1:
        os_set.append("Windows")
    if os_2:
        os_set.append("Ubuntu")
    if os_3:
        os_set.append("macOS")

    app_set = []
    
    try:
        conf_set, init_belief_set = initial_belief_calc(os_set, app_set)
        df_init_conf = pd.DataFrame(conf_set, columns = ['OS', 'Apps'])
        df_init_conf["Initial Probability"] = init_belief_set
        st.table(df_init_conf)
        df_init_conf.to_csv(real_network_init_conf_data)
    except:
        pass



def st_network_belief_update():
    st.subheader("Belief Update Process")
    st.markdown("This page shows the consecutive Belief Updates in table\
                and plot. The Belief updating procedure matures over the\
                number of Observations.")

    obs_data = pd.read_csv(network_observation_data)
    obs_data = obs_data.fillna(0)

    feature_selection = st.sidebar.selectbox("Select Number of Features",\
                                    ["TTL, WS, DF", "TTL, WS"])

    if feature_selection == "TTL, WS":
        for ip in obs_ip_list:
            st.write("Belief update for IP:", ip)
            ip_obs_df = obs_data.loc[obs_data['ip'] == ip]

            observation_list = ip_obs_df.T.to_dict().values()
            conf_data = pd.read_csv(network_init_conf_data)

            os_list = conf_data["OS"].tolist()
            app_list = conf_data["Apps"].tolist()
            conf_set = [[i,ast.literal_eval(j)] for i,j in zip(os_list,app_list)]
        
            init_belief_set = conf_data["Initial Probability"].tolist()

            observation_list_app = [i for i in observation_list if i["App"] != 0]
            updated_belief_set = []
            initial_belief_set = init_belief_set.copy()
            for obs in observation_list_app:
                updated_belief_set.append(belief_update_one_observation_2f(conf_set, obs, initial_belief_set))
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
            
            # st.plotly_chart(fig)
            sorted_df = belief_update_df.sort_values(by=belief_update_df.columns[-1], ascending=False)
            # st.table(belief_update_df) 
            st.table(sorted_df.head(2)[["Configurations", "Initial Belief", sorted_df.columns[-1]]]) 

    if feature_selection == "TTL, WS, DF":
        for ip in obs_ip_list:
            st.write("Belief update for IP:", ip)
            ip_obs_df = obs_data.loc[obs_data['ip'] == ip]

            observation_list = ip_obs_df.T.to_dict().values()
            conf_data = pd.read_csv(network_init_conf_data)

            os_list = conf_data["OS"].tolist()
            app_list = conf_data["Apps"].tolist()
            conf_set = [[i,ast.literal_eval(j)] for i,j in zip(os_list,app_list)]
        
            init_belief_set = conf_data["Initial Probability"].tolist()

            observation_list_app = [i for i in observation_list if i["App"] != 0]
            updated_belief_set = []
            initial_belief_set = init_belief_set.copy()
            for obs in observation_list_app:
                updated_belief_set.append(belief_update_one_observation_3f(conf_set, obs, initial_belief_set))
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
            
            # st.plotly_chart(fig)
            sorted_df = belief_update_df.sort_values(by=belief_update_df.columns[-1], ascending=False)
            # st.table(belief_update_df) 
            st.table(sorted_df.head(2)[["Configurations", "Initial Belief", sorted_df.columns[-1]]]) 
        



def belief_update_one_observation_2f(conf_set, obs, prior_belief_set):
    obs_ttl = np.int64(obs["ip.ttl"])
    obs_ws = np.int64(obs["tcp.window_size"])
    obs_app_banner = str(obs["App"])
    obs_given_conf_set = []
    obs_given_app_set = []

    win_6_kb = pd.read_csv("data/f2_win_6_kb.csv")
    win_5_kb = pd.read_csv("data/f2_win_5_kb.csv")
    lin_kb = pd.read_csv("data/f2_lin_kb.csv")
    bsdl_kb = pd.read_csv("data/f2_bsd_kb.csv")
    gll_kb = pd.read_csv("data/f2_gl_kb.csv")

    win_6_kb = win_6_kb.fillna(0)
    win_5_kb = win_5_kb.fillna(0)
    lin_kb = lin_kb.fillna(0)
    bsdl_kb = bsdl_kb.fillna(0)
    gll_kb = gll_kb.fillna(0)


    win_6_kb['ip.ttl'] = win_6_kb['ip.ttl'].astype(int)
    win_5_kb['ip.ttl'] = win_5_kb['ip.ttl'].astype(int)
    lin_kb['ip.ttl'] = lin_kb['ip.ttl'].astype(int)
    bsdl_kb['ip.ttl'] = bsdl_kb['ip.ttl'].astype(int)
    gll_kb['ip.ttl'] = gll_kb['ip.ttl'].astype(int)

    win_6_kb['tcp.window_size'] = win_6_kb['tcp.window_size'].astype(int)
    win_5_kb['tcp.window_size'] = win_5_kb['tcp.window_size'].astype(int)
    lin_kb['tcp.window_size'] = lin_kb['tcp.window_size'].astype(int)
    bsdl_kb['tcp.window_size'] = bsdl_kb['tcp.window_size'].astype(int)
    gll_kb['tcp.window_size'] = gll_kb['tcp.window_size'].astype(int)

    for i in conf_set:
        if i[0] in "Win NT 6.x":
            obs_given_conf = win_6_kb[(win_6_kb['ip.ttl']==obs_ttl) \
                                & (win_6_kb['tcp.window_size']==obs_ws)]['probability'].tolist()
            if len(obs_given_conf) != 0:
                obs_given_conf_set.append(obs_given_conf[0]) 
            else:
                obs_given_conf_set.append(0.01)  
        elif i[0] in "Win NT 5.x":
            obs_given_conf = win_5_kb[(win_5_kb['ip.ttl']==obs_ttl) \
                                & (win_5_kb['tcp.window_size']==obs_ws)]['probability'].tolist()
            if len(obs_given_conf) != 0:
                obs_given_conf_set.append(obs_given_conf[0]) 
            else:
                obs_given_conf_set.append(0.01)
        elif i[0] in "Linux_v3-11":
            obs_given_conf = lin_kb[(lin_kb['ip.ttl']==obs_ttl) \
                                & (lin_kb['tcp.window_size']==obs_ws)]['probability'].tolist()
            if len(obs_given_conf) != 0:
                obs_given_conf_set.append(obs_given_conf[0]) 
            else:
                obs_given_conf_set.append(0.01)
        elif i[0] in "BSD":
            obs_given_conf = bsdl_kb[(bsdl_kb['ip.ttl']==obs_ttl) \
                                & (bsdl_kb['tcp.window_size']==obs_ws)]['probability'].tolist()
            if len(obs_given_conf) != 0:
                obs_given_conf_set.append(obs_given_conf[0]) 
            else:
                obs_given_conf_set.append(0.01)
        elif i[0] in "Google Linux":
            obs_given_conf = gll_kb[(gll_kb['ip.ttl']==obs_ttl) \
                                & (gll_kb['tcp.window_size']==obs_ws)]['probability'].tolist()
            if len(obs_given_conf) != 0:
                obs_given_conf_set.append(obs_given_conf[0]) 
            else:
                obs_given_conf_set.append(0.01)
        else:
            obs_given_conf_set.append(0.1)

        if len(i[1]) == 1:
            if obs_app_banner in i[1]:
                obs_given_app_set.append(0.99)
            else:
                obs_given_app_set.append(0.01)
        else:
            temp = 1
            for y in i[1]:
                if obs_app_banner in y:
                    temp*=0.99
                else:
                    temp*=0.01
            obs_given_app_set.append(temp)

    obs_given_conf_set = np.array(obs_given_conf_set) * np.array(obs_given_app_set) 
    
    conf_set_given_obs = [0]*len(conf_set)
    for i in range(len(conf_set)):
        numerator = obs_given_conf_set[i] * prior_belief_set[i]
        denominator = 0
        for j in range(len(conf_set)):
            denominator += (obs_given_conf_set[j] * prior_belief_set[j])
        conf_set_given_obs[i] = round(numerator/denominator, 10)
    return conf_set_given_obs


def belief_update_one_observation_3f(conf_set, obs, prior_belief_set):
    obs_ttl = np.int64(obs["ip.ttl"])
    obs_ws = np.int64(obs["tcp.window_size"])
    obs_df = np.int64(obs["ip.flags.df"])
    obs_app_banner = str(obs["App"])
    obs_given_conf_set = []
    obs_given_app_set = []

    win_6_kb = pd.read_csv("data/f3_win_6_kb.csv")
    win_5_kb = pd.read_csv("data/f3_win_5_kb.csv")
    lin_kb = pd.read_csv("data/f3_lin_kb.csv")
    bsdl_kb = pd.read_csv("data/f3_bsd_kb.csv")
    gll_kb = pd.read_csv("data/f3_gl_kb.csv")

    win_6_kb = win_6_kb.fillna(0)
    win_5_kb = win_5_kb.fillna(0)
    lin_kb = lin_kb.fillna(0)
    bsdl_kb = bsdl_kb.fillna(0)
    gll_kb = gll_kb.fillna(0)


    win_6_kb['ip.ttl'] = win_6_kb['ip.ttl'].astype(int)
    win_5_kb['ip.ttl'] = win_5_kb['ip.ttl'].astype(int)
    lin_kb['ip.ttl'] = lin_kb['ip.ttl'].astype(int)
    bsdl_kb['ip.ttl'] = bsdl_kb['ip.ttl'].astype(int)
    gll_kb['ip.ttl'] = gll_kb['ip.ttl'].astype(int)

    win_6_kb['tcp.window_size'] = win_6_kb['tcp.window_size'].astype(int)
    win_5_kb['tcp.window_size'] = win_5_kb['tcp.window_size'].astype(int)
    lin_kb['tcp.window_size'] = lin_kb['tcp.window_size'].astype(int)
    bsdl_kb['tcp.window_size'] = bsdl_kb['tcp.window_size'].astype(int)
    gll_kb['tcp.window_size'] = gll_kb['tcp.window_size'].astype(int)

    win_6_kb['ip.flags.df'] = win_6_kb['ip.flags.df'].astype(int)
    win_5_kb['ip.flags.df'] = win_5_kb['ip.flags.df'].astype(int)
    lin_kb['ip.flags.df'] = lin_kb['ip.flags.df'].astype(int)
    bsdl_kb['ip.flags.df'] = bsdl_kb['ip.flags.df'].astype(int)
    gll_kb['ip.flags.df'] = gll_kb['ip.flags.df'].astype(int)

    for i in conf_set:
        if i[0] in "Win NT 6.x":
            obs_given_conf = win_6_kb[(win_6_kb['ip.ttl']==obs_ttl) \
                                & (win_6_kb['tcp.window_size']==obs_ws)\
                                & (win_6_kb['ip.flags.df']==obs_df)]['probability'].tolist()
            if len(obs_given_conf) != 0:
                obs_given_conf_set.append(obs_given_conf[0]) 
            else:
                obs_given_conf_set.append(0.01)  
        elif i[0] in "Win NT 5.x":
            obs_given_conf = win_5_kb[(win_5_kb['ip.ttl']==obs_ttl) \
                                & (win_5_kb['tcp.window_size']==obs_ws)\
                                & (win_5_kb['ip.flags.df']==obs_df)]['probability'].tolist()
            if len(obs_given_conf) != 0:
                obs_given_conf_set.append(obs_given_conf[0]) 
            else:
                obs_given_conf_set.append(0.01)
        elif i[0] in "Linux_v3-11":
            obs_given_conf = lin_kb[(lin_kb['ip.ttl']==obs_ttl) \
                                & (lin_kb['tcp.window_size']==obs_ws)\
                                & (lin_kb['ip.flags.df']==obs_df)]['probability'].tolist()
            if len(obs_given_conf) != 0:
                obs_given_conf_set.append(obs_given_conf[0]) 
            else:
                obs_given_conf_set.append(0.01)
        elif i[0] in "BSD":
            obs_given_conf = bsdl_kb[(bsdl_kb['ip.ttl']==obs_ttl) \
                                & (bsdl_kb['tcp.window_size']==obs_ws)\
                                & (bsdl_kb['ip.flags.df']==obs_df)]['probability'].tolist()
            if len(obs_given_conf) != 0:
                obs_given_conf_set.append(obs_given_conf[0]) 
            else:
                obs_given_conf_set.append(0.01)
        elif i[0] in "Google Linux":
            obs_given_conf = gll_kb[(gll_kb['ip.ttl']==obs_ttl) \
                                & (gll_kb['tcp.window_size']==obs_ws)\
                                & (gll_kb['ip.flags.df']==obs_df)]['probability'].tolist()
            if len(obs_given_conf) != 0:
                obs_given_conf_set.append(obs_given_conf[0]) 
            else:
                obs_given_conf_set.append(0.01)
        else:
            obs_given_conf_set.append(0.1)

        if len(i[1]) == 1:
            if obs_app_banner in i[1]:
                obs_given_app_set.append(0.99)
            else:
                obs_given_app_set.append(0.01)
        else:
            temp = 1
            for y in i[1]:
                if obs_app_banner in y:
                    temp*=0.99
                else:
                    temp*=0.01
            obs_given_app_set.append(temp)

    obs_given_conf_set = np.array(obs_given_conf_set) * np.array(obs_given_app_set) 
    
    conf_set_given_obs = [0]*len(conf_set)
    for i in range(len(conf_set)):
        numerator = obs_given_conf_set[i] * prior_belief_set[i]
        denominator = 0
        for j in range(len(conf_set)):
            denominator += (obs_given_conf_set[j] * prior_belief_set[j])
        conf_set_given_obs[i] = round(numerator/denominator, 10)
    return conf_set_given_obs