import streamlit as st
import pandas as pd
import time

from network_belief_update import create_network, create_net_observation
from network_belief_update import network_initial_configuration
from network_belief_update import st_network_belief_update


def st_simulated_network_prediction():
    function = st.sidebar.selectbox(
        'Choose Functionality', ["Create Observations", \
                    "Set Initial Config","Updated Belief Info"])

    if function == "Create Observations":
        num_of_nodes = int(st.sidebar.text_input("Input Number of Nodes", 20))
        ip_list = create_network(num_of_nodes)
        num_of_obs = int(st.sidebar.text_input("Input Number of Observations/Node", 20))
        st.sidebar.write("Number of total obs = ", num_of_nodes*num_of_obs)
        obs_df = create_net_observation(num_of_nodes, ip_list, num_of_obs)
        st.write("Shape of the Observation Table is:", obs_df.shape)
        st.write("First 20 Created Observations")
        st.table(obs_df.head(20).assign(remove_index='').set_index('remove_index'))

    if function == "Set Initial Config":
        network_initial_configuration()

    if function == "Updated Belief Info":
        start_time = time.time()
        st_network_belief_update()   
        stop_time = time.time()
        st.write("Execution time (seconds): ", stop_time-start_time)