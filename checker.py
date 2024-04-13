import pandas as pd
import requests as rq

df = pd.read_csv('match_data.csv') 
pd.set_option('future.no_silent_downcasting', True)

num_matches = 66

totals = pd.DataFrame(index=range(num_matches+1),columns=range(4))
totals.columns = ['AutoAmps','AutoSpeaker','TeleopAmps','TeleopSpeaker']

def zero_df(df):
    for i in range(len(df)):
        for j in range(len(df.columns)):
            totals.at[i,df.columns[j]] = 0
zero_df(totals)

for i in range(len(df)):
  match_num = df.at[i, "Match"]
  for j in range(len(totals.columns)):
    totals.at[match_num, totals.columns[j]] += df.at[i, totals.columns[j]]
#print(totals)

base_url = 'https://www.thebluealliance.com/api/v3'
auth_key = 'tzy7ZK1AIP6E8PRrPZ9FIm36ltQXABlHNbrBomNCQvvjWYOZsuwVjUHg9Pv2IRZg'
headers = {'X-TBA-Auth-Key': auth_key}
event_key = "2024casj"

match_key_response = rq.get(base_url+f"/event/{event_key}/matches/keys", headers=headers)

match_data = rq.get(base_url+"/match/2024cafr_qm3", headers=headers)

def process(response):
    if response.status_code == 200:
        # Process the response data
        data = response.json()
        return data
    else:
        print(f"Error: {response.status_code}")
        #print(response.headers)

match_key_list = []
match_key_raw_list = process(match_key_response)
for i in range(len(match_key_raw_list)):
    if "qm" in match_key_raw_list[i]:
        match_key_list.append(match_key_raw_list[i])

actuals = pd.DataFrame(index=range(match_num+1),columns=range(4))
actuals.columns = ['AutoAmps','AutoSpeaker','TeleopAmps','TeleopSpeaker']


for i in range(1, len(actuals)):
    mnum = int(i)
    match_data = process(rq.get(base_url+f'/match/{event_key}_qm{mnum}', headers=headers))
    actuals.at[i, "AutoAmps"] = match_data['score_breakdown']['blue']['autoAmpNoteCount'] + match_data['score_breakdown']['red']['autoAmpNoteCount']
    actuals.at[i, "AutoSpeaker"] = match_data['score_breakdown']['blue']['autoSpeakerNoteCount'] + match_data['score_breakdown']['red']['autoSpeakerNoteCount']
    actuals.at[i, "TeleopAmps"] = match_data['score_breakdown']['blue']['teleopAmpNoteCount'] + match_data['score_breakdown']['red']['teleopAmpNoteCount']
    actuals.at[i, "TeleopSpeaker"] = match_data['score_breakdown']['blue']['teleopSpeakerNoteAmplifiedCount'] + match_data['score_breakdown']['blue']['teleopSpeakerNoteCount'] + match_data['score_breakdown']['red']['teleopSpeakerNoteAmplifiedCount'] + match_data['score_breakdown']['red']['teleopSpeakerNoteCount']


#print(process(match_data)['match_number'])
print(actuals)
print(totals)