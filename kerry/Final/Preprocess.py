# -*- coding: utf-8 -*-
"""
Created on Wed Mar 11 20:17:11 2015
The All-NBA team has been annual awarded bestowed to the best players in the league at the end of every season. 
It is particularly based on votes conducted by sportswriter and broadcasters across North America.  
There are three-five man teams: First, Second, and Third. 
It is suppsoed to be an assessment of the based players at their respective positions. 
Given that avaliable basketball data, can we predict which players will be voted into each team by the end of the 2014-15 season? 


Sourc: http://www.basketball-reference.com/

@author: MindKontrol
"""
import pandas as pd
import csv
import matplotlib.pyplot as plt
import numpy as np

#DATA
#BASIC ATTRIBUTES

#col_u = ["player","pos","age","bref_team_id","g","gs","mp","fg","fga","fg_","x3p","x3pa","x3p_","x2p","x2pa","x2p_","ft","fta","ft_","orb","drb","trb","ast","stl","blk","tov","pf","pts","table_name","season","data_source","scrape_time"]
#all_nba= pd.read_table("https://raw.githubusercontent.com/kjones8812/abresler.github.io/master/data/NBA/player_data/all_player_per_game/nba_player_per_game_data_1951_2015.csv", header= 0,sep = ',',names = col_u)
all_nba = pd.read_csv("/Users/MindKontrol/Python/GADataScience/DAT4/Forecasting All NBA Teams/all_nba_abresler")

#all_nba.to_csv('all_nba_abresler')

type(all_nba) #Data Frame
all_nba.head(10) #Print first 10 rows
all_nba.tail(10)#print last 10 rows
all_nba.describe() # summarize all numeric  columns
all_nba.dtypes #mixture of data types(integers, floats,string objects )
all_nba.shape # There are currently 19030 rows and 32 columns
all_nba.values #dataframe as array
all_nba.info() #missing values in: pos, age,fg.,x3p.,x2p.,ft.


#Used Web Scraping to pull togehter more advanced statistics

nba_advance = pd.read_csv("/Users/MindKontrol/Python/GADataScience/DAT4/Forecasting All NBA Teams/advanced_stats")
nba_advance.head(10) #Print first 10 rows
nba_advance.tail(10)#print last 10 rows
nba_advance.describe() # summarize all numeric  columns
nba_advance.dtypes #mixture of data types(integers, floats,string objects )
nba_advance.shape # There are currently 18977 rows and 31 columns
nba_advance.values #dataframe as array
nba_advance.info() #missing values in: TS, 3PAr, FTr,ORB%,DRB%,%TRB, %AST,%STL,%BLK,%USG,WS,OWS,DWS, BPM,OBPM,DBPM,VORP

#Join on player name and season
#Create new variable in all_nba

season_end = [int(sea[-4:]) for sea in all_nba.season]
all_nba['season_end'] = season_end

#Merge function, using inner join....?
all_stats = pd.merge(all_nba, nba_advance,how = "inner", on = ['player', 'season_end'])

#Del variables
del all_stats['table_name']
del all_stats['season']
del all_stats['data_source']
del all_stats['scrape_time']
del all_stats['Unnamed: 0_x']
del all_stats['Rk']
del all_stats['Pos']
del all_stats['Age']
del all_stats['Tm']
del all_stats['MP']
del all_stats['G']
del all_stats['blnk']
del all_stats['blnk2']
del all_stats['ORB%']
del all_stats['DRB%']

#Handling Missing Values

all_stats.info()
"""""""""""""""""""""

Missing values were found on 2 occasions:
    1) Shooting percentages(when players did not have an attempt)
    2) some attributes were not recorded until mid-late 70s, early 80s. Three pointers, STLs,TOV, ORB,DRB,BLKS
    3) Advance metrics weren't used throughout years because of this.
       
    Most varibles if missing were given 0
    %AST/%TRB although missing for some years, AST/TRB were recorded so, fill with median value.
"""""""""""""""""""""""""""


all_stats[all_stats.fg_.isnull()] # players who did not have any shot attempts 
all_stats.fg_.fillna(value = 0, inplace = True)

all_stats[all_stats.x3p_.isnull()]   #players who did not have any 3 point shot attempts
all_stats.x3p_.fillna(value = 0, inplace = True)

