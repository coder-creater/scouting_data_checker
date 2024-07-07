import pandas as pd
import requests as rq
import numpy as np
import functions as fn
df = pd.read_csv('csvs/cleaned_data.csv') 
num_matches = int((len(df)+1)/6)

red_actuals = pd.read_csv('csvs/red_actuals.csv') 
blue_actuals = pd.read_csv('csvs/blue_actuals.csv')
red_totals = pd.read_csv('csvs/red_totals.csv') 
blue_totals = pd.read_csv('csvs/blue_totals.csv') 

red_note_diff = fn.note_diff(num_matches, red_totals, red_actuals)
blue_note_diff = fn.note_diff(num_matches, blue_totals, blue_actuals)
hblue = fn.hund_count(num_matches, blue_totals, blue_actuals, 'Sum')
hred = fn.hund_count(num_matches, red_totals, red_actuals, 'Sum')

def team_matches(team):
    teamList = []
    for i in range(len(df)):
        if (team == df.at[i, 'TeamNumber']):
            teamList.append(df.at[i, 'Match'])
    return teamList

def contains(num, list):
    for i in range(len(list)):
        if (num == list[i]):
            return True

tko = team_matches(1351)

def team_checker(team):
    t = team_matches(team)
    correct = []
    for i in range(len(t)):
        alliance = str(df.at[(df[(df['TeamNumber']==team) & (df['Match']==t[i])].index.tolist()[0]), 'Alliance'])
        if (alliance == 'red'):
            if(contains(t[i], hred)):
                correct.append(t[i])
        elif (alliance == 'blue'):
            if(contains(t[i], hblue)):
                correct.append(t[i])
    return correct

def team_stats(team):
    t = team_matches(team)
    tnd = pd.DataFrame(index=range(len(t)), columns=range(len(red_note_diff.columns)))
    tnd.columns = red_note_diff.columns
    fn.zero_df(tnd)
    for i in range(len(t)):
        row = (df[(df['TeamNumber']==team) & (df['Match']==t[i])].index.tolist()[0])
        alliance = str(df.at[row, 'Alliance'])
        if (alliance == 'red'):
            for j in range(len(tnd.columns)):
                tnd.at[i, tnd.columns[j]] = red_note_diff.at[t[i], tnd.columns[j]]
        elif (alliance == 'blue'):
                tnd.at[i, tnd.columns[j]] = blue_note_diff.at[t[i], tnd.columns[j]]
    return fn.stats(tnd)

def al_notes_stats(color):
    red_diff = fn.note_diff(num_matches, red_totals, red_actuals)
    blue_diff = fn.note_diff(num_matches, blue_totals, blue_actuals)
    if color == 'red':
        return fn.stats(red_diff)
    elif color == 'blue':
        return fn.stats(blue_diff)

def al_percent_stats(color):
    red_diff = fn.percent_error(num_matches, red_totals, red_actuals)
    blue_diff = fn.percent_error(num_matches, blue_totals, blue_actuals)
    if color == 'red':
        return fn.stats(red_diff)
    elif color == 'blue':
        return fn.stats(blue_diff)

print(al_percent_stats('red'))


#print(ac.df[(ac.df['TeamNumber']==1351) & (ac.df['Match']==3)].index.tolist()[0])
