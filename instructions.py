import streamlit as st

def st_instruction_page():
    st.markdown("# Adversarial Belief Update")
    st.info("> _This app creates a network and helps visualizing the attacker's\
            belief update_")

    st.markdown("## Step-by-Step Guide")
    st.markdown("1. Create a Network")
    st.markdown("2. Input Attacker's Initial Belief Parameters")
    st.markdown("3. Create Observations for Individual Node")
    st.markdown("4. See Belief Update (Plot/Table)")
    st.markdown("")
    st.markdown("")

    st.markdown("### Create a Network")
    st.markdown("A network will be created once you do the followings:")
    st.markdown("* Choose Functionality -> Create Network")
    st.markdown("* Input the Number of Windows Nodes")
    st.markdown("* Input the Number of Linux Nodes")
    st.markdown("* Choose the Plot/Table View of the Network")
    st.markdown("")
    st.markdown("")

    st.markdown("### Input Attacker's Initial Belief Parameters")
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

    st.markdown("### Create Observations for Individual Node")
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

    st.markdown("### See Belief Update (Plot/Table)")
    st.markdown("You can see the belief update process using plots/tables")
    st.markdown("* Choose Functionality -> Node Belief Update")
    st.markdown("* Choose a Node")
    st.markdown("* Check the Real configuration")
    st.markdown("* Choose Functionality -> Updated Belief Info")
    st.markdown("* Choose between plot/table")
    st.markdown("")
    st.markdown("")

    