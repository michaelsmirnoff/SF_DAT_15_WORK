# -*- coding: utf-8 -*-
"""
Created on Sun Feb 15 13:00:55 2015

@author: jenniferlambert
"""


# imports 
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# read csv file in
data = pd.read_csv('Facebook_SA_data.csv')
data.head()

# explore data/make sure it looks ok
data.describe()

data.Theme=data.Theme.map(lambda x: x.lower())

# KM: I changed this line to actually store the results back into data.Theme
# previously, you were doing the map but not storing it anywhere
data.Theme=data.Theme.map(lambda x: x.replace('freedom of speech', 'Free Expression').replace('peace corps', 'Development').replace('learning english', 'English Learning').replace('english Learning', 'English Learning').replace('freedom of expression', 'Free Expression').replace('Freedom of Speech', 'Free Expression').replace('culture preservation', 'Preservation').replace('freedom of expression', 'Free Expression').replace('birthday greeting', 'Mission Affairs').replace('apec', 'Trade').replace('apec', 'Trade').replace('shareAmerica announcement', 'About America').replace('shareamerica announcement', 'About America').title())

# KM: determine the unique themes
themes = set()
for t in data.Theme:
    themes.update(t for t in t.split(','))
themes = sorted(themes)
print themes

# KM: make a column for each theme
for theme in themes:
    data[theme] = [1 if theme in row.split(',') else 0 for row in data.Theme]

# KM: change max number of columns printed so that you can see the results
pd.set_option('max_columns', None)
data.head()

# make other text based columns/variables into dummy variables
data['SA'] = np.where(data['SA? (Y/N)']=='Y', 1, 0)
del data['SA? (Y/N)']

data['link'] = np.where(data['Post_Type']=='Link', 1, 0)
data['link']
data['video'] = np.where(data['Post_Type']=='Video', 1, 0)
data['status'] = np.where(data['Post_Type']=='Status', 1, 0)
data['photo'] = np.where(data['Post_Type']=='Photo', 1, 0)

# remove %age sign from SharesperUser column

data.SharesperUser=data.SharesperUser.map(lambda x: float(x[:-1]))

### Cleaning up column names - since I decided to use Stats Models, I need to eliminate spaces in the column names 
data.columns

headers = ['Mission', 'PostID', 'Blurb', 'Post_Type', 'DateTime', 'UsersReached', 'PaidReach', 'EngagedUsers', 'ClicksPost', 'FansReached', 'EngagedFans', 'Comments', 'Likes', 'Shares', 'LinkClicks', 'EngRatio', 'PosttoPost', 'PropFansReached', 'EngNonFans', 'LCSEngRatio', 'SharesperUser', 'LikesRatio', 'CommentsRatio', 'LinkClicksRatio', 'Theme', 'SATitle', 'AboutAmerica', 'Art', 'Asean', 'Campususa', 'CivilSociety', 'Culture', 'Democracy', 'Development', 'Diversity', 'DrugEnforcement', 'Economy', 'Education', 'EnglishLearning', 'Entrepreneurship', 'Environment', 'FreeExpression', 'GoodGovernance', 'Grants', 'Health', 'HumanRights', 'MissionAffairs', 'Policy', 'Preservation', 'ScienceTech', 'Sports', 'StudyinUSA', 'Trade', 'TraveltoUSA', 'Visas', 'Women', 'Yali', 'Yseali', 'SA', 'link', 'video', 'status', 'photo']

data.columns = headers

# First, try the linear regression model from sklearn
## Run train, test, split (in this, function, the features and response variables will be defined)
# create X and y
feature_cols = ['SA', 'link', 'video', 'status', 'photo', 'AboutAmerica', 'Art', 'Asean', 'Campususa', 'CivilSociety', 'Culture', 'Democracy', 'Development', 'Diversity', 'DrugEnforcement', 'Economy', 'Education', 'EnglishLearning', 'Entrepreneurship', 'Environment', 'FreeExpression', 'GoodGovernance', 'Grants', 'Health', 'HumanRights', 'MissionAffairs', 'Policy', 'Preservation', 'ScienceTech', 'Sports', 'StudyinUSA', 'Trade', 'TraveltoUSA', 'Visas', 'Women', 'Yali', 'Yseali']
X = data[feature_cols]
y = data.SharesperUser
#test-train-split
from sklearn.cross_validation import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=4)
X_train.shape
X_test.shape
y_train.shape
y_test.shape

## run linear regression to find what features are significant in explaining/predicting higher shares per users reached.

# follow the usual sklearn pattern: import, instantiate, fit
from sklearn.linear_model import LinearRegression
lm = LinearRegression()
lm.fit(X_train, y_train)

lm.score(X_test, y_test)

preds = lm.predict(X_test)

from sklearn import metrics

metrics.mean_squared_error(y_test, preds)
np.sqrt(metrics.mean_squared_error(y_test, preds))

# if metrics are good, print intercept and coefficients, but only for LM
print lm.intercept_
print lm.coef_

## cross-validate results to see how good the linear regression is at predicting shares per users reached
from sklearn.cross_validation import cross_val_score
linreg = LinearRegression()
scores = cross_val_score(linreg, X, y, cv=10, scoring='mean_squared_error').mean()
np.sqrt(-scores)

data.SharesperUser.describe()

# Now i'm going to try a different model - the decision tree regressor (from sklearn)
from sklearn.tree import DecisionTreeRegressor
treereg = DecisionTreeRegressor(random_state=1)
treereg.fit(X_train, y_train)

# print metrics (specific to the problem, not the model)
treereg.score(X_test, y_test)
predstr = treereg.predict(X_test)
metrics.mean_squared_error(y_test, predstr)
np.sqrt(metrics.mean_squared_error(y_test, predstr))

## cross validation 
scorestr = cross_val_score(treereg, X, y, cv=10, scoring='mean_squared_error').mean()
np.sqrt(-scorestr)

# Now, let's run a linear regression in stats models so I can look at the p-values for all my feeatures
import statsmodels.formula.api as smf

# create a fitted model in one line (OLS)
lm = smf.ols(formula='SharesperUser ~ SA + link + video + status + photo + AboutAmerica + Art + Asean + Campususa + CivilSociety + Culture + Democracy + Development + Diversity + DrugEnforcement + Economy + Education + EnglishLearning + Entrepreneurship + Environment + FreeExpression + GoodGovernance + Grants + Health + HumanRights + MissionAffairs + Policy + Preservation + ScienceTech + Sports + StudyinUSA + Trade + TraveltoUSA + Visas + Women + Yali + Yseali', data=data).fit()

# print the coefficients and other metrics 
lm.params
lm.rsquared
lm.conf_int()
lm.pvalues