all_stats[all_stats.x2p_.isnull()] #players who did not have any 2 point shot attempts
all_stats.x2p_.fillna(value = 0, inplace = True)

all_stats[all_stats.ft_.isnull()] #players who did not have any Free throw attempts
all_stats.ft_.fillna(value = 0, inplace = True)

#if missing used the median, because every playerwhere value was missing, played in games and had some form of contribution
#Were variables calculated consistently through out time. 
all_stats['PER'].isnull().sum()
all_stats[all_stats.PER.isnull()]
all_stats.PER.fillna(value =all_stats.PER.median(), inplace =True)

all_stats['TRB%'].isnull().sum()
all_stats['TRB%'].fillna(value =all_stats['TRB%'].median(), inplace =True)

all_stats['AST%'].isnull().sum()
all_stats[all_stats['AST%'].isnull()]
all_stats['AST%'].fillna(value =all_stats['AST%'].median(), inplace =True)

#Winshares missing for players during 1950s, so took median of this as well. More or less assessments of average players contrinbution towards offensive, defense, and total. Didn't have info but just took median. 

all_stats['OWS'].isnull().sum()
all_stats[all_stats['OWS'].isnull()]
all_stats['OWS'].fillna(value =all_stats['OWS'].median(), inplace =True)
all_stats['DWS'].isnull().sum()
all_stats[all_stats['DWS'].isnull()]
all_stats['DWS'].fillna(value =all_stats['DWS'].median(), inplace =True)
all_stats['WS'].isnull().sum()
all_stats[all_stats['WS'].isnull()]
all_stats['WS'].fillna(value =all_stats['WS'].median(), inplace =True)

all_stats['WS/48'].isnull().sum()
all_stats[all_stats['WS/48'].isnull()]
all_stats['WS/48'].fillna(value =all_stats['WS/48'].median(), inplace =True)

all_stats['OBPM'].isnull().sum()
all_stats[all_stats['OBPM'].isnull()]
all_stats['OBPM'].fillna(value =all_stats['OBPM'].median(), inplace =True)

all_stats['DBPM'].isnull().sum()
all_stats[all_stats['DBPM'].isnull()]
all_stats['DBPM'].fillna(value =all_stats['DBPM'].median(), inplace =True)

all_stats['BPM'].isnull().sum()
all_stats[all_stats['BPM'].isnull()]
all_stats['BPM'].fillna(value =all_stats['BPM'].median(), inplace =True)

all_stats['VORP'].isnull().sum()
all_stats[all_stats['VORP'].isnull()]
all_stats['VORP'].fillna(value =all_stats['VORP'].median(), inplace =True)


#Everything else kept 0 because these attributes were not used until later. 
all_stats['TS%'].isnull().sum()
all_stats[all_stats['TS%'].isnull()]
all_stats['TS%'].fillna(value =0, inplace =True)

all_stats['3PAr'].isnull()
all_stats[all_stats['3PAr'].isnull()]
all_stats['3PAr'].fillna(value =0, inplace =True)

all_stats['FTr'].isnull().sum()
all_stats[all_stats['FTr'].isnull()]
all_stats['FTr'].fillna(value =0, inplace =True)


all_stats['STL%'].isnull().sum()
all_stats[all_stats['STL%'].isnull()]
all_stats['STL%'].fillna(value =0, inplace =True)

all_stats['BLK%'].isnull().sum()
all_stats['BLK%'].fillna(value =0, inplace =True)

all_stats['TOV%'].isnull().sum()
all_stats[all_stats['TOV%'].isnull()]
all_stats['TOV%'].fillna(value =0, inplace =True)

all_stats['USG%'].isnull().sum()
all_stats[all_stats['USG%'].isnull()]
all_stats['USG%'].fillna(value =0, inplace =True)


#Also need to get the 2015 data and process:

NBA_players_2015=  pd.read_csv("/Users/MindKontrol/Python/GADataScience/DAT4/Forecasting All NBA Teams/CurrentYearStats")
NBA_players_2015.info()
NBA_players_2015.fg_.fillna(value = 0, inplace = True)

NBA_players_2015.x3p_.fillna(value = 0, inplace = True)

NBA_players_2015.x2p_.fillna(value = 0, inplace = True)
NBA_players_2015.ft_.fillna(value = 0, inplace = True)
NBA_players_2015['TS%'].fillna(value =0, inplace =True)
NBA_players_2015['3PAr'].fillna(value =0, inplace =True)
NBA_players_2015['FTr'].fillna(value =0, inplace =True)

