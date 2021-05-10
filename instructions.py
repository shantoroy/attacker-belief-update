import streamlit as st

def st_instruction_page():
        st.markdown("# Adversarial Belief Update")
        st.info(
        """
        > _This app can fingerprint Operating Systems using Bayes Net and Machine \
        Learning as well as can simulate an Attacker's Intuition (Belief Update) \
        inside a compromised network_
        """
        )

        st.info(
        """
        ## Primary Features: 
        1. Real-life OS Fingerprinting using:
            * Bayes Network-based Knowledge Base
            * Multi-Class Classification Algorithms
        2. Simulated Visualization of Node belief updates
        3. Simulation of the updated belief for all nodes in a network
        """
        )


        st.markdown(
        """
        ## Real-Life OS Fingerprinting

        ### Step-by-Step Guide
        1. Upload your data. Supports the following types of data:
            * network packet file (e.g., **test.pcap**)
            * converted CSV file from PCAP files. You can install `tshark` and use the following code

            ```
            $ tshark -r input.pcap -T fields -E header=y -E separator=, -E quote=d -E occurrence=f \ 
            -e ip.version -e ip.hdr_len -e ip.tos -e ip.id -e ip.flags -e ip.flags.rb -e ip.flags.df \ 
            -e ip.flags.mf -e ip.frag_offset -e ip.ttl -e ip.proto -e ip.checksum -e ip.src -e ip.dst \ 
            -e ip.len -e ip.dsfield -e tcp.srcport -e tcp.dstport -e tcp.seq -e tcp.ack -e tcp.len \ 
            -e tcp.hdr_len -e tcp.flags -e tcp.flags.fin -e tcp.flags.syn -e tcp.flags.reset \ 
            -e tcp.flags.push -e tcp.flags.ack -e tcp.flags.urg -e tcp.flags.cwr -e tcp.window_size \ 
            -e tcp.checksum -e tcp.urgent_pointer -e tcp.options.mss_val > output.csv
            ```
        2. Select Any Model: Bayes Network or Machine Learning 
            * Bayes Net
                - Select Initial Configuration (Windows, Linux, or macOS)
                - Select Updated Belief Info (wait and find all node predictions)
            * Machine Learning
                - Select any of the following multi-class Classification Algorithms
                    * Logistic Regression
                    * K-Nearest Neighbor 
                    * SVM (RBF) Classifier
                    * Naive Bayes Classifier
                    * Decision Tree Classifier
                    * Random Forest Classifier
        """
        )

        st.markdown(
        """
        ## Simulated Visualization of Node belief updates

        ### Step-by-Step Guide
        1. Create a Network
        2. Input Attacker's Initial Belief Parameters
        3. Create Observations for Individual Node
        4. See Belief Update (Plot/Table)

        #### Create a Network
        A network will be created once you do the followings:
        * Choose Functionality -> Create Network
        * Input the Number of Windows Nodes
        * Input the Number of Linux Nodes
        * Choose the Plot/Table View of the Network

        #### Input Attacker's Initial Belief Parameters
        The attacker requires an initial set of Operating Systems (OS)\
        and an initial set of installed applications (App). Initial \
        Configuration set is achieved by $O X P(A)$ where $O$ is the \
        set of OS, and $A$ is the set of applications. $P(A)$ is the powerset\
        of $A$.

        2 operating systems, and 2 applications are recommended (total config=8)
        * Choose Functionality -> Initial Belief Config
        * Choose operating systems
        * Choose installed applications



        #### Create Observations for Individual Node
        While creating observation for a network node, you can choose observations\
        based on the real configuration (regular network) or you can choose\
        observations based on different configurations (deceptive network).

        Perform the following Steps:
        * Choose Functionality -> Node Belief Update
        * Choose a Node
        * Check the Real configuration
        * Choose Functionality -> Create Observation
        * Checkmark configurations (OS/App) you want
        * Input the number of observations



        #### See Belief Update (Plot/Table)
        You can see the belief update process using plots/tables
        * Choose Functionality -> Node Belief Update
        * Choose a Node
        * Check the Real configuration
        * Choose Functionality -> Updated Belief Info
        * Choose between plot/table

        """
        )



        st.markdown(
        """
        ## Simulated Network Prediction

        ### Step-by-Step Guide
        1. Create Observations
            * Select No. of nodes 
            * Select No. of observations
        2. Input Attacker's Initial Belief Parameters (as before)
        3. See Belief Update (Table for all nodes respectively)
        """
        )







