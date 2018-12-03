#! python
# model.py - combines basketball-reference scraper data (team and player) into 1 dataframe
from scrapers.nba_player_stats_scraper import player_df
from scrapers.nba_team_stats_scraper import team_df
import os
import sys
import random
import pandas as pd

# nba dict object
nba_dictionary = {
    'Golden State Warriors': 'GSW',
    'San Antonio Spurs': 'SAS',
    'Houston Rockets': 'HOU',
    'Los Angeles Clippers': 'LAC',
    'Utah Jazz': 'UTA',
    'Toronto Raptors': 'TOR',
    'Cleveland Cavaliers': 'CLE',
    'Boston Celtics': 'BOS',
    'Washington Wizards': 'WAS',
    'Oklahoma City Thunder': 'OKC',
    'Memphis Grizzlies': 'MEM',
    'Miami Heat': 'MIA',
    'Denver Nuggets': 'DEN',
    'Charlotte Hornets': 'CHO',
    'Chicago Bulls': 'CHI',
    'Portland Trail Blazers': 'POR',
    'Milwaukee Bucks': 'MIL',
    'Indiana Pacers': 'IND',
    'Minnesota Timberwolves': 'MIN',
    'Atlanta Hawks': 'ATL',
    'Detroit Pistons': 'DET',
    'New Orleans Pelicans': 'NOP',
    'Dallas Mavericks': 'DAL',
    'Sacramento Kings': 'SAC',
    'New York Knicks': 'NYK',
    'Phoenix Suns': 'PHO',
    'Philadelphia 76ers': "PHI",
    'Los Angeles Lakers': 'LAL',
    'Brooklyn Nets': 'BRK',
    'Orlando Magic': 'ORL',
}
