# -*- coding: utf-8 -*-
"""
Created on Sat Aug  1 12:00:00 2015

@author: Nick Smirnov

Original code was written by MindKontrol.  The basis of the original work was written by MindKontrol to extract nominal & advanced player data.  I included for a way to scrape for initial rookie season information.
"""

#Library for all execution
import requests # how python goes onto the internet!
from bs4 import BeautifulSoup # (version 4)
import unicodedata
import pandas as pd
import numpy as np
import csv

#attributes
new_attributes = [ 'season_end','Rk', 'player', 'Pos', 'Age', 'Tm', 'G', 'MP', 'PER', 'TS%', '3PAr', 'FTr', 'ORB%', 'DRB%', 'TRB%', 'AST%', 'STL%', 'BLK%', 'TOV%', 'USG%','blnk', 'OWS', 'DWS', 'WS', 'WS/48','blnk2','OBPM', 'DBPM', 'BPM', 'VORP']

col_u = ["season_end","Rk","player","pos","age","bref_team_id","g","gs","mp","fg","fga","fg_","x3p","x3pa","x3p_","x2p","x2pa","x2p_","efg_","ft","fta","ft_","orb","drb","trb","ast","stl","blk","tov","pf","pts"]

debut_attributes = ["season_end","Rk","player","age","yrs","g","mp","fg","fga","x3p","x3pa","ft","fta","orb","trb","ast","stl","blk","tov","pf","pts","fg_","3p_","ft_","MP","PTS","TRB","AST"]

#Functions
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

def Debut(year):
    df = pd.DataFrame(columns = debut_attributes)
    #df.reindex_axis()
    r = requests.get('http://www.basketball-reference.com/leagues/NBA_'+ str(year) +'_debut.html')
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

#Define data & run extract of Basketball reference    
years = range(1978,2016)

basic_stats = pd.DataFrame()
for year in years:
    stats= BasicStats(year)
    basic_stats=basic_stats.append(stats)

advanced_stats = pd.DataFrame()    
for year in years:
    advstats = AdvanceStats(year)
    advanced_stats = advanced_stats.append(advstats)

Debuts = pd.DataFrame()   
for year in years:
    debut = Debut(year)
    Debuts = Debuts.append(debut)

#Get rid of Asterisk on player names
# Strip * from player names
advanced_stats['player'] = advanced_stats['player'].map(lambda x:x.strip('*'))
basic_stats['player'] = basic_stats['player'].map(lambda x:x.strip('*'))
Debuts['player'] = Debuts['player'].map(lambda x:x.strip('*'))

#Merge Basic stats and Advanced Stats
NBA_Stats=pd.merge(basic_stats,advanced_stats,how = "left", on = ['player', 'season_end'])


del NBA_Stats['Pos']
del NBA_Stats['Age']
del NBA_Stats['Tm']
del NBA_Stats['G']
del NBA_Stats['blnk']
del NBA_Stats['blnk2']

    
Debuts = Debuts[['season_end','player','age']]

#Create exp column

NBA_Stats['exp'] = -1

#Create exclusive player list
player_names = set(NBA_Stats['player'])

len(player_names)
#2776 total players
player_names = list(player_names)
sorted_players = sorted(player_names, key = lambda x: x.split(' ')[-1])

#players who entered the league since 1976
#2725
len(Debuts['player'][Debuts.season_end >= 1976])
#players who entered the league since 1978
#2566
len(Debuts['player'][Debuts.season_end >= 1978])

inclusive_player_names = Debuts['player'][Debuts.season_end >= 1978]
len(inclusive_player_names)


#attempt to modify Exp values
for row_index in range(NBA_Stats.shape[0]):
    row = NBA_Stats.ix[row_index:row_index]
    if len(set(row['player']) & set(inclusive_player_names)):
        try:
            first_year = int(Debuts[Debuts.player ==list(row['player'])[0]]['season_end'])
            row['exp'] = row['season_end'] - first_year
        except:
            pass

