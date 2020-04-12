import pandas as pd
import os
import requests
import urllib
import json
import re
import numpy as np
from glob import glob

TOP_PATH = os.environ['PWD']
MOST_RECENT_DRAFT = 2019

def clean_combine(df_passed):
    df = df_passed.copy()
    df.dropna(how = 'all', inplace = True)
    #Several columns have a 'missing value' entry of 9.99, so replace those with NaN
    df['40 Yard'] = df['40 Yard'].replace(9.99, value = np.nan)
    df['Shuttle'] = df['Shuttle'].replace(9.99, value = np.nan)
    df['3Cone'] = df['3Cone'].replace(9.99, value = np.nan)
    college_map = {
        'Frenso State' : 'Fresno State',
        'Southeast Louisiana' : 'Southeastern Louisiana',
        'Nevada Las Vegas' : 'UNLV',
        'Southern California' : 'USC'
    }
    df['College'] = df['College'].apply(lambda x : re.sub(r' \(.*\)', '', x) if isinstance(x, str) else x)
    df['College'] = df['College'].apply(lambda x : college_map[x] if x in college_map.keys() else x)
    return df


def clean_draft(df_passed):

    def clean_college_column(col):
        college_map = {
            'Ala-Birmingham' : 'Alabama-Birmingham',
            'Ark-Pine Bluff' : 'Arkansas-Pine Bluff',
            'BYU' : 'Brigham Young',
            'Boston Col.' : 'Boston College',
            'Concordia-StatePaul' : 'Concordia - St Paul',
            'Hobart' : 'Hobart & William Smith',
            'Kutztown Pennsylvania' : 'Kutztown',
            'LSU' : 'Louisiana State',
            'La-Monroe' : 'Louisiana-Monroe',
            'Middle Tenn. State' : 'Middle Tennessee State',
            'Missouri Western State' : 'Missouri Western',
            'NW Missouri State' : 'Northwest Missouri State',
            'NW State' : 'Northwestern State',
            'Prairie View' : 'Prairie View A&M',
            'S.F. Austin' : 'Stephen F. Austin',
            'SE Louisiana' : 'Southeastern Louisiana',
            'SE Missouri State' : 'Southeast Missouri State',
            'SMU' : 'Southern Methodist',
            'Southern Miss' : 'Southern Mississippi',
            'TCU' : 'Texas Christian',
            'Tenn-Chattanooga' : 'Tennessee-Chattanooga',
            'Tenn-Martin' : 'Tennessee-Martin',
            'The Citadel' : 'Citadel',
            'West. Carolina' : 'Western Carolina',
            'West. Illinois' : 'Western Illinois',
            'West. Michigan' : 'Western Michigan',
            'Louisiana' : 'Louisiana-Lafayette',
            'Charlotte' : 'North Carolina Charlotte'
        }
        col = col.apply(lambda x : x.replace('St.', 'State') if isinstance(x, str) else x)
        col = col.apply(lambda x : re.sub(r' \(.*\)', '', x) if isinstance(x, str) else x)
        col = col.apply(lambda x : x.replace('East.', 'Eastern') if isinstance(x, str) else x)
        col = col.apply(lambda x : college_map[x] if x in college_map.keys() else x)
        return col

    df = df_passed.copy()
    try:
        df['College/Univ'] = clean_college_column(df['College/Univ'])
    except KeyError:
        print('Error cleaning college info for ' + str(int(df['YEAR'][0])) + ' possibly due to draft not having happened yet')
        pass
    return df


def merge_draft_and_combine(draft_df, combine_df):
    #Merge two dataframes, include position to get past duplicate name issue
    full_df = draft_df.merge(combine_df, how = 'left', left_on = 'Player', right_on = 'Name')
    #Drop Redundant Columns
    #full_df = full_df.drop(['College', 'Name', 'POS', 'Year', 'Unnamed: 0_y', 'Unnamed: 0_x'], axis = 1, errors = 'ignore')
    #Make sure no data was lost
    #assert(len(full_df) == len(draft_df)), 'Lost data for ' + str(int(full_df['YEAR'][0]))
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
    df.rename({'Receiving Rec' : 'Rec'}, axis = 1, inplace = True)
    return df


def combine_and_clean_all_drafts():
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
    #If the directory to put it in (data/interim) doesn't exist, make it
    df = df.reset_index(drop = True)
    if not os.path.exists(TOP_PATH + '/data/interim'):
        os.mkdir(TOP_PATH + '/data/interim')
    #Create the CSV file from this dataframe
    df.to_csv(TOP_PATH + '/data/interim/ALL_DRAFTS_WITH_ATH_TESTING.csv', index = False)
    return df


def get_current_executives_and_clean(df_passed):
    df = df_passed.copy()
    #Get a list of all the current GMs
    curr_executives = df[df['To'] == MOST_RECENT_DRAFT]['Person'].values
    #Get a boolean list to find dataframe of current GMs, including where they've worked before
    executive_choices = df.apply(lambda x : x['Person'] in curr_executives, axis = 1)
    curr_executives_df = df[executive_choices]
    curr_executives_df = curr_executives_df.reset_index(drop = True)
    #Add in a feature that has list of years worked for each GM that will help with joining later
    curr_executives_df['Years Worked'] = curr_executives_df.apply(lambda x : list(range(x['From'], x['To'] + 1)), axis = 1)
    #If the directory to put it in (data/interim) doesn't exist, make it
    if not os.path.exists(TOP_PATH + '/data/interim'):
        os.mkdir(TOP_PATH + '/data/interim')
    #Create the CSV file from this dataframe
    curr_executives_df.to_csv(TOP_PATH + '/data/interim/CURRENT_EXECUTIVES.csv', index = False)
    return curr_executives_df


def combine_drafts_and_executives(full_draft_df, curr_execs_df):
    #Merge the full draft dataframe with the current executives dataframe based on team
    #This will result in a very large dataframe as each player will have a row for each GM of the team
    #they were drafted by
    df = full_draft_df.merge(curr_execs_df, how = 'inner', left_on = 'Tm', right_on = 'Teams')
    #Only keep draft picks for picks made by the GM during that time
    #This will get rid of any draft picks NOT made by a current GM
    df = df[[df.loc[x]['YEAR'] in df.loc[x]['Years Worked'] for x in range(len(df))]]
    #Drop unnecessary columns
    df.drop(['Years Worked', 'From', 'To_y', 'Teams', 'Titles'], axis = 1, inplace = True, errors = 'ignore')
    df.rename({'To_x' : 'Played To'}, axis = 1, inplace = True)
    if not os.path.exists(TOP_PATH + '/data/final'):
        os.mkdir(TOP_PATH + '/data/final')
    df.to_csv(TOP_PATH + '/data/final/EXECUTIVES_PICKS.csv', index = False)
    return df



