import pandas as pd
import requests as rq
import numpy as np
import functions as fn
import alliance_checker as ac

hblue = ac.hblue_spec
hred = ac.hred_spec
df = ac.df

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
    tnd = pd.DataFrame(index=range(len(t)), columns=range(len(ac.red_note_diff.columns)))
    tnd.columns = ac.red_note_diff.columns
    fn.zero_df(tnd)
    for i in range(len(t)):
        row = (df[(df['TeamNumber']==team) & (df['Match']==t[i])].index.tolist()[0])
        alliance = str(df.at[row, 'Alliance'])
        if (alliance == 'red'):
            for j in range(len(tnd.columns)):
                tnd.at[i, tnd.columns[j]] = ac.red_note_diff.at[t[i], tnd.columns[j]]
        elif (alliance == 'blue'):
                tnd.at[i, tnd.columns[j]] = ac.blue_note_diff.at[t[i], tnd.columns[j]]
    print(tnd)
    return fn.stats(tnd)

print('972')
print(team_checker(972))
print(team_stats(972))
print('1351')
print(team_checker(1351))
print(team_stats(1351))



#print(ac.df[(ac.df['TeamNumber']==1351) & (ac.df['Match']==3)].index.tolist()[0])
