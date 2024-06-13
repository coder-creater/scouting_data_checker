import pandas as pd
import requests as rq
import numpy as np
import functions as fn

#setup
df = pd.read_csv('csvs/cleaned_data.csv')
num_matches = int((len(df)+1)/6)

#actuals
red_actuals = pd.DataFrame(index=range(num_matches+1),columns=range(4))
red_actuals.columns = ['AutoAmps','AutoSpeaker','TeleopAmps','TeleopSpeaker']

blue_actuals = pd.DataFrame(index=range(num_matches+1),columns=range(4))
blue_actuals.columns = ['AutoAmps','AutoSpeaker','TeleopAmps','TeleopSpeaker']


for i in range(1, len(red_actuals)):
    mnum = int(i)
    match_data = fn.process(rq.get(fn.base_url+f'/match/{fn.event_key}_qm{mnum}', headers=fn.headers))
    #for red alliances
    red_actuals.at[i, "AutoAmps"] = match_data['score_breakdown']['red']['autoAmpNoteCount']
    red_actuals.at[i, "AutoSpeaker"] = match_data['score_breakdown']['red']['autoSpeakerNoteCount']
    red_actuals.at[i, "TeleopAmps"] = match_data['score_breakdown']['red']['teleopAmpNoteCount']
    red_actuals.at[i, "TeleopSpeaker"] = match_data['score_breakdown']['red']['teleopSpeakerNoteAmplifiedCount'] + match_data['score_breakdown']['red']['teleopSpeakerNoteCount']
    #for blue alliances
    blue_actuals.at[i, "AutoAmps"] = match_data['score_breakdown']['blue']['autoAmpNoteCount']
    blue_actuals.at[i, "AutoSpeaker"] = match_data['score_breakdown']['blue']['autoSpeakerNoteCount']
    blue_actuals.at[i, "TeleopAmps"] = match_data['score_breakdown']['blue']['teleopAmpNoteCount']
    blue_actuals.at[i, "TeleopSpeaker"] = match_data['score_breakdown']['blue']['teleopSpeakerNoteAmplifiedCount'] + match_data['score_breakdown']['blue']['teleopSpeakerNoteCount']

red_actuals['Sum'] = red_actuals.sum(axis=1)
blue_actuals['Sum'] = blue_actuals.sum(axis=1)

#totals
red_totals = pd.DataFrame(index=range(num_matches+1),columns=range(4))
red_totals.columns = ['AutoAmps','AutoSpeaker','TeleopAmps','TeleopSpeaker']
blue_totals = pd.DataFrame(index=range(num_matches+1),columns=range(4))
blue_totals.columns = ['AutoAmps','AutoSpeaker','TeleopAmps','TeleopSpeaker']

#sets all values of input df to be zero
fn.zero_df(red_totals)
fn.zero_df(blue_totals)

#sets 'totals' df to be incremented values of all notes scored in match for a given goal (AutoAmp, AutoSpeaker, TeleopAmp, TeleopSpeaker)
for i in range(len(df)):
  match_num = df.at[i, "Match"]
  for j in range(len(red_totals.columns)):
    if(df.at[i, "Alliance"]=='red'):
        red_totals.at[match_num, red_totals.columns[j]] += df.at[i, red_totals.columns[j]]
    else:
        blue_totals.at[match_num, blue_totals.columns[j]] += df.at[i, blue_totals.columns[j]]  
red_totals['Sum'] = red_totals.sum(axis=1)
blue_totals['Sum'] = blue_totals.sum(axis=1)

#to csvs
red_actuals.to_csv('csvs/red_actuals.csv')
blue_actuals.to_csv('csvs/blue_actuals.csv')
red_totals.to_csv('csvs/red_totals.csv')
blue_totals.to_csv('csvs/blue_totals.csv')