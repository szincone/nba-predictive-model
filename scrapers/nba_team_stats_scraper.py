#! python
# nba_team_stats_scraper.py - scrapes basketball-reference and turns into pandas dataframe
import requests
import bs4
import pandas as pd
import os
from dotenv import load_dotenv

# loading our environment variables
load_dotenv()

# url we're scraping
url_data = os.getenv("team_stats_url")

# getting our response
res = requests.get(url_data)
res.raise_for_status()  # raises exception if an issue with getting the url_data

# turning our response into soup
soup = bs4.BeautifulSoup(res.text, "html.parser")

# getting column headers for our data
column_headers = [th.getText() for th in
                  soup.findAll('tr', limit=2)[1].findAll('th')]

# getting data_rows (neccesary for getting player data)
data_rows = soup.findAll('tr')[1:]

# for some reason 'rank row' is in a 'tr' tag and all other data is in a 'td' tag, so delete the 'rank row' to get rid of the assertion error
column_headers.remove(column_headers[0])

# getting player data
team_data = [[td.getText() for td in data_rows[i].findAll('td')]
             for i in range(len(data_rows))]

# building our data frame
df = pd.DataFrame(team_data[1:], columns=column_headers)

# renaming columns for clarity
df.rename(columns={'ORtg/A': 'Off-Rat-Adj', 'DRtg/A': 'Def-Rat-Adj', 'NRtg/A': 'Net-Rat-Adj',
                   'MOV/A': 'MOV-Adj', 'NRtg': 'Net-Rat', 'DRtg': 'Def-Rat', 'ORtg': 'Off-Rat',
                   'W/L%': 'W-L-Per'}, inplace=True)


# convert data to number type
df = df.apply(pd.to_numeric, errors='ignore')

# this gets rid of any NaN columns still left
df = df.dropna(axis=1, how='any')
