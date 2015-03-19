# -*- coding: utf-8 -*-
"""
Created on Sun Mar 15 10:11:07 2015

@author: MindKontrol
"""


import pandas as pd
import csv
import matplotlib.pyplot as plt
import numpy as np
#
#
NBA_players= pd.read_csv("/Users/MindKontrol/Python/GADataScience/DAT4/Forecasting All NBA Teams/NBA_players.csv")
#
NBA_players_2015=  pd.read_csv("/Users/MindKontrol/Python/GADataScience/DAT4/Forecasting All NBA Teams/NBA_players_2015.csv")

corrMat =NBA_players.corr()

NBA_players.team= np.where(NBA_players.team != 'None',1,0)

NBA_players.team.value_counts().plot(kind = 'bar')

plt.title("Distribution of Honorees, (1 = Made Team)")  
#Only 750 players have made team


alpha_level = .35
NBA_players.pts[NBA_players.team ==0].plot(kind = 'hist',alpha=alpha_level)
NBA_players.pts[NBA_players.team ==1].plot(kind = 'hist')
plt.xlabel("Pts")
plt.ylabel("Points Distribution" )
plt.legend(('No team','All NBA Team', ),loc='best')




NBA_players.WS[NBA_players.team ==1].plot(kind = 'hist')
NBA_players.WS[NBA_players.team ==0].plot(kind = 'hist', alpha=alpha_level)
plt.legend(('All NBA Team', 'No team'),loc='best')
plt.xlabel("Win Shares")
plt.ylabel("Win Share Distribution" )



NBA_players.mp[NBA_players.team ==1].plot(kind = 'hist')
NBA_players.mp[NBA_players.team ==0].plot(kind = 'hist',alpha=alpha_level)
plt.legend(('All NBA Team', 'No team'),loc='best')
plt.xlabel("Minutes Played")
plt.ylabel("Minutes Played Distribution" )



NBA_players.PER[NBA_players.team ==1].plot(kind = 'kde')
NBA_players.PER[NBA_players.team ==0].plot(kind = 'kde',alpha=alpha_level)
plt.legend(('All NBA Team', 'No team'),loc='best')
plt.xlabel("Player Efficiency")
plt.ylabel("Player Efficiency Rating Distribution" )

