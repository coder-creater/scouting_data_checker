import pandas as pd
import requests as rq
import numpy as np
import functions as fn

df = pd.read_csv('match_data.csv') 
pd.set_option('future.no_silent_downcasting', True)

num_matches = 66

totals = pd.DataFrame(index=range(num_matches+1),columns=range(4))
totals.columns = ['AutoAmps','AutoSpeaker','TeleopAmps','TeleopSpeaker']

#sets all values of input df to be zero
fn.zero_df(totals)

#sets 'totals' df to be incremented values of all notes scored in match for a given goal (AutoAmp, AutoSpeaker, TeleopAmp, TeleopSpeaker)
for i in range(len(df)):
  match_num = df.at[i, "Match"]
  for j in range(len(totals.columns)):
    totals.at[match_num, totals.columns[j]] += df.at[i, totals.columns[j]]
#print(totals)

#setup for accessing the API
base_url = 'https://www.thebluealliance.com/api/v3'
auth_key = 'tzy7ZK1AIP6E8PRrPZ9FIm36ltQXABlHNbrBomNCQvvjWYOZsuwVjUHg9Pv2IRZg'
headers = {'X-TBA-Auth-Key': auth_key}
event_key = "2024casj"

#grabs all match keys in a given event
match_key_response = rq.get(base_url+f"/event/{event_key}/matches/keys", headers=headers)

#initializes an empty list for the match keys
match_key_list = []
#turns it into a JSON
match_key_raw_list = fn.process(match_key_response)
#adds all qual matches to the empty list
for i in range(len(match_key_raw_list)):
    if "qm" in match_key_raw_list[i]:
        match_key_list.append(match_key_raw_list[i])

#initializes an empty df for the actual values
actuals = pd.DataFrame(index=range(match_num+1),columns=range(4))
actuals.columns = ['AutoAmps','AutoSpeaker','TeleopAmps','TeleopSpeaker']

#grabs all actual totals from the API
for i in range(1, len(actuals)):
    mnum = int(i)
    match_data = fn.process(rq.get(base_url+f'/match/{event_key}_qm{mnum}', headers=headers))
    actuals.at[i, "AutoAmps"] = match_data['score_breakdown']['blue']['autoAmpNoteCount'] + match_data['score_breakdown']['red']['autoAmpNoteCount']
    actuals.at[i, "AutoSpeaker"] = match_data['score_breakdown']['blue']['autoSpeakerNoteCount'] + match_data['score_breakdown']['red']['autoSpeakerNoteCount']
    actuals.at[i, "TeleopAmps"] = match_data['score_breakdown']['blue']['teleopAmpNoteCount'] + match_data['score_breakdown']['red']['teleopAmpNoteCount']
    actuals.at[i, "TeleopSpeaker"] = match_data['score_breakdown']['blue']['teleopSpeakerNoteAmplifiedCount'] + match_data['score_breakdown']['blue']['teleopSpeakerNoteCount'] + match_data['score_breakdown']['red']['teleopSpeakerNoteAmplifiedCount'] + match_data['score_breakdown']['red']['teleopSpeakerNoteCount']

#creates new columns with the sum of ALL notes scored in a match, from both alliances
totals['Sum'] = totals.sum(axis=1)
actuals['Sum'] = actuals.sum(axis=1)

#empty array for percent diff (up or down matters)
perc_match_total = []
#empty array for percent diff (up or down doesn't matter)
perc_match_diff = []
#idk why i have the above two honestly
#initializes an empty df for the difference of notes in each category
note_diff = pd.DataFrame(index=range(num_matches),columns=range(5))
fn.zero_df(note_diff)
note_diff.columns = ['AutoAmps','AutoSpeaker','TeleopAmps','TeleopSpeaker','Sum']
#empty list for the matches that were scored 100% correctly
hund_match =[]
#calculates the percent diff and the number of notes diff
for i in range(1, len(totals)):
    pc = (totals.at[i, 'Sum'])/(actuals.at[i, 'Sum'])
    dpc = (abs(1.0-pc))
    for j in range(len(note_diff.columns)):
        dn = (abs(totals.at[i, note_diff.columns[j]]-actuals.at[i, note_diff.columns[j]]))
        note_diff.at[i, note_diff.columns[j]] = dn
    perc_match_total.append(pc)  
    perc_match_diff.append(dpc)
    if pc == 1.0:
        hund_match.append(i)

#creates a df for the final data, then averages, medians, and stds the values
final_data = pd.DataFrame(index=["AutoAmps",'AutoSpeaker','TeleopAmp','TeleopSpeaker','Total'],columns=['Avg','Med','STD'])
for i in range(len(note_diff.columns)):
    avg = np.mean(note_diff[note_diff.columns[i]])
    med = np.median(note_diff[note_diff.columns[i]])
    std = np.std(note_diff[note_diff.columns[i]])
    final_data.at[final_data.index[i],'Avg'] = avg
    final_data.at[final_data.index[i],'Med'] = med
    final_data.at[final_data.index[i],'STD'] = std

#prints values
print("Average compared to 1.0: " + str(np.mean(perc_match_total)))
print("Std compared to 1.0: " + str(np.std(perc_match_total)))
print("Average difference in .%. compared to 1.0: " + str(np.mean(perc_match_diff)))
print("Std of diff in .%. compared to 1.0: " + str(np.std(perc_match_diff)))
print("Percent of matches scouted 100%: " + str((len(hund_match)/num_matches)))
print("")
print("Note-based data:")
print(final_data)