#Create CSVs
file_name = 'C:\Users\Nick\Desktop\GA\SF_DAT_15_WORK\Project\First_Draft\data\NBAStats.csv'
NBA_Stats.to_csv(file_name,index=True)

file_name = 'C:\Users\Nick\Desktop\GA\SF_DAT_15_WORK\Project\First_Draft\data\Debut.csv'
Debuts.to_csv('Debut.csv',index=False)

file_name = 'C:\Users\Nick\Desktop\GA\SF_DAT_15_WORK\Project\First_Draft\data\2015_Rookies.csv'
NBA_Rookies = NBA_Stats[(NBA_Stats.exp == 0) & (NBA_Stats.season_end == 2015)]
NBA_Rookies.to_csv(file_name,index=False)



#Columns of Data Frames
NBA_Stats.columns
Debuts.columns



#stats
NBA_Stats[NBA_Stats.player == 'Glen Rice Jr'][['player','season_end','exp','PER']]

#Fill Nulls

NBA_Stats.isnull().sum()

#to fix:
#fg_, x3p_. x2p_, efg_, ft_, PER, TS%, 3PAr, FTr, ORB%, DRB%, TRB%, AST%, STL%, BLK%, TOV%, USG%, WS/48
# FIXED:
#
#
'''
titanic_data['Age'] = titanic_data.groupby("Sex").transform(lambda x: x.fillna(x.mean()))['Age'] 
'''

#
#drop players
#
NBAT = NBA_Stats

NBAT.drop(NBAT[NBAT.player == 'George Johnson'].index, axis=0)
NBAT[NBAT.player == 'David Stockton']

#remove players with -1 or less Exp
NBA_Remove = NBAT.drop([NBAT.exp < 0].index, axis=0)
NBAT = NBA_Remove

NBA_Remove = NBAT.drop(NBAT[(NBAT.exp == 0) & (NBAT.season_end == 2015)].index, axis=0)
NBAT = NBA_Remove

file_name = 'C:\Users\Nick\Desktop\GA\SF_DAT_15_WORK\Project\First_Draft\data\NBAStats.csv'
NBAT.to_csv(file_name,index=False)
#NBA_Rookies = NBAT[(NBAT.exp == 0) & (NBAT.season_end == 2015)]

player_names = set(NBA_Stats['player'])

len(player_names)

#
# Create additional PD DFs
#

NBA_Rookie_Stats = NBA_Stats[NBA_Stats.exp == 0]
NBA_Second_Stats = NBA_Stats[NBA_Stats.exp == 1]
NBA_Third_Stats = NBA_Stats[NBA_Stats.exp == 2]

file_name = 'C:\Users\Nick\Desktop\GA\SF_DAT_15_WORK\Project\First_Draft\data\One.csv'
NBA_Rookie_Stats.to_csv(file_name,index=False)

file_name = 'C:\Users\Nick\Desktop\GA\SF_DAT_15_WORK\Project\First_Draft\data\Two.csv'
NBA_Second_Stats.to_csv(file_name,index=False)

file_name = 'C:\Users\Nick\Desktop\GA\SF_DAT_15_WORK\Project\First_Draft\data\Three.csv'
NBA_Third_Stats.to_csv(file_name,index=False)

#
NBA_Stats[['player','PER']][(NBA_Stats.exp > 0) & (NBA_Stats.player == 'Willie Green')].groupby('player').PER.mean()
NBA_Stats[['player','PER']][NBA_Stats.player == 'Willie Green'].groupby('player').PER.mean()
NBA_Stats[['player','PER']][(NBA_Stats.exp > 10) & (NBA_Stats.player == 'Willie Green')].groupby('player').PER.mean()


NBA_Stats[['player','PER']][NBA_Stats.exp > 0].groupby('player').PER.mean()
NBA_Stats[['player','PER']][NBA_Stats.exp > 0].groupby('player').PER.max()

