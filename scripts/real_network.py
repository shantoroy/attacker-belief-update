import streamlit as st
import pandas as pd
import json
import ast
import os
import time
import joblib
import numpy as np
from collections import Counter

from packetToDF import packetToCSV
from pcap2DF import pcap2CSV
from network_belief_update import real_network_initial_configuration
from bayes_inference import belief_update_one_observation_BN


real_network_init_conf_data = "data/real_network_init_conf.csv"

####################################################################
########################### ML Section #############################
####################################################################

def data_preprocess(init_df):
    df = init_df.drop(columns=['ip.tos', 'tcp.options.mss_val'])
    final_df = df.dropna()
    return final_df

def st_machine_learning():
    init_df = pd.read_csv("data/testPacketToCSV.csv")
    processed_df = data_preprocess(init_df)
    x_iloc_list = [1,5,8,13,17,18,19,20,22,23,24,25,26,29]

    model = st.sidebar.selectbox(
                'Choose Model', ["LR", "KNN", "SVM(rbf)", "NB", "DT", "RF"])
    
    if model == "LR":
        try:
            loaded_model = joblib.load("saved_models/predict_base_OS/lr.sav")
        except Exception as e:
            st.write(e)
        
    if model == "KNN":
        try:
            loaded_model = joblib.load("saved_models/predict_base_OS/knn.sav")
        except Exception as e:
            st.write(e)

    if model == "SVM(rbf)":
        try:
            loaded_model = joblib.load("saved_models/predict_base_OS/svm.sav")
        except Exception as e:
            st.write(e)

    if model == "NB":
        try:
            loaded_model = joblib.load("saved_models/predict_base_OS/nb.sav")
        except Exception as e:
            st.write(e)

    if model == "DT":
        try:
            loaded_model = joblib.load("saved_models/predict_base_OS/tree.sav")
        except Exception as e:
            st.write(e)

    if model == "RF":
        try:
            loaded_model = joblib.load("saved_models/predict_base_OS/rf.sav")
        except Exception as e:
            st.write(e)


    ip_list = processed_df["ip.src"].unique().tolist()

    for ip in ip_list:
        st.write("---------------------------------->")
        st.write("Prediction for IP:", ip)
        # for each ip create individual DF
        ip_obs_df = processed_df.loc[processed_df["ip.src"] == ip]
        # add all rows as list in the obs_list
        ip_obs_list = []
        for i in range(len(ip_obs_df)):
            ip_obs_list.append(ip_obs_df.iloc[i, x_iloc_list].tolist())
        # st.write(ip_obs_list)

        prediction_list = []
        for obs in ip_obs_list:
            obs_np_array = np.array(obs)
            reshaped_obs = obs_np_array.reshape(1,-1)
            prediction = loaded_model.predict(reshaped_obs)
            # st.write(prediction)
            prediction_list.append(list(prediction)[0])
        # st.write(prediction_list)

        final_prediction = {}
        unique_prediction = Counter(prediction_list).keys()
        prediction_count = Counter(prediction_list).values()
        for i,j in zip(unique_prediction,prediction_count):
            final_prediction[i] = j 
        
        st.write("Total Observation: ", len(prediction_list))
        st.write(final_prediction)
        st.write("\n")


####################################################################
############################# Bayes Net ############################
####################################################################

def bayes_net_update():
    init_df = pd.read_csv("data/testPacketToCSV.csv")
    processed_df = data_preprocess(init_df)
    ip_list = processed_df["ip.src"].unique().tolist()

    for ip in ip_list:
        st.write("---------------------------------->")
        st.write("Belief update for IP:", ip)
        ip_obs_df = processed_df.loc[processed_df["ip.src"] == ip]

        conf_data = pd.read_csv(real_network_init_conf_data)

        # filter ip_obs_df based on only feature columns
        ip_obs_df = ip_obs_df[["ip.ttl", "ip.flags.df", "tcp.window_size"]]
        # rename column names to match with belief update function
        ip_obs_df = ip_obs_df.rename(columns={'ip.ttl': 'ttl', 'ip.flags.df': 'nop', \
                                                'tcp.window_size': 'ws'})

        # # convert float to int for all columns (otherwise there will be errors)
        # ip_obs_df = ip_obs_df.astype(int)

        observation_list = ip_obs_df.T.to_dict().values()
        # st.write(observation_list)

        os_list = conf_data["OS"].tolist()
        app_list = conf_data["Apps"].tolist()
        conf_set = [[i,ast.literal_eval(j)] for i,j in zip(os_list,app_list)]
    
        init_belief_set = conf_data["Initial Probability"].tolist()

        # need fix from here
        # observation_list_app = [i for i in observation_list if i["App"] != 0]
        updated_belief_set = []
        initial_belief_set = init_belief_set.copy()
        for obs in observation_list:
            updated_belief_set.append(belief_update_one_observation_BN(conf_set, obs, initial_belief_set))
            initial_belief_set = updated_belief_set[-1]

        belief_update_data = {}
        belief_update_data.update({"Configurations" : conf_set})
        belief_update_data.update({"Initial Belief" : init_belief_set})
        for i in range(len(observation_list)):
            belief_update_data.update({"obs. "+str(i+1) : updated_belief_set[i]})
        belief_update_df = pd.DataFrame(belief_update_data)

        st.write(belief_update_df)


####################################################################
########################### File Reading ###########################
####################################################################

def try_read_df(f):
    try:
        return pd.read_csv(f)
    except:
        pass
    #     return pd.read_excel(f)



####################################################################
######################## Streamlit Interface #######################
####################################################################


def st_real_network_prediction():
    function = st.sidebar.selectbox(
        'Choose Functionality', ["Upload Observation File", \
                                            "Select Method"])

    if function == "Upload Observation File":
        filetype = st.sidebar.selectbox(
        'Choose File Type', ["PCAP File", "CSV/Excel"])

        if filetype == "CSV/Excel":
            uploaded_file = st.sidebar.file_uploader("Upload a file", accept_multiple_files=False,\
                                                                    type=("csv", "xls"))
            if uploaded_file is not None:
                data = try_read_df(uploaded_file)
                st.write("Here are the first ten rows of the File")
                st.table(data.head(10))
                file_details = {"FileName":uploaded_file.name,"FileType":uploaded_file.type,\
                                                            "FileSize":uploaded_file.size}
                st.sidebar.write(file_details)


        if filetype == "PCAP File":
            uploaded_file = st.sidebar.file_uploader("Upload a file", accept_multiple_files=False,\
                                                                    type=("pcap", "pcapng"))
            filename = "data/test.pcap"
            if uploaded_file is not None:
                with open(filename, "wb") as f:
                                f.write(uploaded_file.getbuffer())
                # df = packetToCSV()
                pcap2CSV()
                df = pd.read_csv("data/testPacketToCSV.csv")
                st.write("Shape of the Dataframe is: ", df.shape)
                st.write("Here are the first ten rows of the File")
                st.table(df.head(10))
                file_details = {"FileName":uploaded_file.name,"FileType":uploaded_file.type,\
                                                            "FileSize":uploaded_file.size}
                st.sidebar.write(file_details)


    if function == "Select Method":
        method = st.sidebar.selectbox(
                    'Choose Prediction Method', ["Bayes Net", "Machine Learning"])
        if method == "Bayes Net":
            bayes_func = st.sidebar.selectbox(
                    'Choose Bayes Functionality', ["Set Initial Config", "Updated Belief"])
            if bayes_func == "Set Initial Config":
                real_network_initial_configuration()
            if bayes_func == "Updated Belief":
                bayes_net_update()

        if method == "Machine Learning":
            st_machine_learning()