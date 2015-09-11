# -*- coding: utf-8 -*-
"""
Created on Wed Aug 19 20:24:54 2015

@author: Nick
"""

#Library for all execution
import requests # how python goes onto the internet!
from bs4 import BeautifulSoup # (version 4)
import unicodedata
import pandas as pd
import numpy as np
import csv

#Load NBA Stats from CSVs
file_name = 'C:\Users\Nick\Desktop\GA\SF_DAT_15_WORK\Project\First_Draft\data\NBAStats.csv'
NBA_Stats = pd.read_csv(file_name, index_col=0)
#NBA_Stats = pd.read_csv(file_name)

file_name = 'C:\Users\Nick\Desktop\GA\SF_DAT_15_WORK\Project\First_Draft\data\Debut.csv'
#Debuts = pd.read_csv(file_name)
Debuts = pd.read_csv(file_name, index_col=0)


NBA_Stats.columns
Debuts.columns

#
# Changing Columns
#

NBA_Stats['WSp48'] = NBA_Stats['WS/48']
del NBA_Stats['Rk_y'] 
del NBA_Stats['WS/48'] 

#

NBA_Stats[['player','season_end','PER','WS','WSp48']][NBA_Stats.player == 'Michael Finley']




#
# Remove NANs
#Fill Nulls
#

NBA_Stats.isnull().sum()

#NBAT = NBA_Stats
#ufo.Colors.fillna(value='Unknown', inplace=True)
#NBAT.fillna(value='Unknown', inplace=True)

NBA_Stats.fillna(value='0')
#NBAT.isnull().sum()


#to fix:
#fg_, x3p_. x2p_, efg_, ft_, PER, TS%, 3PAr, FTr, ORB%, DRB%, TRB%, AST%, STL%, BLK%, TOV%, USG%, WS/48
# FIXED:
#

#
# Calculate average PER & WS
# rename column
#

player_mean_PER = NBA_Stats.groupby('player').mean()['PER'].reset_index()
NBA_Stats = pd.merge(NBA_Stats,player_mean_PER,on='player',how='left')

#

NBA_Stats['PER_mean'] = NBA_Stats['PER_y']
NBA_Stats[['PER_mean','PER_y']]
del NBA_Stats['PER_y']

NBA_Stats.columns

player_mean_WS = NBA_Stats.groupby('player').mean()['WS'].reset_index()
NBA_Stats = pd.merge(NBA_Stats,player_mean_WS,on='player',how='left')

NBA_Stats['WS_mean'] = NBA_Stats['WS_y']
NBA_Stats[['WS_mean','WS_y']] 
del NBA_Stats['WS_y']

NBA_Stats.columns

player_mean_PER = NBA_Stats.groupby('player').mean()['PER'].reset_index()
NBA_Stats = pd.merge(NBA_Stats,player_mean_PER,on='player',how='left')

# For Debuts DF

NBA_Stats['PER_mean'] = NBA_Stats['PER_y']
NBA_Stats[['PER_mean','PER_y']]
del NBA_Stats['PER_y']


Debuts.columns

player_mean_WS = NBA_Stats.groupby('player').mean()['WS'].reset_index()
NBA_Stats = pd.merge(NBA_Stats,player_mean_WS,on='player',how='left')

NBA_Stats['WS_mean'] = NBA_Stats['WS_y']
NBA_Stats[['WS_mean','WS_y']] 
del NBA_Stats['WS_y']

Debuts.columns

#
# Create DataFrames for first 3 seasons
#

NBA_Rookie_Stats = NBA_Stats[NBA_Stats.exp == 0]
NBA_Second_Stats = NBA_Stats[NBA_Stats.exp == 1]
NBA_Third_Stats = NBA_Stats[NBA_Stats.exp == 2]

NBA_Rookie_Stats.columns

#
# Create CSVs for first 3 seasons
#

file_name = 'C:\Users\Nick\Desktop\GA\SF_DAT_15_WORK\Project\First_Draft\data\One.csv'
NBA_Rookie_Stats.to_csv(file_name,index=False)


file_name = 'C:\Users\Nick\Desktop\GA\SF_DAT_15_WORK\Project\First_Draft\data\Two.csv'
NBA_Second_Stats.to_csv(file_name,index=False)

file_name = 'C:\Users\Nick\Desktop\GA\SF_DAT_15_WORK\Project\First_Draft\data\Three.csv'
NBA_Third_Stats.to_csv(file_name,index=False)


#
# Save Data Frames as CSVs
#

file_name = 'C:\Users\Nick\Desktop\GA\SF_DAT_15_WORK\Project\First_Draft\data\NBAStats.csv'
NBA_Stats.to_csv(file_name,index=True)
#NBA_Rookie_Stats.to_csv(file_name,index=False)

file_name = 'C:\Users\Nick\Desktop\GA\SF_DAT_15_WORK\Project\First_Draft\data\Debut.csv'
Debuts.to_csv('Debut.csv',index=True)