NBA_Stats[['player','WS']][NBA_Stats.exp > 0].groupby('player').WS.mean()
NBA_Stats[['player','WS']][NBA_Stats.exp > 0].groupby('player').WS.max()

NBA_Stats[['player','WS/48']][NBA_Stats.exp > 0].groupby('player').mean()
NBA_Stats[['player','WS/48']][NBA_Stats.exp > 0].groupby('player').max()

NBA_Stats[['player','WS','PER','WS/48']][NBA_Stats.player == 'Zoran Planinic']

NBA_Stats.columns

# Data Exp

NBA_Stats.groupby('exp').exp.count()

#drinks.plot(x='beer_servings', y='wine_servings', kind='scatter', alpha=0.3)
#drinks.wine_servings.hist(by=drinks.continent, sharex=True, sharey=True)
NBA_Stats.plot(x='exp', y=groupby('exp').exp.count(), kind='line')

NBA_Stats.exp.hist(by=NBA_Stats.exp)
NBA_Stats['exp'].value_counts().plot(kind='bar')
'''
data stats
'''
#ufo.groupby('shapesreported').shapesreported.count()

file_name = 'C:\Users\Nick\Desktop\GA\SF_DAT_15_WORK\Project\First_Draft\data\NBAStats.csv'
NBA_Data = pd.read_csv(file_name)

NBA_Data.columns

player_names = set(NBA_Stats['player'])

len(player_names)
#2776 total players
player_names = list(player_names)
sorted_players = sorted(player_names, key = lambda x: x.split(' ')[-1])

#players who entered the league since 1976
#2725
len(Debuts['player'][Debuts.season_end >= 1976])
#players who entered the league since 1978
#2566
len(Debuts['player'][Debuts.season_end >= 1978])

inclusive_player_names = Debuts['player'][Debuts.season_end >= 1978]
len(inclusive_player_names)


#
#attempt 1
#
# This was the best attempt to adjust NBA player experience
#
for row_index in range(NBA_Data.shape[0]):
    row = NBA_Data.ix[row_index:row_index]
    if len(set(row['player']) & set(inclusive_player_names)):
        try:
            first_year = int(Debuts[Debuts.player ==list(row['player'])[0]]['season_end'])
            row['exp'] = row['season_end'] - first_year
        except:
            pass
        
        
NBA_Data.to_csv('NBA_Stats_Exp.csv',index=True)



    
15182    
NBA_Data.ix[15182:15182]

NBA_Data[NBA_Data.player == 'Michael Jordan'][['season_end','exp']]

NBA_Data.ix[0:0]
subNBA = list(NBA_t[1])
type(int(subNBA[0]))

#attempt 1
for player in inclusive_player_names:
    try:
        NBA_Data[NBA_Data.player == player]['exp'] = min(list(NBA_Data[NBA_Data.player == player]['season_end'])) - Debuts[Debuts.player == player]['season_end']
    except Exception as e:
        print e, player
        pass

#attempt 2
for player in inclusive_player_names:
    seasons = list(NBA_Data[NBA_Data.player == player]['season_end'])
    first_year = Debuts[Debuts.player == player]['season_end']
    for season in seasons:
        try:
            NBA_Data[(NBA_Data.player == player) & (NBA_Data.season_end == season)]['exp'] = season - first_year
        except Exception as e:
            print e, player
            pass

#           NBA_Data[(NBA_Data.player == 'Kobe Bryant') & (NBA_Data.season_end == 2000)]['season_end'] 


''' Note, you'll need to adjust the location of the NBA Rookies file per your own settings'''

#Load NBA Stats from CSVs
file_name = 'data\NBAStats.csv'
#NBA_Stats = pd.read_csv(file_name, index_col=0)
NBA_Stats = pd.read_csv(file_name)

file_name = 'data\Debut.csv'
Debuts = pd.read_csv(file_name)

#


