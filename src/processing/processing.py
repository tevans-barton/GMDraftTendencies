import pandas as pd
import os
import requests
import urllib
import json
import re
import numpy as np
from glob import glob

TOP_PATH = os.environ['PWD']
MOST_RECENT_DRAFT = 2020

def clean_combine(df_passed):
    df = df_passed.copy()
    #Info for David Long the Linebacker is incorrect in the dataset and needs to be manually fixed :(
    if 'David Long' in df['Player'].values:
        the_loc = df[(df['Player'] == 'David Long') & (df['Pos'] == 'LB')]['School'].index[0]
        df.loc[the_loc] = ['David Long', 'LB', 'West Virginia', '5-11', 227, np.nan, np.nan, 18, np.nan, np.nan, np.nan]
    #Convert height from strings of form ft-in into integers in inches
    df['Ht'] = df['Ht'].apply(lambda x : int(x.split('-')[0]) * 12 + int(x.split('-')[1]))
    #Replace the state abbreviation with the full word for continuity with draft data
    df['School'] = df['School'].apply(lambda x: x.replace('St.', 'State'))
    return df

def clean_draft(df_passed):
    df = df_passed.copy()
    college_map = {
        'Hobart' : 'Hobart & William Smith',
        'The Citadel' : 'Citadel',
        'Concordia-StatePaul (MN)' : 'Concordia (MN)',
        'Charleston (WV)' : 'Charleston',
        'S.F. Austin' : 'Stephen F. Austin',
        'West. Illinois' : 'Western Illinois',
        'NW Missouri State' : 'Northwest Missouri State',
        'Middle Tenn. State' : 'Middle Tennessee State',
        'Tenn-Martin' : 'Tennessee-Martin'
    }
    #Changing College data to match up with how combine has college inputted
    try:
        df['College/Univ'] = df['College/Univ'].apply(lambda x: x.replace('St.', 'State') if isinstance(x, str) else x)
        df['College/Univ'] = df['College/Univ'].apply(lambda x: college_map[x] if x in college_map.keys() else x)
        df['Pos'] = df['Pos'].replace({'DL' : 'DE', 'T' : 'OT', 'NT' : 'DT'})
        df = df.fillna({'Solo' : 0, 'Int' : 0, 'Sk' : 0, 'Passing Cmp' : 0, 'Passing Att' : 0, 'Passing Yds' : 0,
                'Passing Int' : 0, 'Rushing Att' : 0, 'Rushing Yds' : 0, 'Rushing TD' : 0, 'Receiving Rec' : 0, 
                'Receiving Yds' : 0, 'Receiving TD' : 0})
    except KeyError:
        print('Error cleaning draft info for ' + str(int(df['YEAR'][0])) + ', possibly due to draft not having happened yet')
        pass
    return df


def merge_draft_and_combine(draft_df, combine_df):
    #Merge two dataframes, include position to get past duplicate name issue
    full_df = draft_df.merge(combine_df, how = 'left', left_on = ['Player', 'College/Univ'], right_on = ['Player', 'School'])
    #Drop Redundant Columns
    full_df.drop(['Pos_y', 'School'], axis = 1, inplace = True)
    #Make sure no data was lost
    assert(len(full_df) == len(draft_df)), 'Lost data for ' + str(int(full_df['YEAR'][0]))
    return full_df


def clean_merged_dataframe(df_passed):
    df = df_passed.copy()
    team_dict = {
        'ARI' : 'Cardinals',
        'SFO' : '49ers',
        'NYJ' : 'Jets',
        'OAK' : 'Raiders',
        'TAM' : 'Buccaneers', 
        'NYG' : 'Giants',
        'JAX' : 'Jaguars',
        'DET' : 'Lions',
        'BUF' : 'Bills',
        'PIT' : 'Steelers',
        'CIN' : 'Bengals',
        'GNB' : 'Packers',
        'MIA' : 'Dolphins',
        'ATL' : 'Falcons',
        'WAS' : 'Redskins',
        'CAR' : 'Panthers',
        'MIN' : 'Vikings',
        'TEN' : 'Titans',
        'DEN' : 'Broncos',
        'PHI' : 'Eagles',
        'HOU' : 'Texans',
        'BAL' : 'Ravens',
        'LAC' : 'Chargers',
        'SEA' : 'Seahawks',
        'NWE' : 'Patriots', 
        'IND' : 'Colts',
        'CLE' : 'Browns',
        'NOR' : 'Saints',
        'KAN' : 'Chiefs',
        'DAL' : 'Cowboys',
        'LAR' : 'Rams',
        'CHI' : 'Bears',
        'STL' : 'Rams',
        'SDG' : 'Chargers'
    }
    #Want to make team names the same format as the executives table for later
    df['Tm'] = df['Tm'].map(team_dict)
    #Make names for columns more precise
    df.rename({'Receiving Rec' : 'Rec', 'Pos_x' : 'Pos'}, axis = 1, inplace = True)
    return df


