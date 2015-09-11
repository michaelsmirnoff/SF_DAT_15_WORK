# -*- coding: utf-8 -*-
"""
Created on Wed Jul 18 12:10:44 2015

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
from sklearn import svm, linear_model, datasets
from sklearn.cross_validation import cross_val_score
from sklearn.pipeline import Pipeline
import statsmodels.formula.api as smf

import seaborn as sns
import matplotlib.pyplot as plt

import nltk
nltk.download('all')

#
# Load saved CSVs into Data Frames
#

file_name = 'https://raw.githubusercontent.com/nsmirnov/SF_DAT_15_WORK/master/Project/Final_Project/data/NBAStats.csv'
NBA_Stats = pd.read_csv(file_name, index_col=0)

file_name = 'https://raw.githubusercontent.com/nsmirnov/SF_DAT_15_WORK/master/Project/Final_Project/data/One.csv'
NBA_Rookie_Stats = pd.read_csv(file_name)

file_name = 'https://raw.githubusercontent.com/nsmirnov/SF_DAT_15_WORK/master/Project/Final_Project/data/Two.csv'
NBA_Second_Stats = pd.read_csv(file_name)

file_name = 'https://raw.githubusercontent.com/nsmirnov/SF_DAT_15_WORK/master/Project/Final_Project/data/Three.csv'
NBA_Third_Stats = pd.read_csv(file_name)

#linear regression
sns.pairplot(NBA_Stats)

pd.scatter_matrix(NBA_Stats, figsize=(12, 10))

NBA_Stats.columns
NBA_Rookie_Stats.columns

sample_cols = ["age","g","mp","trb","ast","stl","blk","tov","pf","pts"]
sample_cols = ["age","g", "mp", "fg", "fga", "fg_", "x3p", "x3pa", "x3p_","x2p", "x2pa", "x2p_", "efg_", "ft", "fta", "ft_", "orb","drb", "trb", "ast", "stl", "blk", "tov", "pf", "pts","TS%", "3PAr", "FTr", "ORB%", "DRB%", "TRB%", "AST%","STL%", "BLK%", "TOV%", "USG%"]
#feature_cols = ["season_end","Rk_x","player","pos","age","bref_team_id","g","gs","mp","fg","fga","fg_","x3p","x3pa","x3p_","x2p","x2pa","x2p_","efg_","ft","fta","ft_","orb","drb","trb","ast","stl","blk","tov","pf","pts", 'TS%', '3PAr', 'FTr', 'ORB%', 'DRB%', 'TRB%', 'AST%', 'STL%', 'BLK%', 'TOV%', 'USG%',, 'OWS', 'DWS', 'OBPM', 'DBPM', 'BPM', 'VORP']

# Linear Regression for PER

#X = NBA_Stats[feature_cols]
X = NBA_Rookie_Stats[sample_cols]
y = NBA_Rookie_Stats.PER_mean

# instantiate and fit
linreg = LinearRegression()
linreg.fit(X, y)

print linreg.intercept_
print linreg.coef_

zip(sample_cols, linreg.coef_)

NBAV = linreg.coef_
NBAhash = {}

for i in range(len(sample_cols)):
    NBAhash[ sample_cols[i] ] = NBAV[i]

X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=1)

linreg = LinearRegression()
linreg.fit(X_train, y_train)

#lm = smf.ols(formula='PER ~ age + ast + blk + g + mp + pf + pts + stl + tov + trb', data=NBA_Stats).fit()
lm = smf.ols(formula='PER_mean ~ age + g + mp + fg + fga + fg_ + x3p + x3pa + x3p_ + x2p + x2pa + x2p_ + efg_ + ft + fta + ft_ + orb + drb + trb + ast + stl + blk + tov + pf + pts + TS% + 3PAr + FTr + ORB% + DRB% + TRB% + AST% + STL% + BLK% + TOV% + USG%', data=NBA_Stats).fit()
lm = smf.ols(formula='PER_mean ~ age + g + mp + fg + fga + fg_ + x3p + x3pa + x3p_ + x2p + x2pa + x2p_ + efg_ + ft + fta + ft_ + orb + drb + trb + ast + stl + blk + tov + pf + pts + FTr', data=NBA_Stats).fit()

lm.pvalues 

zip(sample_cols, linreg.coef_)
''' Co-efs
cool:    0.2634
useful: -0.1471
funny: - 0.1289
'''


#R_Squared:
#lm = smf.ols(formula='stars ~ cool + useful + funny', data=YelpData).fit()
lm.rsquared
#  R_Squared: 0.54

y_pred = linreg.predict(X_test)

#MAE:
print metrics.mean_absolute_error(y_test, y_pred)
# MAE = 2.3718132887


#RMSE:
print np.sqrt(metrics.mean_squared_error(y_test, y_pred))

# RMSE = 3.45765755975


# Scross-Validation
scores = cross_val_score(linreg, X, y, scoring='mean_squared_error', cv=5)

#array([-12.02567298, -24.60356426, -26.6180074 , -13.67459742, -17.27870706])

scores = cross_val_score(linreg, X, y, scoring='mean_squared_error', cv=10)

#array([ -7.84199514, -16.09987499, -25.52726151, -22.72150749,
#       -31.97410682, -27.67546978, -10.80397927, -16.21574526,
#       -15.99544992, -19.19970488])





#
# Linear Regression for WS
#

#sample_cols = ["age","g","mp","trb","ast","stl","blk","tov","pf","pts"]
#feature_cols = ["season_end","Rk_x","player","pos","age","bref_team_id","g","gs","mp","fg","fga","fg_","x3p","x3pa","x3p_","x2p","x2pa","x2p_","efg_","ft","fta","ft_","orb","drb","trb","ast","stl","blk","tov","pf","pts", 'TS%', '3PAr', 'FTr', 'ORB%', 'DRB%', 'TRB%', 'AST%', 'STL%', 'BLK%', 'TOV%', 'USG%',, 'OWS', 'DWS', 'OBPM', 'DBPM', 'BPM', 'VORP']

# Linear Regression for PER

#X = NBA_Stats[feature_cols]
X = NBA_Stats[sample_cols]
y = NBA_Stats.WS_mean

# instantiate and fit
linreg = LinearRegression()
linreg.fit(X, y)

print linreg.intercept_
print linreg.coef_

zip(sample_cols, linreg.coef_)

X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=1)

linreg = LinearRegression()
linreg.fit(X_train, y_train)

lm = smf.ols(formula='WS_mean ~ age + g + mp + fg + fga + fg_ + x3p + x3pa + x3p_ + x2p + x2pa + x2p_ + efg_ + ft + fta + ft_ + orb + drb + trb + ast + stl + blk + tov + pf + pts + TS% + 3PAr + FTr + ORB% + DRB% + TRB% + AST% + STL% + BLK% + TOV% + USG%', data=NBA_Stats).fit()
lm = smf.ols(formula='WS_mean ~ age + g + mp + fg + fga + fg_ + x3p + x3pa + x3p_ + x2p + x2pa + x2p_ + efg_ + ft + fta + ft_ + orb + drb + trb + ast + stl + blk + tov + pf + pts + FTr', data=NBA_Stats).fit()
lm.pvalues 

#R_Squared:
#lm = smf.ols(formula='stars ~ cool + useful + funny', data=YelpData).fit()
lm.rsquared
#  R_Squared: 0.54

y_pred = linreg.predict(X_test)

#MAE:
print metrics.mean_absolute_error(y_test, y_pred)
# MAE = 1.00893315001

#RMSE:
print np.sqrt(metrics.mean_squared_error(y_test, y_pred))

# RMSE = 1.36337738484


# Scross-Validation
linreg = LinearRegression()
scores = cross_val_score(linreg, X, y, scoring='mean_squared_error', cv=5)

#array([-1.86308346, -1.79443844, -1.91262201, -1.92342407, -1.86764912])

scores = cross_val_score(linreg, X, y, scoring='mean_squared_error', cv=10)

#array([-1.72139261, -1.98520686, -1.85981714, -1.69573518, -1.96760124,
#       -1.84324098, -1.9279525 , -1.89524026, -1.91018435, -1.82265031])