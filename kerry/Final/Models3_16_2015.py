# -*- coding: utf-8 -*-
"""
Created on Mon Mar 16 11:01:58 2015

@author: joneskm1
"""


import pandas as pd
import csv
import matplotlib.pyplot as plt
import numpy as np
#

#Read in data 
NBA_players= pd.read_csv('C:\Users\joneskm1\Documents\General_Assembly\DAT4\Forecasting All NBA Teams\NBA_players.csv')
NBA_players_2015 =  pd.read_csv('C:\Users\joneskm1\Documents\General_Assembly\DAT4\Forecasting All NBA Teams\NBA_players_2015.csv')

#Set up data for predicting 2014 teams
nba_2014= NBA_players[NBA_players.season_end == 2014]
nbaHistoric= NBA_players[NBA_players.season_end <= 2013]

#Set up data for predicting 2015 teams

nbaHistoric2= NBA_players[NBA_players.season_end <= 2014]
nba_2015= NBA_players_2015

#Logistic Regerssion#
#First Model using basic stats


from sklearn.linear_model import LogisticRegression
from sklearn.cross_validation import train_test_split
from sklearn import metrics


d = nbaHistoric
d.info()

d_2014 = nba_2014
d_2014.info()


col_u = ["g","gs","mp","fg","fga","fg_","x3p","x3pa","x3p_","x2p","x2pa","x2p_","ft","fta","ft_","orb","drb","trb","ast","stl","blk","tov","pf","pts"]

#Set up X and y variables
X= d[col_u]
X_2014 = d_2014[col_u]
 
 # Convert team variable to numeric before splitting
d.team= np.where(d.team != 'None',1,0)
y = d.team 


# 2 - Split the data into train and test sets

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=1)
train = pd.DataFrame(data=X_train, columns=[col_u ])
train['team'] = y_train
test = pd.DataFrame(data=X_test,columns=[col_u ])
test['team'] = y_test

#3 Model

logReg = LogisticRegression()
logReg.fit(X_train,y_train)
B1 = logReg.coef_[0][0] # still confused why you use [0][0]
B0 = logReg.intercept_[0]
np.exp(B1) 
#Increasing x by oen unit increases log-odds of making team by 1.02

#Evaluate Model
#Calculate Accuracy
logReg.score(X_test, y_test)# .973

#Predict
#preds = logReg.predict(X_test)

# compare to null accuracy rate
y_test.mean()
1 - y_test.mean() #.957...what does this mean? What accuracy do I get if i say that everyoen didnt make the team


#Create predictions using the model on the test set
test['pred_class'] = logReg.predict(X_test)

####Describe performance of model

# Specificity
# For those who didn't make the team, how many did it predict correctly?
test_nd = test[test.team ==0 ]
specificity = sum(test_nd.pred_class == test_nd.team) / float(len(test_nd.team))
#.994

# Sensitivity
# For those who did make the team, how many did it predict correctly? 
test_d = test[test.team == 1]
sensitivity = sum(test_d.pred_class == test_d.team) / float(len(test_d.team))





#Second model

#Can we improve sensitivity by using advance variables?
col_a = ["FTr","BLK%","TS%","STL%","AST%","3PAr","USG%",'DBPM','OBPM','BPM','PER','DWS','OWS','WS','WS/48','TOV%','TRB%']


X= d[col_a]
X_2014 = d_2014[col_a]
y = d.team

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=1)
train = pd.DataFrame(data=X_train, columns=[col_a ])
train['team'] = y_train
test = pd.DataFrame(data=X_test,columns=[col_a ])
test['team'] = y_test


logReg = LogisticRegression()
logReg.fit(train[col_a ],y_train)
B1 = logReg.coef_[0][0] # still confused why you use [0][0]
B0 = logReg.intercept_[0]
np.exp(B1) #.44

preds = logReg.predict(X_test)

#Create predictions using the model on the test set
test['pred_class'] = logReg.predict(test[col_a ])

####Describe performance of model
#Calculate Accuracy
logReg.score(X_test, y_test)# .975

# Specificity
# For those who didn't make the team, how many did it predict correctly?
test_nd = test[test.team ==0 ]
specificity = sum(test_nd.pred_class == test_nd.team) / float(len(test_nd.team))
#.994 ; improves...

# Sensitivity
# For those who did make the team, how many did it predict correctly? 
test_d = test[test.team == 1]
sensitivity = sum(test_d.pred_class == test_d.team) / float(len(test_d.team))
#senstivity decreases

#third Model
col_c= ["g","mp","fg_","ft_","orb","drb","ast","stl","blk","tov","pts",'DBPM','OBPM','PER','DWS','WS','WS/48','AST%']
#col_c = ["g","mp","fg_","ft_","orb","drb","ast","stl","blk","tov","pts",'DBPM','OBPM','PER','DWS','OWS']

X= d[col_c]
X_2014 = d_2014[col_c]
d.team= np.where(d.team != 'None',1,0)

y = d.team


X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=1)
train = pd.DataFrame(data=X_train, columns=[col_c ])
train['team'] = y_train
test = pd.DataFrame(data=X_test,columns=[col_c ])
test['team'] = y_test


logReg = LogisticRegression()
logReg.fit(train[col_c ],y_train)
B1 = logReg.coef_[0][0] # still confused why you use [0][0]
B0 = logReg.intercept_[0]
np.exp(B1) #.961

