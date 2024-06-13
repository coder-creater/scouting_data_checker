import pandas as pd
import requests as rq
import numpy as np

match_data = pd.read_csv('match_data.csv')

base_url = 'https://www.thebluealliance.com/api/v3'
auth_key = 'tzy7ZK1AIP6E8PRrPZ9FIm36ltQXABlHNbrBomNCQvvjWYOZsuwVjUHg9Pv2IRZg'
headers = {'X-TBA-Auth-Key': auth_key}
event_key = "2024casj"

#grabs all match keys in a given event
match_key_response = rq.get(base_url+f"/event/{event_key}/matches/keys", headers=headers)

#returns as JSON if no error thrown
def process(response):
    if response.status_code == 200:
        # Process the response data
        data = response.json()
        return data
    else:
        print(f"Error: {response.status_code}")
        #print(response.headers)

#initializes an empty list for the match keys
match_key_list = []
#turns it into a JSON
match_key_raw_list = process(match_key_response)
#adds all qual matches to the empty list
for i in range(len(match_key_raw_list)):
    if "qm" in match_key_raw_list[i]:
        match_key_list.append(match_key_raw_list[i])

#print(process(rq.get(base_url+f'/match/{event_key}_qm1', headers=headers))['alliances']['red']['team_keys'])

def listCheck(item, list1, list2):
    for i in range(len(list1)):
        if (item == list1[i]):
            return "red"
    for i in range(len(list2)):
        if (item == list2[i]):
            return "blue"

red_keys = process(rq.get(base_url+f'/match/{event_key}_qm1', headers=headers))['alliances']['red']['team_keys']
blue_keys = process(rq.get(base_url+f'/match/{event_key}_qm1', headers=headers))['alliances']['blue']['team_keys']
print(red_keys)
print(blue_keys)
team="frc"+str(match_data.at[1, 'TeamNumber'])

for i in range(len(match_data)):
    match_num = match_data.at[i, 'Match']
    red = process(rq.get(base_url+f'/match/{event_key}_qm{match_num}', headers=headers))['alliances']['red']['team_keys']
    blue = process(rq.get(base_url+f'/match/{event_key}_qm{match_num}', headers=headers))['alliances']['blue']['team_keys']
    team = "frc"+str(match_data.at[i, 'TeamNumber'])
    color = listCheck(team, red, blue)
    match_data.at[i, 'Alliance'] = color
    if (i==393):
        print(color)

match_data.to_csv('cleaned_data.csv', index=False)
print(match_data)