import pandas as pd
import requests as rq
import numpy as np
df = pd.read_csv('csvs/cleaned_data.csv')
num_matches = int((len(df)+1)/6)


for i in range(1, 20):
    mn = df.at[i, 'Match']
    tn = df.at[i, 'TeamNumber']
    mb = df.at[i, 'AutoLeave']
    df = df.at[i, 'TeamNumber']
    sp = df.at[i, 'TeamNumber']
    aus = df.at[i, 'AutoSpeaker']
    aa = df.at[i, 'AutoAmps']
    cr = df.at[i, 'AutoMiddle']
    ts = df.at[i, 'TeleopSpeaker']
    ta = df.at[i, 'TeleopAmps']
    eg = df.at[i, 'TeamNumber']
    t = df.at[i, 'TeamNumber']
    h = df.at[i, 'TeamNumber']
    gp = df.at[i, 'TeamNumber']
    f = df.at[i, 'TeamNumber']
    p = df.at[i, 'TeamNumber']
    tp = df.at[i, 'TeamNumber']
    n = df.at[i, 'TeamNumber']
    fl = open(f'match{mn}_teamCal.txt', 'w')
    file = """YOURNAME: Cal
    TEAMNUM: 3491
    MATCHNUM_TEAMNUM: 7_3491
    MATCHNUM: 7
    MOBILITY: true
    DEFENDING: false
    STARTINGPOS: 1
    AUTONSPEAKER: 0
    AUTONAMP: 0
    CENTERRING: false
    TELEOPSPEAKER: 0
    TELEOPAMP: 0
    ENDGAME: None
    TRAP: false
    HARMONY: false
    GROUNDPICKUP: false
    FEEDER: false
    PENALTIES: 0
    TECHPENALTIES: 0
    NOTES: 
    """
    fl.write(file)
    fl.close()