NBA_players_2015['TOV%'].fillna(value =0, inplace =True)

del NBA_players_2015['Unnamed: 0']
del NBA_players_2015['Pos']
del NBA_players_2015['Age']
del NBA_players_2015['Tm']
del NBA_players_2015['blnk']
del NBA_players_2015['blnk2']
del NBA_players_2015['Rk_x']
del NBA_players_2015['Rk_y']
del NBA_players_2015['ORB%']
del NBA_players_2015['DRB%']

NBA_players_2015.pos.value_counts()

NBA_players_2015.replace('SG','G', inplace = True) #decided to change to Gs and Fs because All NBA teams 
NBA_players_2015.replace('PG','G', inplace = True) 
NBA_players_2015.replace('SF','F',inplace = True) 
NBA_players_2015.replace('PF','F',inplace = True) 
NBA_players_2015.replace('C-PF','C', inplace = True) #Primary Position 
NBA_players_2015.replace('SF-SG','F', inplace = True) 
NBA_players_2015.replace('PG-SG','G',inplace = True) 
NBA_players_2015.replace('SG-PG','G',inplace = True) 
NBA_players_2015.replace('PF-C','F', inplace = True) #decided to change to Gs and Fs because All NBA teams 
NBA_players_2015.replace('PF-SF','F', inplace = True) 
NBA_players_2015.replace('SF-PF','F',inplace = True) 
NBA_players_2015.replace('F-C','F',inplace = True) 
NBA_players_2015.replace('F-G','F',inplace = True) 
NBA_players_2015.replace('SG-SF','G',inplace = True) 
NBA_players_2015.replace('G-F','G',inplace = True) 
NBA_players_2015.replace('C-F','C',inplace = True) 
NBA_players_2015.replace('SG-PF','G',inplace = True) 
NBA_players_2015.replace('C-SF','C',inplace = True) 
NBA_players_2015.replace('SF-G','F',inplace = True) 
NBA_players_2015.replace('PG-SF','G',inplace = True) 
NBA_players_2015.replace('SF-PG','F',inplace = True) 


NBA_players_2015.to_csv('/Users/MindKontrol/Python/GADataScience/DAT4/Forecasting All NBA Teams/NBA_players_2015.csv')

#Add ALL-NBA Team Data


NBA= pd.read_csv("/Users/MindKontrol/Python/GADataScience/DAT4/Forecasting All NBA Teams/All_Team_Data.csv")
NBA_players = pd.merge(all_stats, NBA, how = "left", on = ['player', 'season_end'])

#Where value in team varible is missing fill with none.
NBA_players.team.fillna(value = 'None', inplace = True)

#Void missing age values 
NBA_players  = NBA_players[NBA_players.age.notnull()]

#Selection teams consists of two guards, two forwards, adn one center
#So need to aggergate positions into G,F,C
NBA_players[NBA_players.pos.isnull()]# I know that Jarnell Stokes is a PF
NBA_players.pos.fillna(value = 'F', inplace = True) 

#NBA_players.pos.value_counts()

NBA_players.replace('SG','G', inplace = True) #decided to change to Gs and Fs because All NBA teams 
NBA_players.replace('PG','G', inplace = True) 
NBA_players.replace('SF','F',inplace = True) 
NBA_players.replace('PF','F',inplace = True) 
#First just preprocess by taking average

#Exploratory Analysis
#Find most important features, parellel coordinates; coorealtion matrix

NBA_players.to_csv('NBA_players.csv')


corrMat =NBA_players.corr()
NBA_players.columns

from pandas.tools.plotting import parallel_coordinates
features = [["g","gs","mp","fg","fga","fg_","x3p","x3pa","x3p_","x2p","x2pa","x2p_","ft","fta","ft_","orb","drb","trb","ast","stl","blk","tov","pf","pts"]]
#features = [['g','gs','mp','pts','AST%','PER','STL%','USG%','FTr','3PAr','TS%','VORP','BPM','OBPM','DBPM','WS','WS/48','DWS','OWS',]]
NBA_df = pd.DataFrame(NBA_players, columns = features)
NBA_df['team']= NBA_players.team
parallel_coordinates(data=NBA_df,class_column = 'team')


                     