#Create predictions using the model on the test set
test['pred_class'] = logReg.predict(test[col_c ])

####Describe performance of model
#Calculate Accuracy
logReg.score(X_test, y_test)# .975

# Specificity
# For those who didn't make the team, how many did it predict correctly?
test_nd = test[test.team ==0 ]
specificity = sum(test_nd.pred_class == test_nd.team) / float(len(test_nd.team))
#.992 ;

# Sensitivity
# For those who did make the team, how many did it predict correctly? 
test_d = test[test.team == 1]
sensitivity = sum(test_d.pred_class == test_d.team) / float(len(test_d.team))
#.655

#How well did it do?
d_2014['pred2014'] = logReg.predict(d_2014[col_c])

d_2014['probs2014'] = logReg.predict_proba(d_2014[col_c])[:, 1]

df =d_2014[['player','team','pred2014','probs2014']]
null = 1 - sum(d.team) / float(len(d.team))
#Actuately predicting 8 award winners with a probablity 0f .5 or greater



#Create predictions using the model on the test set
test['pred_class'] = logReg.predict(test[col_c ])


# nicer confusion matrix
from nltk import ConfusionMatrix
print ConfusionMatrix(list(y_test), list(preds))


#229 possible yes; 57%

## ROC CURVE and AUC

#Do I want it on X_test or 2014 data?
probs = logReg.predict_proba(X_test)[:, 1]
from sklearn import metrics


# plot ROC curve
fpr, tpr, thresholds = metrics.roc_curve(y_test, probs)
plt.plot(fpr, tpr)
plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.0])
plt.xlabel('False Positive Rate (1 - Specificity)')
plt.ylabel('True Positive Rate (Sensitivity)')

# calculate AUC
print metrics.roc_auc_score(y_test, probs) #is this good?

#Cross Validation
from sklearn.cross_validation import cross_val_score

X = nbaHistoric[col_c]
y = nbaHistoric.team
logreg = LogisticRegression()
cross_val_score(logreg, X, y, cv=10, scoring='roc_auc').mean()
#.985 AUC
#.968 Accuracy




#Use supervised classification models to predict what team players are on


feat_cols =  ["g","mp","fg_","ft_","orb","drb","ast","stl","blk","tov","pts",'DBPM','OBPM','PER','DWS','OWS','WS','WS/48','AST%']
from sklearn.tree import DecisionTreeClassifier
treeclf = DecisionTreeClassifier()

nbaHistoric= NBA_players[NBA_players.season_end <= 2013]

d = nbaHistoric
d.info()
d_2014 = nba_2014


X= d[feat_cols]
X_2014 = d_2014[feat_cols]
y = nbaHistoric.team



X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=1)
train = pd.DataFrame(data=X_train, columns=[feat_cols])
train['team'] = y_train
test = pd.DataFrame(data=X_test, columns=[feat_cols])
test['team'] = y_test
treeclf.fit(X,y)

pd.DataFrame({'feature':feat_cols, 'importance':treeclf.feature_importances_})

d_2014['treepred']= treeclf.predict(d_2014[feat_cols])


#visualize decision tree
#from sklearn.tree import export_graphviz
#with open("NBA.dot", 'wb') as f:
#    f = export_graphviz(treeclf, out_file=f, feature_names=feat_cols)


    
#####################
    

from sklearn.ensemble import RandomForestClassifier
rfclf = RandomForestClassifier(n_estimators=100, max_features='auto', oob_score=True, random_state=1)
rfclf.fit(d[feat_cols], y, sample_weight = np.array([5 if i == 0 else 1 for i in y]) )
# used sample weight to address Unbalanced classification using RandomForestClassifier in sklearn but can lead to bias
pd.DataFrame({'feature':feat_cols, 'importance':rfclf.feature_importances_})

rfclf.oob_score_

d_2014['rfprd']=rfclf.predict_proba(d_2014[feat_cols])[:, 1]
d_2014['rfprd_predic']=rfclf.predict(d_2014[feat_cols])
    
df = d_2014[['player','team','treepred','rfprd_predic','pred2014', 'probs2014' ]]

#df.to_csv('project.csv')



#is it compensating for the ones that dont make the team?
# unbalanced classification: resampling but can lead to bias


###############LOG REG Model for  2015
    

nbaHistoric2= NBA_players[NBA_players.season_end <= 2014]
nba_2015= NBA_players_2015



#nbaHistoric = NBA_players[NBA_players.season_end <= 2013]

d = nbaHistoric2

#df = pd.DataFrame(logReg.coef_, columns = col_c)
#check coefs


d.team= np.where(d.team != 'None',1,0)

d.info()

d_2015 = nba_2015
d_2015.info()


X= d[col_c]
X_2015 = d_2015[col_c]
y = d.team

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=1)
train = pd.DataFrame(data=X_train, columns=[col_c ])
train['team'] = y_train
test = pd.DataFrame(data=X_test,columns=[col_c ])
test['team'] = y_test


logReg = LogisticRegression()
logReg.fit(train[col_c ],y_train)
B1 = logReg.coef_[0][0] 
B0 = logReg.intercept_[0]
np.exp(B1) #.963


preds = logReg.predict(X_test)

logReg.fit(X, y)


d_2015['pred2015'] = logReg.predict(d_2015[col_c])

d_2015['probs2015'] = logReg.predict_proba(d_2015[col_c])[:, 1]

#Why am i getting really high probabilites?
#Jack cooley??
