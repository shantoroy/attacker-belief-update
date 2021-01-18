import pandas as pd
import numpy as np
import random

# Windows
def windows_kb():
    win_ttl = np.array(range(100,129))
    win_ws = 8192

    win_kb = pd.DataFrame(columns=['ttl', 'ws', 'probability'])
    for i in range(len(win_ttl)):
        temp = pd.DataFrame([[win_ttl[i], win_ws, None]], columns=['ttl', 'ws', 'probability'])
        win_kb = win_kb.append(temp)

    win_kb.reset_index(inplace= True, drop=True)

    win_kb.loc[(win_kb['ttl'] > 125) & (win_kb['ttl'] < 129), 'probability'] = 0.99
    win_kb.loc[(win_kb['ttl'] > 120) & (win_kb['ttl'] < 126), 'probability'] = 0.97
    win_kb.loc[(win_kb['ttl'] > 99) & (win_kb['ttl'] < 121), 'probability'] = 0.95
    return win_kb


# linux
def linux_kb():
    lin_ttl = np.array(range(50,65))
    lin_ws = 5840

    lin_kb = pd.DataFrame(columns=['ttl', 'ws', 'probability'])
    for i in range(len(lin_ttl)):
        temp = pd.DataFrame([[lin_ttl[i], lin_ws, None]], columns=['ttl', 'ws', 'probability'])
        lin_kb = lin_kb.append(temp)

    lin_kb.reset_index(inplace= True, drop=True)

    lin_kb.loc[(lin_kb['ttl'] > 60) & (lin_kb['ttl'] < 65), 'probability'] = 0.99
    lin_kb.loc[(lin_kb['ttl'] > 54) & (lin_kb['ttl'] < 61), 'probability'] = 0.97
    lin_kb.loc[(lin_kb['ttl'] > 49) & (lin_kb['ttl'] < 55), 'probability'] = 0.95
    return lin_kb