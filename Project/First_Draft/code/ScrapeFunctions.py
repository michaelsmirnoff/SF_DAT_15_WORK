# -*- coding: utf-8 -*-
"""
Created on Sat Aug  1 12:00:00 2015

@author: Nick Smirnov
"""


import requests # how python goes onto the internet!
from bs4 import BeautifulSoup # (version 4)
import unicodedata
import pandas as pd
import numpy as np
import csv

r = requests.get('http://www.basketball-reference.com/leagues/NBA_2015_advanced.html')
b = BeautifulSoup(r.text, "html.parser") 

attrs = b.find('tr').text
attrs = unicodedata.normalize('NFKD', attrs).encode('ascii','ignore')

attributes = attrs.split("\n")
#
new_attributes = [ 'season_end','Rk', 'player', 'Pos', 'Age', 'Tm', 'G', 'MP', 'PER', 'TS%', '3PAr', 'FTr', 'ORB%', 'DRB%', 'TRB%', 'AST%', 'STL%', 'BLK%', 'TOV%', 'USG%','blnk', 'OWS', 'DWS', 'WS', 'WS/48','blnk2','OBPM', 'DBPM', 'BPM', 'VORP']

col_u = ["season_end","Rk","player","pos","age","bref_team_id","g","gs","mp","fg","fga","fg_","x3p","x3pa","x3p_","x2p","x2pa","x2p_","efg_","ft","fta","ft_","orb","drb","trb","ast","stl","blk","tov","pf","pts"]
#get 2015 basic basketball attributes

year = 2015

def BasicStats(year):
    df = pd.DataFrame(columns = col_u)
    #df.reindex_axis()
    r = requests.get('http://www.basketball-reference.com/leagues/NBA_'+ str(year) +'_per_game.html')
    b = BeautifulSoup(r.text,"html.parser")
    players_basic = b.find_all('tr', attrs = {"class":"full_table"})
    for player in players_basic:
        player_bas_atts = player.find_all('td')
        player_bas_atts_list = []
        player_bas_atts_list.append(str(year))
        for att in player_bas_atts:
            player_bas_atts_list.append(str(att.text))
        df.loc[len(df)]=player_bas_atts_list
    return df
    
    
 
years = range(1980,2016)
#years = range(1980,1982)
basic_stats = pd.DataFrame()
for year in years:
    stats= BasicStats(year)
    basic_stats=basic_stats.append(stats)
#    
#stats2015 =BasicStats('2015')
#stats2015.head()


def AdvanceStats(year):
    df = pd.DataFrame(columns = new_attributes)
    #df.reindex_axis()
    r = requests.get('http://www.basketball-reference.com/leagues/NBA_'+ str(year) +'_advanced.html')
    b = BeautifulSoup(r.text,"html.parser")
    players_advance = b.find_all('tr', attrs = {"class":"full_table"})
    for player in players_advance:
        player_adv_atts = player.find_all('td')
        player_adv_atts_list = []
        player_adv_atts_list.append(str(year))
        for att in player_adv_atts:
            player_adv_atts_list.append(str(att.text))
        df.loc[len(df)]=player_adv_atts_list
    return df

#years = range(1980,2016)
years = range(1980,1982)
advanced_stats = pd.DataFrame()    
for year in years:
    advstats = AdvanceStats(year)
    advanced_stats = advanced_stats.append(advstats)



#Get rid of Asterisk on player names
advanced_stats['player'] = advanced_stats['player'].map(lambda x:x.strip('*'))
basic_stats['player'] = basic_stats['player'].map(lambda x:x.strip('*'))

#Create CSV
advanced_stats.to_csv('advanced_stats')

#Merge Basic stats and Advanced Stats
Stats=pd.merge(basic_stats,advanced_stats,how = "left", on = ['player', 'season_end'])

#Create CSV
Stats.to_csv('NBAStats.csv')

'''

May be able to ignore the rest




'''




#Get team-summary NBA data

import requests # how python goes onto the internet!
from bs4 import BeautifulSoup # (version 4)
#from BeautifulSoup import BeautifulSoup
help(requests.get)
r = requests.get('http://www.basketball-reference.com/leagues/NBA_1980.html#all_team_stats')

b = BeautifulSoup(r.text.replace('&nbsp;','').replace('&gt;','').encode('ascii','ignore')) # create a beautifulsoup object

b

#
col_tm = ["season_end","Team","player","pos","age","bref_team_id","g","gs","mp","fg","fga","fg_","x3p","x3pa","x3p_","x2p","x2pa","x2p_","efg_","ft","fta","ft_","orb","drb","trb","ast","stl","blk","tov","pf","pts"]
#
#
r = requests.get('http://www.basketball-reference.com/leagues/NBA_1980.html#all_team_stats')
b = BeautifulSoup(r.text, "html.parser") 

attrs = b.find('tr').text
attrs = unicodedata.normalize('NFKD', attrs).encode('ascii','ignore')

attributes = attrs.split("\n")





