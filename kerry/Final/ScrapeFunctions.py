# -*- coding: utf-8 -*-
"""
Created on Sat Mar  7 22:32:55 2015

@author: MindKontrol
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

col_u = ["season_end","Rk","player","pos","age","bref_team_id","g","gs","mp","fg","fga","fg_","x3p","x3pa","x3p_","x2p","x2pa","x2p_","ft","fta","ft_","orb","drb","trb","ast","stl","blk","tov","pf","pts"]
#get 2015 basic basketball attributes

year = 2015

def BasicStats(year):
    df = pd.DataFrame(columns = col_u)
    #df.reindex_axis()
    r =requests.get('http://www.basketball-reference.com/leagues/NBA_'+ str(year) +'_per_game.html')
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
 
years = range(1952,2016)
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

years = range(1951,2016)
advanced_stats = pd.DataFrame()    
for year in years:
    advstats = AdvanceStats(year)
    advanced_stats = advanced_stats.append(advstats)



#Get rid of Asterisk on player names
advanced_stats['player'] = advanced_stats['player'].map(lambda x:x.strip('*'))

#Create CSV
advanced_stats.to_csv('advanced_stats')

#Merge Basic stats and Advanced Stats
CurrentStats=pd.merge(stats,advstats,how = "left", on = ['player', 'season_end'])

#Create CSV
CurrentStats.to_csv('CurrentYearStats')

#Get historic all-nba team data

import requests # how python goes onto the internet!
from bs4 import BeautifulSoup # (version 4)
#from BeautifulSoup import BeautifulSoup
help(requests.get)
r = requests.get('http://www.basketball-reference.com/awards/all_league.html')


b = BeautifulSoup(r.text.replace('&nbsp;','').replace('&gt;','').encode('ascii','ignore')) # create a beautifulsoup object

b

b.prettify()




all_league_data = pd.DataFrame(columns = ['year','team','player']) # Create an empty data frame

stw_list = b.findAll('div', attrs={'class': 'stw'}) # Find all 'stw's'
for stw in stw_list:
	year = str(stw.find('table', attrs = {'class':'no_highlight wide_table'})['data-mobile-header']) # Get the year
	teams = stw.findAll('td', attrs = {'class':'mobile_text'}) # Get all of the teams:  1st, 2nd, 3rd
	for team in teams:
		team_level = str(team.find('h3').text) # Get the team level
		players = team.findAll('td') # Find all of the players in each team
		for player in players:
			player_name = str(player.find('a').text) # Get the player names
			all_league_data.loc[len(all_league_data)] = [year, team_level, player_name] # Write the row to the data frame

all_league_data # The new data frame
#b.find_all('td',attrs = {'class':'mobile_text'}) Gives me teams, and td class where rows are located but cant see rows in td class 
 


season = []
league= []
for seas in all_league_data.year:
    a,b = seas.split(" ")
    league.append(b)
    #print league
    a,c = a.split("-")
    #print c
    e = (seas[0:2]+ c)
    new_year = a +"-"+ e
    season.append(new_year)


y2k = []
for ne in season:
    a = ne.replace('1999-1900','1999-2000')
    y2k.append(a)

all_league_data.year =y2k
#Addleague to dataset
all_league_data['league'] = league

#Only have NBA data statistics not other leagues
#now remove all values not equal to NBA
NBA= all_league_data[all_league_data.league=='NBA']

#create season variable
NBA['season']= NBA.year


del NBA['year']
del NBA['league']


season_end = [int(sea[-4:]) for sea in NBA.season]

NBA['season_end'] = season_end

NBA.to_csv('All_Team_Data.csv')






