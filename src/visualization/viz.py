import pandas as pd
import os
import matplotlib.pyplot as plt
import re
import numpy as np
from glob import glob

TOP_PATH = os.environ['PWD']

def picks_by_round(GM_Name):
    curr_execs = pd.read_csv(TOP_PATH + '/data/final/EXECUTIVES_PICKS.csv')
    gm_df = curr_execs[curr_execs['GM'] == GM_Name].reset_index(drop = True)
    picks_by_round = gm_df[['Rnd', 'Pick']].groupby('Rnd').count()
    fig_1 = plt.figure()
    ax = plt.bar(picks_by_round.index, picks_by_round['Pick'])
    plt.xlabel('Round')
    plt.ylabel('Number of Picks')
    plt.title('{gm}\'s Picks as {team} GM'.format(gm = GM_Name, team = gm_df['Tm'].iloc[0]))
    plt.show()
    return

def picks_by_position(GM_Name):
    curr_execs = pd.read_csv(TOP_PATH + '/data/final/EXECUTIVES_PICKS.csv')
    gm_df = curr_execs[curr_execs['GM'] == GM_Name].reset_index(drop = True)
    picks_by_round = gm_df[['Pos', 'Pick']].groupby('Pos').count()
    fig_1 = plt.figure()
    ax = plt.bar(picks_by_round.index, picks_by_round['Pick'])
    plt.xlabel('Position')
    plt.ylabel('Number of Picks')
    plt.title('{gm}\'s Picks as {team} GM'.format(gm = GM_Name, team = gm_df['Tm'].iloc[0]))
    plt.show()
    return

def picks_by_year(GM_Name):
    curr_execs = pd.read_csv(TOP_PATH + '/data/final/EXECUTIVES_PICKS.csv')
    gm_df = curr_execs[curr_execs['GM'] == GM_Name].reset_index(drop = True)
    picks_by_year = gm_df[['YEAR', 'Pick']].groupby('YEAR').count()
    fig_1 = plt.figure()
    ax = plt.bar(picks_by_year.index.astype(str), picks_by_year['Pick'])
    plt.xlabel('Year')
    plt.ylabel('Number of Picks')
    plt.title('{gm}\'s Picks as {team} GM'.format(gm = GM_Name, team = gm_df['Tm'].iloc[0]))
    plt.show()
    return
