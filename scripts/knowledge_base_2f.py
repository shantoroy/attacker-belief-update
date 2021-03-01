import pandas as pd
import numpy as np
import random


def kb(win_ttl, win_ws):
    win_kb = pd.DataFrame(columns=['ip.ttl', 'tcp.window_size', 'probability'])
    for i in range(len(win_ttl)):
        temp = pd.DataFrame([[win_ttl[i], win_ws, None]], columns=['ip.ttl', 'tcp.window_size', 'probability'])
        win_kb = win_kb.append(temp)
    for i in range(len(win_ttl)):
        temp = pd.DataFrame([[win_ttl[i], None, None]], columns=['ip.ttl', 'tcp.window_size', 'probability'])
        win_kb = win_kb.append(temp)
    temp = pd.DataFrame([[None, win_ws, None]], columns=['ip.ttl', 'tcp.window_size', 'probability'])
    win_kb = win_kb.append(temp)
    temp = pd.DataFrame([[None, None, None]], columns=['ip.ttl', 'tcp.window_size', 'probability'])
    win_kb = win_kb.append(temp)

    win_kb.reset_index(inplace= True, drop=True)
# (min(win_ttl)-)  (max(win_ttl)+1)
    win_kb.loc[(win_kb['ip.ttl'] >= min(win_ttl)) & (win_kb['ip.ttl'] <= max(win_ttl))\
                                & (win_kb['tcp.window_size'].isnull()), 'probability'] = 0.24
    win_kb.loc[(win_kb['ip.ttl'] >= min(win_ttl)) & (win_kb['ip.ttl'] <= max(win_ttl))\
                                & (win_kb['tcp.window_size'] == win_ws), 'probability'] = 0.5
    win_kb.loc[(win_kb['ip.ttl'].isnull()) & (win_kb['tcp.window_size'] == win_ws), 'probability'] = 0.24
    win_kb.loc[(win_kb['ip.ttl'].isnull()) & (win_kb['tcp.window_size'].isnull()), 'probability'] = 0.02
    return win_kb


# Windows
def windows_6_kb():
    ttl = np.array(range(120,129))
    ws = 8192
    df_kb = kb(ttl, ws)
    return df_kb



def windows_5_kb():
    ttl = np.array(range(120,129))
    ws = 65535
    df_kb = kb(ttl, ws)
    return df_kb


# linux
def linux_kb():
    ttl = np.array(range(55,65))
    ws = 5840
    df_kb = kb(ttl, ws)
    return df_kb

def bsd_kb():
    ttl = np.array(range(55,65))
    ws = 65535
    df_kb = kb(ttl, ws)
    return df_kb

def gl_kb():
    ttl = np.array(range(55,65))
    ws = 5720
    df_kb = kb(ttl, ws)
    return df_kb


# router
# def cisco_kb():
#     ttl = np.array(range(250,256))
#     ws = 4128
#     df = 0
#     df_kb = kb(ttl, ws)
#     return df_kb



def create_knowledge_base():
    win_6_kb = windows_6_kb()
    win_5_kb = windows_5_kb()
    lin_kb = linux_kb()
    bsdl_kb = bsd_kb()
    gll_kb = gl_kb()
    # ciscol_kb = cisco_kb()

    win_6_kb.to_csv("data/f2_win_6_kb.csv")
    win_5_kb.to_csv("data/f2_win_5_kb.csv")
    lin_kb.to_csv("data/f2_lin_kb.csv")
    bsdl_kb.to_csv("data/f2_bsd_kb.csv")
    gll_kb.to_csv("data/f2_gl_kb.csv")
    # ciscol_kb.to_csv("data/f2_cisco_kb.csv")


create_knowledge_base()