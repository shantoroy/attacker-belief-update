import streamlit as st

def st_instruction_page():
    st.markdown("# Adversarial Belief Update")
    st.info("> _This app can fingerprint Operating Systems using Bayes Net and Machine \
                Learning as well as can simulate an Attacker's Intuition (Belief Update) \
                inside a compromised network_")

    st.info(
    """
    ## Primary Features: 
    1. Real-life OS Fingerprinting using:
        * Bayes Network-based Knowledge Base
        * Multi-Class Classification Algorithms
    2. Simulated Visualization of Node belief updates
    3. Simulation of the updated belief for all nodes in a network
    """)


    st.markdown(
        """
        ## Real-Life OS Fingerprinting
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
        """
    )
    


    

    st.markdown("#### Input Attacker's Initial Belief Parameters")
    st.markdown("The attacker requires an initial set of Operating Systems (OS)\
                and an initial set of installed applications (App). Initial \
                Configuration set is achieved by $O X P(A)$ where $O$ is the \
                set of OS, and $A$ is the set of applications. $P(A)$ is the powerset\
                of $A$.")
    st.markdown("2 operating systems, and 2 applications are recommended (total config=8)")
    st.markdown("* Choose Functionality -> Initial Belief Config")
    st.markdown("* Choose operating systems")
    st.markdown("* Choose installed applications")
    st.markdown("")
    st.markdown("")

    st.markdown("#### Create Observations for Individual Node")
    st.markdown("While creating observation for a network node, you can choose observations\
                based on the real configuration (regular network) or you can choose\
                observations based on different configurations (deceptive network).")
    st.markdown("Perform the following Steps:")
    st.markdown("* Choose Functionality -> Node Belief Update")
    st.markdown("* Choose a Node")
    st.markdown("* Check the Real configuration")
    st.markdown("* Choose Functionality -> Create Observation")
    st.markdown("* Checkmark configurations (OS/App) you want")
    st.markdown("* Input the number of observations")
    st.markdown("")
    st.markdown("")

    st.markdown("#### See Belief Update (Plot/Table)")
    st.markdown("You can see the belief update process using plots/tables")
    st.markdown("* Choose Functionality -> Node Belief Update")
    st.markdown("* Choose a Node")
    st.markdown("* Check the Real configuration")
    st.markdown("* Choose Functionality -> Updated Belief Info")
    st.markdown("* Choose between plot/table")
    st.markdown("")
    st.markdown("")

    