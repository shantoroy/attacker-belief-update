import pandas as pd
import numpy as np
import random

# possible operating systems
os_dict = {
    "windows": ["Win 7", "Win Server 2008"],
    "linux": ["Red Hat 8", "Ubuntu 20.04"]
}

# possible applications
app_dict = {
    "server": ["Apache", "IIS"],
    "browser": ["Chrome", "Firefox"]
}


def windows_node_creation(num_of_windows):
    win_machine_list = []
    for i in range(num_of_windows):
        conf = []
        conf.append(np.random.randint(110,129))
        conf.append(8192)
        conf.append(random.choice(os_dict["windows"]))
        if conf[2] == "Win Server 2008":
            conf.append(random.choice(app_dict["server"]))
        else:
            conf.append(random.choice(app_dict["browser"]))
        win_machine_list.append(conf)
    return win_machine_list


def linux_node_creation(num_of_linux):
    linux_machine_list = []
    for i in range(num_of_linux):
        conf = []
        conf.append(np.random.randint(50,65))
        conf.append(5840)
        conf.append(random.choice(os_dict["linux"]))
        if conf[2] == "Red Hat 8":
            conf.append("Apache")
        else:
            conf.append(random.choice(app_dict["browser"]))
        linux_machine_list.append(conf)
    return linux_machine_list
    

def network_creation(win, linux):
    # use functions to create Windows and Linux nodes
    win_machine_list = windows_node_creation(win)
    df_win = pd.DataFrame(win_machine_list, columns = ['TTL', 'WS', 'OS', 'App']) 
    linux_machine_list = linux_node_creation(linux)
    df_linux = pd.DataFrame(linux_machine_list, columns = ['TTL', 'WS', 'OS', 'App']) 

    # combine both lists to create the network
    network = pd.concat([df_win, df_linux], axis=0)
    network.reset_index(inplace= True, drop=True)
    return network

