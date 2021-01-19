import pandas as pd
import numpy as np
import random

# Windows
def windows_kb():
    win_ttl = np.array(range(120,129))
    win_ws = 8192

    win_kb = pd.DataFrame(columns=['ttl', 'ws', 'probability'])
    for i in range(len(win_ttl)):
        temp = pd.DataFrame([[win_ttl[i], win_ws, None]], columns=['ttl', 'ws', 'probability'])
        win_kb = win_kb.append(temp)
    for i in range(len(win_ttl)):
        temp = pd.DataFrame([[win_ttl[i], None, None]], columns=['ttl', 'ws', 'probability'])
        win_kb = win_kb.append(temp)
    temp = pd.DataFrame([[None, win_ws, None]], columns=['ttl', 'ws', 'probability'])
    win_kb = win_kb.append(temp)
    temp = pd.DataFrame([[None, None, None]], columns=['ttl', 'ws', 'probability'])
    win_kb = win_kb.append(temp)

    win_kb.reset_index(inplace= True, drop=True)

    win_kb.loc[(win_kb['ttl'] > 119) & (win_kb['ttl'] < 129) \
                                & (win_kb['ws'].isnull()), 'probability'] = 0.24
    win_kb.loc[(win_kb['ttl'] > 119) & (win_kb['ttl'] < 129) \
                                & (win_kb['ws'] == win_ws), 'probability'] = 0.5
    win_kb.loc[(win_kb['ttl'].isnull()) & (win_kb['ws'] == win_ws), 'probability'] = 0.24
    win_kb.loc[(win_kb['ttl'].isnull()) & (win_kb['ws'].isnull()), 'probability'] = 0.02

    return win_kb


# linux
def linux_kb():
    lin_ttl = np.array(range(58,65))
    lin_ws = 5840

    lin_kb = pd.DataFrame(columns=['ttl', 'ws', 'probability'])
    for i in range(len(lin_ttl)):
        temp = pd.DataFrame([[lin_ttl[i], lin_ws, None]], columns=['ttl', 'ws', 'probability'])
        lin_kb = lin_kb.append(temp)
    for i in range(len(lin_ttl)):
        temp = pd.DataFrame([[lin_ttl[i], None, None]], columns=['ttl', 'ws', 'probability'])
        lin_kb = lin_kb.append(temp)
    temp = pd.DataFrame([[None, lin_ws, None]], columns=['ttl', 'ws', 'probability'])
    lin_kb = lin_kb.append(temp)
    temp = pd.DataFrame([[None, None, None]], columns=['ttl', 'ws', 'probability'])
    lin_kb = lin_kb.append(temp)

    lin_kb.reset_index(inplace= True, drop=True)

    lin_kb.loc[(lin_kb['ttl'] > 57) & (lin_kb['ttl'] < 65) \
                                & (lin_kb['ws'].isnull()), 'probability'] = 0.24
    lin_kb.loc[(lin_kb['ttl'] > 57) & (lin_kb['ttl'] < 65) \
                                & (lin_kb['ws'] == lin_ws), 'probability'] = 0.5
    lin_kb.loc[(lin_kb['ttl'].isnull()) & (lin_kb['ws'] == lin_ws), 'probability'] = 0.24
    lin_kb.loc[(lin_kb['ttl'].isnull()) & (lin_kb['ws'].isnull()), 'probability'] = 0.02

    return lin_kb


def create_knowledge_base():
    win_kb = windows_kb()
    lin_kb = linux_kb()
    win_kb.to_csv("win_kb.csv")
    lin_kb.to_csv("lin_kb.csv")


create_knowledge_base()