# Extract Transform Load File for Data
# Thomas Evans-Barton
# GH: @tevans-barton

import pandas as pd
import os
import requests
import urllib
import json

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
    return df


def get_executives_table(team):
    #Want URL to have form https://www.pro-football-reference.com/teams/htx/executives.htm
    EXECUTIVE_URL_PREFIX = 'https://www.pro-football-reference.com/teams/'
    url = EXECUTIVE_URL_PREFIX + str(team) + '/executives.htm'
    #Gets the DataFrame from this website, 0 because there are multiple dataframes on this page
    df = pd.read_html(url)[0]
    #Drop some unnecessary columns
    df = df.drop(['Teams', 'Notes'], axis = 1)
    return df


def get_combine_table(year):
    #Want URL to have form https://nflcombineresults.com/nflcombinedata.php?year=2010&pos=&college=
    COMBINE_URL_PREFIX = 'https://nflcombineresults.com/nflcombinedata.php?year='
    url = COMBINE_URL_PREFIX + str(year) + '&pos=&college='
    #Gets the DataFrame from this website, 0 because there are multiple dataframes on this page
    df = pd.read_html(url)[0]
    df = df.drop(['Unnamed: 13', 'Unnamed: 14'], axis = 1)
    return df

def get_data(years, teams, outpath):
    #Check if the outpath exists, if not, make it
    if not os.path.exists(TOP_PATH + outpath):
    	os.mkdir(TOP_PATH + outpath)
    #Get draft data for each year
    for y in years:
        try:
            get_draft_table(y).to_csv(TOP_PATH + outpath + '/DRAFT_' + str(y) + '.csv')
        except urllib.error.HTTPError:
            print('No draft data for ' + str(y))
            pass
        try:
            get_combine_table(y).to_csv(TOP_PATH + outpath + '/COMBINE_' + str(y) + '.csv')
        except urllib.error.HTTPError:
            print('No combine data for ' + str(y))
            pass
    #Get executive data for each team
    for t in teams:
        try:
            get_executives_table(t).to_csv(TOP_PATH + outpath + '/EXECUTIVES_' + str(t).upper() + '.csv')
        except urllib.HTTPError:
            print('No executive data available for ' + str(t))
            pass
    return