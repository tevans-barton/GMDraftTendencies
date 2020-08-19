import pandas as pd
import os
import matplotlib.pyplot as plt
import re
import numpy as np
from glob import glob

TOP_PATH = os.environ['PWD']

def picks_by_round(GM_Name = False):
    #Put this conditional here so if GM_Name not passed, makes visualization for all picks
    if not GM_Name:
        #Read in data of all picks
        all_picks = pd.read_csv(TOP_PATH + '/data/final/ALL_DRAFTS_WITH_ATH_TESTING.csv')
        #Groupby to find number of picks by round
        picks_by_round = all_picks[['Rnd', 'Pick']].groupby('Rnd').count()
        #Plot the picks by round
        fig_1 = plt.figure()
        ax = plt.bar(picks_by_round.index, picks_by_round['Pick'])
        plt.xlabel('Round')
        plt.ylabel('Number of Picks')
        plt.title('All Picks by Round')
        plt.show()
        return
    #If GM_Name passed, read in the picks with the executives attached
    curr_execs = pd.read_csv(TOP_PATH + '/data/final/EXECUTIVES_PICKS.csv')
    #Select only the picks of the GM that is passed
    gm_df = curr_execs[curr_execs['GM'] == GM_Name].reset_index(drop = True)
    #Groupby to find number of picks by round
    picks_by_round = gm_df[['Rnd', 'Pick']].groupby('Rnd').count()
    #Plot the picks by round
    fig_1 = plt.figure()
    ax = plt.bar(picks_by_round.index, picks_by_round['Pick'])
    plt.xlabel('Round')
    plt.ylabel('Number of Picks')
    plt.title('{gm}\'s Picks as GM by Round'.format(gm = GM_Name))
    plt.show()
    return

def picks_by_position(GM_Name = False):
    #Put this conditional here so if GM_Name not passed, makes visualization for all picks
    if not GM_Name:
        #Read in data of all picks
        all_picks = pd.read_csv(TOP_PATH + '/data/final/ALL_DRAFTS_WITH_ATH_TESTING.csv')
        #Groupby to find number of picks by position
        picks_by_pos = all_picks[['Pos', 'Pick']].groupby('Pos').count()
        #Plot the picks by position
        fig_1 = plt.figure()
        ax = plt.bar(picks_by_pos.index, picks_by_pos['Pick'])
        plt.xlabel('Position')
        plt.ylabel('Number of Picks')
        plt.title('All Picks by Position')
        plt.show()
        return
    #If GM_Name passed, read in the picks with the executives attached
    curr_execs = pd.read_csv(TOP_PATH + '/data/final/EXECUTIVES_PICKS.csv')
    #Select only the picks of the GM that is passed
    gm_df = curr_execs[curr_execs['GM'] == GM_Name].reset_index(drop = True)
    #Groupby to find number of picks by position
    picks_by_pos = gm_df[['Pos', 'Pick']].groupby('Pos').count()
    #Plot the picks by position
    fig_1 = plt.figure()
    ax = plt.bar(picks_by_pos.index, picks_by_pos['Pick'])
    plt.xlabel('Position')
    plt.ylabel('Number of Picks')
    plt.title('{gm}\'s Picks as GM by Position'.format(gm = GM_Name))
    plt.show()
    return

def picks_by_year(GM_Name):
    #Read in the picks with the executives attached
    curr_execs = pd.read_csv(TOP_PATH + '/data/final/EXECUTIVES_PICKS.csv')
    #Select only the picks of the GM that is passed
    gm_df = curr_execs[curr_execs['GM'] == GM_Name].reset_index(drop = True)
    #Groupby to find number of picks by year
    picks_by_year = gm_df[['YEAR', 'Pick']].groupby('YEAR').count()
    #Plot the picks by year
    fig_1 = plt.figure()
    ax = plt.bar(picks_by_year.index.astype(str), picks_by_year['Pick'])
    plt.xlabel('Year')
    plt.ylabel('Number of Picks')
    plt.title('{gm}\'s Picks as GM by Year'.format(gm = GM_Name))
    plt.show()
    return

def picks_by_age(GM_Name = False):
    #Put this conditional here so if GM_Name not passed, makes visualization for all picks
    if not GM_Name:
        #Read in data of all picks
        all_picks = pd.read_csv(TOP_PATH + '/data/final/ALL_DRAFTS_WITH_ATH_TESTING.csv')
        #Groupby to find number of picks by age
        picks_by_age = all_picks[['Age', 'Pick']].groupby('Age').count()
        #Plot the picks by age
        fig_1 = plt.figure()
        ax = plt.bar(picks_by_age.index, picks_by_age['Pick'])
        plt.xlabel('Age')
        plt.ylabel('Number of Picks')
        plt.title('All Picks by Age')
        plt.show()
        return
    #If GM_Name passed, read in the picks with the executives attached
    curr_execs = pd.read_csv(TOP_PATH + '/data/final/EXECUTIVES_PICKS.csv')
    #Select only the picks of the GM that is passed
    gm_df = curr_execs[curr_execs['GM'] == GM_Name].reset_index(drop = True)
    #Groupby to find number of picks by age
    picks_by_pos = gm_df[['Age', 'Pick']].groupby('Age').count()
    #Plot the picks by age
    fig_1 = plt.figure()
    ax = plt.bar(picks_by_pos.index, picks_by_pos['Pick'])
    plt.xlabel('Age')
    plt.ylabel('Number of Picks')
    plt.title('{gm}\'s Picks as GM by Age'.format(gm = GM_Name))
    plt.show()
    return

def forty_by_pos(GM_Name = False):
    #Put this conditional here so if GM_Name not passed, makes visualization for all picks
    if not GM_Name:
        #Read in data of all picks
        all_picks = pd.read_csv(TOP_PATH + '/data/final/ALL_DRAFTS_WITH_ATH_TESTING.csv')
        #Groupby to find mean forty by position
        forty_by_pos = all_picks[['Pos', '40yd']].groupby('Pos').mean()
        #Plot the forty times by position
        fig_1 = plt.figure()
        ax = plt.bar(forty_by_pos.index, forty_by_pos['40yd'])
        plt.xlabel('Position')
        plt.ylabel('Mean Forty Time')
        plt.ylim(4, 5.75)
        plt.title('All Picks Forty Times by Position')
        plt.show()
        return
    #If GM_Name passed, read in the picks with the executives attached
    curr_execs = pd.read_csv(TOP_PATH + '/data/final/EXECUTIVES_PICKS.csv')
    #Select only the picks of the GM that is passed
    gm_df = curr_execs[curr_execs['GM'] == GM_Name].reset_index(drop = True)
    #Groupby to find median forty by position
    forty_by_pos = gm_df[['Pos', '40yd']].groupby('Pos').mean()
    #Plot the picks by age
    fig_1 = plt.figure()
    ax = plt.bar(forty_by_pos.index, forty_by_pos['40yd'])
    plt.xlabel('Position')
    plt.ylabel('Mean Forty Time')
    plt.ylim(4, 5.75)
    plt.title('{gm}\'s Picks as GM by Age'.format(gm = GM_Name))
    plt.show()
    return
