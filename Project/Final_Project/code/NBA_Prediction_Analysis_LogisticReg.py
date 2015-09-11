# -*- coding: utf-8 -*-
"""
Created on Thu Aug 20 08:40:53 2015

@author: Nick
"""

from sklearn import metrics
from sklearn import datasets
from sklearn.cluster import KMeans
from sklearn.datasets.samples_generator import make_blobs, make_moons
from sklearn.metrics.pairwise import euclidean_distances
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from sklearn.linear_model import LinearRegression
from sklearn.linear_model import LogisticRegression
from sklearn.cross_validation import train_test_split
import statsmodels.formula.api as smf

import seaborn as sns
import matplotlib.pyplot as plt

import nltk
nltk.download('all')

#
# Load saved CSVs into Data Frames
#

file_name = 'C:\Users\Nick\Desktop\GA\SF_DAT_15_WORK\Project\First_Draft\data\NBAStats.csv'
#NBA_Stats = pd.read_csv(file_name, index_col=0)
NBA_Stats = pd.read_csv(file_name)

file_name = 'C:\Users\Nick\Desktop\GA\SF_DAT_15_WORK\Project\First_Draft\data\Debut.csv'
Debuts = pd.read_csv(file_name)

file_name = 'C:\Users\Nick\Desktop\GA\SF_DAT_15_WORK\Project\First_Draft\data\One.csv'
NBA_Rookie_Stats = pd.read_csv(file_name)

file_name = 'C:\Users\Nick\Desktop\GA\SF_DAT_15_WORK\Project\First_Draft\data\Two.csv'
NBA_Second_Stats = pd.read_csv(file_name)

file_name = 'C:\Users\Nick\Desktop\GA\SF_DAT_15_WORK\Project\First_Draft\data\Three.csv'
NBA_Third_Stats = pd.read_csv(file_name)

#
# Logistic Regression for PER
#

sample_cols = ["age","g","mp","trb","ast","stl","blk","tov","pf","pts"]
#feature_cols = ["season_end","Rk_x","player","pos","age","bref_team_id","g","gs","mp","fg","fga","fg_","x3p","x3pa","x3p_","x2p","x2pa","x2p_","efg_","ft","fta","ft_","orb","drb","trb","ast","stl","blk","tov","pf","pts", 'TS%', '3PAr', 'FTr', 'ORB%', 'DRB%', 'TRB%', 'AST%', 'STL%', 'BLK%', 'TOV%', 'USG%',, 'OWS', 'DWS', 'OBPM', 'DBPM', 'BPM', 'VORP']

#
# Linear Regression for PER
#

#X = NBA_Stats[feature_cols]

NBA_Rookie_Stats['PER_cond'] = NBA_Rookie_Stats['PER_mean'].apply(lambda x: True if x >= 20 else False)

NBA_Rookie_Stats[['player','PER_mean','PER_cond']][NBA_Rookie_Stats.PER_cond == True].count()
NBA_Rookie_Stats[['player','PER_mean','PER_cond']].count()

good_players = NBA_Rookie_Stats[['player','PER_mean','PER_cond']][NBA_Rookie_Stats.PER_cond == True].count() / NBA_Rookie_Stats[['player','PER_mean','PER_cond']].count()

X = NBA_Rookie_Stats[sample_cols]
Cond_y = NBA_Rookie_Stats.PER_cond

X_train, X_test, y_train, y_test = train_test_split(X, Cond_y, random_state=1)
logreg = LogisticRegression()
logreg.fit(X_train, y_train)

PER_Prediction = logreg.predict(X_test)
matrix = metrics.confusion_matrix(y_test, PER_Prediction)

sensitivity = float(matrix[1][1]) / (matrix[1][0] + matrix[1][1])
# sensitivity = 20.0% 
specificity = float(matrix[0][0]) / (matrix[0][1] + matrix[0][0])
# specificity = 99.8 %
accuracy = (float(matrix[0][0]) + matrix[1][1]) / ((matrix[1][0] + matrix[1][1])+(matrix[0][1] + matrix[0][0]))
# accuracy = 97.9%

#Cross Validation

cross_val_score(logreg, X, Cond_y, scoring='roc_auc', cv=10).mean()
# 0.898

cross_val_score(logreg, X, Cond_y, cv=10, scoring='accuracy').mean()
# 97.6

#ROC_AUC
#array([ 0.89622642,  0.89712489,  0.86238395,  0.88948787,  0.90791808])

#
# Linear Regression for WS
#

#X = NBA_Stats[feature_cols]

NBA_Rookie_Stats['WS_cond'] = NBA_Rookie_Stats['WS_mean'].apply(lambda x: True if x >= 6.5 else False)

NBA_Rookie_Stats[['player','WS_mean','WS_cond']]

NBA_Rookie_Stats[['player','WS_mean','WS_cond']][NBA_Rookie_Stats.WS_cond == True].count()
NBA_Rookie_Stats[['player','WS_mean','WS_cond']].count()

good_players = NBA_Rookie_Stats[['player','WS_mean','WS_cond']][NBA_Rookie_Stats.WS_cond == True].count() / NBA_Rookie_Stats[['player','WS_mean','WS_cond']].count()

X = NBA_Rookie_Stats[sample_cols]
Cond_y = NBA_Rookie_Stats.WS_cond

X_train, X_test, y_train, y_test = train_test_split(X, Cond_y, random_state=1)
logreg = LogisticRegression()
logreg.fit(X_train, y_train)

WS_Prediction = logreg.predict(X_test)
matrix = metrics.confusion_matrix(y_test, WS_Prediction)

sensitivity = float(matrix[1][1]) / (matrix[1][0] + matrix[1][1])
# sensitivity = 29.4% 
specificity = float(matrix[0][0]) / (matrix[0][1] + matrix[0][0])
# specificity = 99.2 %
accuracy = (float(matrix[0][0]) + matrix[1][1]) / ((matrix[1][0] + matrix[1][1])+(matrix[0][1] + matrix[0][0]))
# accuracy = 97.2%

#Cross Validation

cross_val_score(logreg, X, Cond_y, scoring='roc_auc', cv=10).mean()
# 0.922

cross_val_score(logreg, X, Cond_y, cv=10, scoring='accuracy').mean()
# 96.7

#
# Save CSV
#

file_name = 'C:\Users\Nick\Desktop\GA\SF_DAT_15_WORK\Project\First_Draft\data\One.csv'
NBA_Rookie_Stats.to_csv(file_name,index=False)