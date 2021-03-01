import pandas as pd
import numpy as np
import random
import streamlit as st


win_family = ["Win 7", "Win Server 2008"]
linux_family = ["Red Hat 8", "Ubuntu 20.04"]

def powerset(s):
    x = len(s)
    masks = [1 << i for i in range(x)]
    for i in range(1 << x):
        yield [ss for mask, ss in zip(masks, s) if i & mask]


def configuration_set(os_set,app_combination_set):
    return [[os, app] for os in os_set for app in app_combination_set]


def initial_belief_calc(os_set, app_set):
    app_power_set = list(powerset(app_set))
    conf_set = configuration_set(os_set,app_power_set)
    init_belief_set = [1/len(conf_set)]*len(conf_set)
    return conf_set, init_belief_set


def belief_update_one_observation(conf_set, obs, prior_belief_set):
    obs_ttl = np.int64(obs["TTL"])
    obs_ws = np.int64(obs["WS"])
    obs_app_banner = str(obs["App"])
    obs_given_conf_set = []
    obs_given_app_set = []

    win_kb = pd.read_csv("data/win_kb.csv")
    lin_kb = pd.read_csv("data/lin_kb.csv")

    win_kb = win_kb.fillna(0)
    lin_kb = lin_kb.fillna(0)
    
    win_kb['ttl'] = win_kb['ttl'].astype(int)
    win_kb['ws'] = win_kb['ws'].astype(int)
    lin_kb['ttl'] = lin_kb['ttl'].astype(int)
    lin_kb['ws'] = lin_kb['ws'].astype(int)

    for i in conf_set:
        if i[0] in win_family:
            obs_given_conf = win_kb[(win_kb['ttl']==obs_ttl) \
                                & (win_kb['ws']==obs_ws)]['probability'].tolist()
            if len(obs_given_conf) != 0:
                obs_given_conf_set.append(obs_given_conf[0]) 
            else:
                obs_given_conf_set.append(0.01)  
        elif i[0] in linux_family:
            obs_given_conf = lin_kb[(lin_kb['ttl']==obs_ttl) \
                                & (lin_kb['ws']==obs_ws)]['probability'].tolist()
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


def create_observation(configuration, num_of_obs=5):
    obs_set = []
    try:
        for i in range(num_of_obs):
            obs = {}
            if len(configuration) == 1:
                choice = random.randint(1,3)
                if configuration[0] in win_family:
                    if choice == 1:
                        obs['TTL'] = np.random.randint(120,129)
                    if choice == 2:
                        obs['WS'] = 8192
                    if choice == 3:
                        obs['TTL'] = np.random.randint(120,129)
                        obs['WS'] = 8192

                if configuration[0] in linux_family:
                    if choice == 1:
                        obs['TTL'] = np.random.randint(60,64)
                    if choice == 2:
                        obs['WS'] = 5840
                    if choice == 3:
                        obs['TTL'] = np.random.randint(60,64)
                        obs['WS'] = 5840

            if len(configuration) > 1:
                choice = random.randint(1,6)
                app_choice = random.randint(1,len(configuration)-1)
                if configuration[0] in win_family:
                    if choice == 1:
                        obs['TTL'] = np.random.randint(120,129)
                    if choice == 2:
                        obs['WS'] = 8192
                    if choice == 3:
                        obs['TTL'] = np.random.randint(120,129)
                        obs['WS'] = 8192
                    if choice == 4:
                        obs['TTL'] = np.random.randint(120,129)
                        obs['App'] = configuration[app_choice]
                    if choice == 5:
                        obs['WS'] = 8192
                        obs['App'] = configuration[app_choice]
                    if choice == 6:
                        obs['TTL'] = np.random.randint(120,129)
                        obs['WS'] = 8192
                        obs['App'] = configuration[app_choice]
                    

                if configuration[0] in linux_family:
                    if choice == 1:
                        obs['TTL'] = np.random.randint(60,64)
                    if choice == 2:
                        obs['WS'] = 5840
                    if choice == 3:
                        obs['TTL'] = np.random.randint(60,64)
                        obs['WS'] = 5840
                    if choice == 4:
                        obs['TTL'] = np.random.randint(60,64)
                        obs['App'] = configuration[app_choice]
                    if choice == 5:
                        obs['WS'] = 5840
                        obs['App'] = configuration[app_choice]
                    if choice == 6:
                        obs['TTL'] = np.random.randint(60,64)
                        obs['WS'] = 5840
                        obs['App'] = configuration[app_choice]

            obs_set.append(obs)
    except:
        pass
    return obs_set




