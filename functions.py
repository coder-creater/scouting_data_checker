import pandas as pd
import requests as rq
import numpy as np

def zero_df(df):
    for i in range(len(df)):
        for j in range(len(df.columns)):
            df.at[i,df.columns[j]] = 0

def process(response):
    if response.status_code == 200:
        # Process the response data
        data = response.json()
        return data
    else:
        print(f"Error: {response.status_code}")
        #print(response.headers)

base_url = 'https://www.thebluealliance.com/api/v3'
auth_key = 'tzy7ZK1AIP6E8PRrPZ9FIm36ltQXABlHNbrBomNCQvvjWYOZsuwVjUHg9Pv2IRZg'
headers = {'X-TBA-Auth-Key': auth_key}
event_key = "2024casj"

def note_diff(num_matches, df1, df2):
    note_diff = pd.DataFrame(index=range(num_matches),columns=range(5))
    zero_df(note_diff)
    note_diff.columns = ['AutoAmps','AutoSpeaker','TeleopAmps','TeleopSpeaker','Sum']
    for i in range(1, len(df1)):
        for j in range(len(note_diff.columns)):
            dn = (abs(df1.at[i, note_diff.columns[j]]-df2.at[i, note_diff.columns[j]]))
            note_diff.at[i, note_diff.columns[j]] = dn

    return note_diff

def percent_error(num_matches, df1, df2):
    note_diff = pd.DataFrame(index=range(num_matches),columns=range(5))
    zero_df(note_diff)
    note_diff.columns = ['AutoAmps','AutoSpeaker','TeleopAmps','TeleopSpeaker','Sum']
    for i in range(1, len(df1)):
        for j in range(len(note_diff.columns)):
            dn = (abs(df1.at[i, note_diff.columns[j]]-df2.at[i, note_diff.columns[j]]))
            if df2.at[i, note_diff.columns[j]] == 0:
                note_diff.at[i, note_diff.columns[j]] = dn*100
            else:
                note_diff.at[i, note_diff.columns[j]] = (dn/df2.at[i, note_diff.columns[j]])*100
    
    return note_diff

def hund_count(num, df1, df2, col):
    hunds = []
    note_diff = pd.DataFrame(index=range(num),columns=range(len(df1.columns)))
    note_diff.columns = df1.columns
    for i in range(1, len(df1)):
        if (df1.at[i,col]==df2.at[i,col]):
            hunds.append(i)
    return hunds

def hund_spec(num, df1, df2, col):
    hunds = []
    note_diff = pd.DataFrame(index=range(num),columns=range(len(df1.columns)))
    note_diff.columns = df1.columns
    for i in range(1, len(df1)):
        if (df1.at[i,col]==df2.at[i,col]):
            if ((df1.at[i, df1.columns[1]]==df2.at[i, df2.columns[1]]) and (df1.at[i, df1.columns[1]]==df2.at[i, df2.columns[1]]) and (df1.at[i, df1.columns[3]]==df2.at[i, df2.columns[3]]) and (df1.at[i, df1.columns[4]]==df2.at[i, df2.columns[4]])):
                hunds.append(i)
    return hunds




def stats(df):
        #creates a df for the final data, then averages, medians, and stds the values
    final_data = pd.DataFrame(index=range(len(df.columns)),columns=['Avg','Med','STD'])
    final_data.index = df.columns
    for i in range(len(df.columns)):
        avg = round(np.mean(df[df.columns[i]]),3)
        med = round(np.median(df[df.columns[i]]),3)
        std = round(np.std(df[df.columns[i]]), 3)
        final_data.at[final_data.index[i],'Avg'] = avg
        final_data.at[final_data.index[i],'Med'] = med
        final_data.at[final_data.index[i],'STD'] = std
    
    return final_data

red_actuals = pd.read_csv('csvs/red_actuals.csv') 
blue_actuals = pd.read_csv('csvs/blue_actuals.csv')
red_totals = pd.read_csv('csvs/red_totals.csv') 
blue_totals = pd.read_csv('csvs/blue_totals.csv')
