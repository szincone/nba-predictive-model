#! python
# nba_player_stats_scraper.py - scrapes basketball-reference and turns into pandas dataframe
import requests
import bs4
import copy
import pandas as pd
import os
from dotenv import load_dotenv

# loading our environment variables
load_dotenv()

# url we're scraping
url_data = os.getenv("player_stats_url")

# getting our response
res = requests.get(url_data)
res.raise_for_status()  # raises exception if an issue with getting the url_data

# turning our response into soup
soup = bs4.BeautifulSoup(res.text, "html.parser")

# getting column headers for our data
column_headers = [th.getText() for th in
                  soup.findAll('tr', limit=1)[0].findAll('th')]

# getting data_rows (neccesary for getting player data)
data_rows = soup.findAll('tr')[1:]

# for some reason 'rank row' is in a 'tr' tag and all other data is in a 'td' tag,
# so delete the 'rank row' to get rid of the assertion error
column_headers.remove(column_headers[0])

# getting player data
player_data = [[td.getText() for td in data_rows[i].findAll('td')]
               for i in range(len(data_rows))]

# building our data frame
df_raw = pd.DataFrame(player_data, columns=column_headers)

# there are some blank columns with 'none' in them, so we'll get rid of them with notnull
df_raw = df_raw[df_raw.Player.notnull()]

# renaming columns for clarity
df_raw.rename(columns={'WS/48': 'WS-per-48',
                       'Player': 'Name', 'Tm': 'Team'}, inplace=True)

# replacing all column headers that have '%' with '-Perc' instead
df_raw.columns = df_raw.columns.str.replace('%', '-Perc')

# players who change teams show up more than once, we'll get the first entry from
# the table(which is there combined TOT stat) and drop the rest with drop_duplicates
df_raw = df_raw.drop_duplicates(['Name'], keep='first')

# argument convert_numeric changes types that have numbers to the most suitable type
df_raw = df_raw.apply(pd.to_numeric, errors='ignore')

# this gets rid of any NaN columns still left
df_raw = df_raw.dropna(axis=1, how='all')

# getting rid of any symbols that might be in the player names
df_raw['Name'] = df_raw['Name'].str.replace("\'|\\.", "")
df_raw['Name'] = df_raw['Name'].str.replace("\\-", " ")

# filtering by MP using quantile(65th)
mins_quan = df_raw.MP.quantile(q=.65)

# updating df by mins played
df = df_raw.loc[df_raw['MP'] >= mins_quan]

# PER sorted from highest to lowest
PER = df.sort_values('PER', axis=0, ascending=False)

# to avoid a 'SettingWithCopyWarning', make a deepcopy
nba_df = copy.deepcopy(df)

# making new column and weighting the equation
usage_weight = nba_df['USG-Perc'] * .5
rebound_weight = nba_df['TRB-Perc'] * .625  # rebounds = 1.25
assist_weight = nba_df['AST-Perc'] * .75  # assists = 1.5
steal_weight = nba_df['STL-Perc'] * 1  # steals = 2
block_weight = nba_df['BLK-Perc'] * 1  # blocks = 2
turn_over_weight = nba_df['TOV-Perc'] * .25  # turnovers = -.5

# adding new column using equation
nba_df['Z-Stat'] = ((usage_weight + rebound_weight + assist_weight +
                     steal_weight + block_weight) // turn_over_weight)

# filtering our player dataframe
nba_df = nba_df.loc[(nba_df['Z-Stat'] >= 10) & (
    nba_df['VORP'] > 0)].sort_values('Z-Stat', axis=0, ascending=False)

# renaming for export readability
player_df = nba_df
