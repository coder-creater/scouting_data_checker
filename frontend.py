from nicegui import ui
import pandas as pd
import requests as rq
import numpy as np
import functions as fn
import team_checker as tc



def get_num_correct(team):
    num_correct.text = str(tc.team_checker(int(team)))
    total_correct.text = str(len(tc.team_checker(int(team))))+'/'+str(len(tc.team_matches(int(team))))+' correct'

def get_data(team):
    df = tc.team_stats(int(team))
    titles = df.index
    df.insert(0, 'Titles', titles)
    team_stats.from_pandas(df)
    print(tc.team_stats(int(team)))

z = ui.input(label="Team", value='boo')
q = ui.label().bind_text_from(z, 'value')
ui.button('Number Of Corectly Scouted Matches', on_click=lambda: get_num_correct(z.value))
num_correct = ui.label('none')
total_correct = ui.label('__ correct')
ui.button('Team Data', on_click=lambda: get_data(z.value))
team_stats = ui.table(columns='', rows='')


ui.run()
