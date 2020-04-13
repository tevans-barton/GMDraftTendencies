# Extract Transform Load File for Data
# Thomas Evans-Barton
# GH: @tevans-barton

import pandas as pd
import os
import requests
import urllib
import json
import numpy as np

TOP_PATH = os.environ['PWD']

def get_draft_table(year):
    #Want URL to have form 'https://www.pro-football-reference.com/years/2019/draft.htm'
    DRAFT_URL_PREFIX = 'https://www.pro-football-reference.com/years/'
    url = DRAFT_URL_PREFIX + str(year) + '/draft.htm'
    #Gets the DataFrame from this website, 0 because there are multiple dataframes on this page
    df = pd.read_html(url)[0]
    #Dropping link to college stats column
    df = df.drop('Unnamed: 28_level_0', axis = 1, errors = 'ignore')
    #Changing column names to more normal form and dropping multi-column index
    col_names = []
    for col in df.columns:
        if 'Unnamed' in col[0] or 'Misc' in col[0]:
            col_names.append(str(col[1]))
        else:    
            col_names.append(str(col[0]) + ' ' + str(col[1]))
    df.columns = col_names
    #Since data on website is broken up by round, 'Pick' appears as a value in the column
    #Except for years where draft has not occurred yet
    try:
        df = df[df['Pick'] != 'Pick']
    except KeyError:
        print('No picks for ' + str(year))
        pass
    #Want a column in the table with the year for easier merging later
    df['YEAR'] = [year] * len(df)
    return df


def get_executives_table(team):
    #Want URL to have form https://www.pro-football-reference.com/teams/htx/executives.htm
    EXECUTIVE_URL_PREFIX = 'https://www.pro-football-reference.com/teams/'
    url = EXECUTIVE_URL_PREFIX + str(team) + '/executives.htm'
    #Gets the DataFrame from this website, 0 because there are multiple dataframes on this page
    df = pd.read_html(url)[0]
    #Drop some unnecessary columns
    df = df.drop(['Notes'], axis = 1)
    return df


def get_combine_table(year):
    #Want URL to have form https://www.pro-football-reference.com/draft/2020-combine.htm
    COMBINE_URL_PREFIX = 'https://www.pro-football-reference.com/draft/'
    url = COMBINE_URL_PREFIX + str(year) + '-combine.htm'
    #Gets the DataFrame from this website, 0 because there are multiple dataframes on this page
    df = pd.read_html(url)[0]
    df.drop(['College', 'Drafted (tm/rnd/yr)'], axis = 1, inplace = True)
    #Get rid of extra header rows
    df = df[df['Player'] != 'Player']
    return df


def get_data(years, teams, outpath):
    #Check if the outpath exists, if not, make it
    if not os.path.exists(TOP_PATH + outpath):
    	os.mkdir(TOP_PATH + outpath)
    #Get draft data for each year
    for y in years:
        try:
            get_draft_table(y).to_csv(TOP_PATH + outpath + '/DRAFT_' + str(y) + '.csv', index = False)
        except urllib.error.HTTPError:
            print('No draft data for ' + str(y))
            pass
        try:
            get_combine_table(y).to_csv(TOP_PATH + outpath + '/COMBINE_' + str(y) + '.csv', index = False)
        except urllib.error.HTTPError:
            print('No combine data for ' + str(y))
            pass
    #Get executive data for each team and put it into one table
    executives_table = pd.DataFrame()
    for t in teams:
        try:
            executives_table = executives_table.append(get_executives_table(t))
        except urllib.HTTPError:
            print('No executive data available for ' + str(t))
            pass
    executives_table = executives_table.reset_index(drop = True)
    executives_table.to_csv(TOP_PATH + outpath + '/EXECUTIVES.csv', index = False)
    return