def combine_and_clean_all_drafts():
    #Note: There should be 2544 rows in total (for years 2010 - 2019)
    #Get all of the paths to the draft CSVs
    draft_paths = np.sort(glob(TOP_PATH + '/data/raw/DRAFT_*.csv'))
    #Get all of the paths to the combine CSVs
    combine_paths = np.sort(glob(TOP_PATH + '/data/raw/COMBINE_*.csv'))
    #Make an initial empty dataframe to add on to
    df = pd.DataFrame()
    #Loop through all the dataframe paths
    for i in range(len(draft_paths)):
        total_df = pd.DataFrame()
        draft_df = pd.read_csv(draft_paths[i])
        draft_df = clean_draft(draft_df)
        combine_df = pd.read_csv(combine_paths[i])
        combine_df = clean_combine(combine_df)
        #Try except to merge_draft_and_combine, won't work for current year
        try:
            total_df = merge_draft_and_combine(draft_df, combine_df)
            total_df = clean_merged_dataframe(total_df)
            df = df.append(total_df)
        except:
            #-16 and -14 are to get the two files that couldn't merge, as opposed to full file paths
            print('Problem Merging ' + str(combine_paths[i][-16:]) + ' and ' + str(draft_paths[i][-14:]) + ' possibly due to lack of draft information')
            pass
    #If the directory to put it in (data/final) doesn't exist, make it
    df = df.reset_index(drop = True)
    if not os.path.exists(TOP_PATH + '/data/final'):
        os.mkdir(TOP_PATH + '/data/final')
    #Create the CSV file from this dataframe
    df.to_csv(TOP_PATH + '/data/final/ALL_DRAFTS_WITH_ATH_TESTING.csv', index = False)
    return df


def get_current_executives_and_clean():
    #Read in the raw executives data
    df = pd.read_csv(TOP_PATH + '/data/raw/EXECUTIVES.csv')
    #Get a list of all the current GMs
    curr_executives = df[df['To'] == MOST_RECENT_DRAFT - 1]['Person'].values
    #Get a boolean list to find dataframe of current GMs, including where they've worked before
    executive_choices = df.apply(lambda x : x['Person'] in curr_executives, axis = 1)
    curr_executives_df = df[executive_choices]
    curr_executives_df = curr_executives_df.reset_index(drop = True)
    #Add in a feature that has list of years worked for each GM that will help with joining later
    curr_executives_df['Years Worked'] = curr_executives_df.apply(lambda x : list(range(x['From'], x['To'] + 2)), axis = 1) #Might need to change this back to a +1 at some point
    #If the directory to put it in (data/interim) doesn't exist, make it
    if not os.path.exists(TOP_PATH + '/data/interim'):
        os.mkdir(TOP_PATH + '/data/interim')
    #Create the CSV file from this dataframe
    curr_executives_df.to_csv(TOP_PATH + '/data/interim/CURRENT_EXECUTIVES.csv', index = False)
    return curr_executives_df


def combine_drafts_and_executives():
    full_draft_df = combine_and_clean_all_drafts()
    curr_execs_df = get_current_executives_and_clean()
    #Merge the full draft dataframe with the current executives dataframe based on team
    #This will result in a very large dataframe as each player will have a row for each GM of the team
    #they were drafted by
    df = full_draft_df.merge(curr_execs_df, how = 'inner', left_on = 'Tm', right_on = 'Teams')
    #Only keep draft picks for picks made by the GM during that time
    #This will get rid of any draft picks NOT made by a current GM
    df = df[[df.loc[x]['YEAR'] in df.loc[x]['Years Worked'] for x in range(len(df))]]
    #Drop unnecessary columns
    df.drop(['Years Worked', 'From', 'To_y', 'Teams', 'Titles'], axis = 1, inplace = True, errors = 'ignore')
    df.rename({'Person' : 'GM'}, axis = 1, inplace = True)
    df.rename({'To_x' : 'Played To'}, axis = 1, inplace = True)
    if not os.path.exists(TOP_PATH + '/data/final'):
        os.mkdir(TOP_PATH + '/data/final')
    df = df[['GM', 'YEAR', 'Rnd', 'Pick', 'Tm', 'Player', 'Pos', 'Age', 'Played To', 
            'AP1', 'PB', 'St', 'G', 'Passing Cmp', 'Passing Att', 'Passing Yds', 'Passing TD',
            'Passing Int', 'Rushing Att', 'Rushing Yds', 'Rushing TD', 'Rec',
            'Receiving Yds', 'Receiving TD', 'Solo', 'Int', 'Sk', 'College/Univ',
            'Ht', 'Wt', '40yd', 'Vertical', 'Bench', 'Broad Jump', '3Cone',
            'Shuttle']].reset_index(drop = True)
    df.to_csv(TOP_PATH + '/data/final/EXECUTIVES_PICKS.csv', index = False)
    return df



