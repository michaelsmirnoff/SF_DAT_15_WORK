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

from sklearn import tree
import pandas as pd
import numpy as np
from sklearn.cross_validation import train_test_split
from sklearn import metrics
import matplotlib.pyplot as plt

'''
import nltk
nltk.download('all')
'''
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
#
#

sample_cols = ["age","g", "mp", "fg", "fga", "fg_", "x3p", "x3pa", "x3p_","x2p", "x2pa", "x2p_", "efg_", "ft", "fta", "ft_", "orb","drb", "trb", "ast", "stl", "blk", "tov", "pf", "pts","TS%", "3PAr", "FTr", "ORB%", "DRB%", "TRB%", "AST%","STL%", "BLK%", "TOV%", "USG%"]

len(sample_cols) # = 36

#
# Trees for PER
#
NBA_Rookie_Stats['PER_bin'] = np.where(NBA_Rookie_Stats.PER_cond == True, 1, 0)
NBA_Rookie_Stats[['PER_bin','PER_cond']][NBA_Rookie_Stats.PER_cond == True]

X = NBA_Rookie_Stats[sample_cols]
Y = NBA_Rookie_Stats.PER_bin

# Now, split the data into training and test sets
X_train, X_test, y_train, y_test = train_test_split(X,Y, random_state=1)

# Create a decision tree classifier instance (start out with a small tree for interpretability)
ctree = tree.DecisionTreeClassifier(random_state=1, max_depth=2)

# Fit the decision tree classifier
ctree.fit(X_train, y_train)

# Create a feature vector
features = X_train.columns.tolist()
features = X_train.tolist()

features

# How to interpret the diagram?
ctree.classes_

ctree.feature_importances_
zip(sample_cols, ctree.feature_importances_)


preds = ctree.predict(X_test)

# Calculate accuracy
metrics.accuracy_score(y_test, preds)
#97.2

# Confusion matrix
matrix = pd.crosstab(y_test, preds, rownames=['actual'], colnames=['predicted'])

sensitivity = float(matrix[1][1]) / (matrix[1][0] + matrix[1][1])
# sensitivity = 0.0% 
specificity = float(matrix[0][0]) / (matrix[0][1] + matrix[0][0])
# specificity = 97.5 %
accuracy = (float(matrix[0][0]) + matrix[1][1]) / ((matrix[1][0] + matrix[1][1])+(matrix[0][1] + matrix[0][0]))
# accuracy = 97.2%

# Make predictions on the test set using predict_proba
probs = ctree.predict_proba(X_test)[:,1]

# Calculate the AUC metric
metrics.roc_auc_score(y_test, probs)
# 0.52

#Run cross val

cross_val_score(ctree, X, Y, cv=10, scoring='accuracy').mean()
# 96.6

cross_val_score(ctree, X, Y, cv=10, scoring='roc_auc').mean()
# 0.615

#
# Run against other models
#

from sklearn.naive_bayes import MultinomialNB
nb = MultinomialNB()
from sklearn.neighbors import KNeighborsClassifier  # import class
knn = KNeighborsClassifier(n_neighbors=5)           # instantiate the estimator

cross_val_score(nb, X, Y, cv=10, scoring='roc_auc').mean()
# 0.771

cross_val_score(nb, X, Y, cv=10, scoring='accuracy').mean()
# 86.8

cross_val_score(knn, X, Y, cv=10, scoring='roc_auc').mean()
# 0.668

cross_val_score(knn, X, Y, cv=10, scoring='accuracy').mean()
# 97.2


'''

FINE-TUNING THE TREE

'''
from sklearn.grid_search import GridSearchCV


# check CV score for max depth = 3
ctree = tree.DecisionTreeClassifier(max_depth=3)
np.mean(cross_val_score(ctree, X, Y, cv=5, scoring='roc_auc'))

# check CV score for max depth = 10
ctree = tree.DecisionTreeClassifier(max_depth=10)
np.mean(cross_val_score(ctree, X, Y, cv=5, scoring='roc_auc'))


# Conduct a grid search for the best tree depth
ctree = tree.DecisionTreeClassifier(random_state=1)
depth_range = range(1, 20)
param_grid = dict(max_depth=depth_range)
grid = GridSearchCV(ctree, param_grid, cv=5, scoring='roc_auc')
grid.fit(X, Y)


# Check out the scores of the grid search
grid_mean_scores = [result[1] for result in grid.grid_scores_]


# Plot the results of the grid search
plt.figure()
plt.plot(depth_range, grid_mean_scores)
plt.hold(True)
plt.grid(True)
plt.plot(grid.best_params_['max_depth'], grid.best_score_, 'ro', markersize=12, markeredgewidth=1.5,
         markerfacecolor='None', markeredgecolor='r')

# Get the best estimator
best = grid.best_estimator_

cross_val_score(best, X, Y, cv=10, scoring='roc_auc').mean()
# 0.668

cross_val_score(logreg, X, Y, cv=10, scoring='roc_auc').mean()
# 0.898


# Conduct a grid search for the best tree depth
ctree = tree.DecisionTreeClassifier(random_state=1)
depth_range = range(1, 20)
criterion_range = ['gini', 'entropy']
max_feaure_range = range(1,5)
param_grid = dict(max_depth=depth_range, criterion=criterion_range, max_features=max_feaure_range)
grid = GridSearchCV(ctree, param_grid, cv=5, scoring='roc_auc')
grid.fit(X, Y)

# Check out the scores of the grid search
grid_mean_scores = [result[1] for result in grid.grid_scores_]

# Get the best estimator

best = grid.best_estimator_

'''
calculate a cross-validated roc_auc score for the model and compare to 
# base logistic regression
'''

cross_val_score(best, X, Y, cv=10, scoring='roc_auc').mean()
# 626

cross_val_score(logreg, X, Y, cv=10, scoring='roc_auc').mean()
# 0.898

'''

Decision Tree for WS

'''

#
# Trees for PER
#
NBA_Rookie_Stats['WS_bin'] = np.where(NBA_Rookie_Stats.WS_cond == True, 1, 0)
NBA_Rookie_Stats[['WS_bin','WS_cond']][NBA_Rookie_Stats.WS_cond == True]

X = NBA_Rookie_Stats[sample_cols]
Y = NBA_Rookie_Stats.WS_bin

# Now, split the data into training and test sets
X_train, X_test, y_train, y_test = train_test_split(X,Y, random_state=1)

# Create a decision tree classifier instance (start out with a small tree for interpretability)
ctree = tree.DecisionTreeClassifier(random_state=1, max_depth=2)

# Fit the decision tree classifier
ctree.fit(X_train, y_train)

# Create a feature vector
#features = X_train.columns.tolist()
features = X_train.tolist()

features

# How to interpret the diagram?
ctree.classes_

ctree.feature_importances_
zip(sample_cols, ctree.feature_importances_)


preds = ctree.predict(X_test)

# Calculate accuracy
metrics.accuracy_score(y_test, preds)
#96.6

# Confusion matrix
matrix = pd.crosstab(y_test, preds, rownames=['actual'], colnames=['predicted'])

sensitivity = float(matrix[1][1]) / (matrix[1][0] + matrix[1][1])
# sensitivity = 25.0% 
specificity = float(matrix[0][0]) / (matrix[0][1] + matrix[0][0])
# specificity = 97.5 %
accuracy = (float(matrix[0][0]) + matrix[1][1]) / ((matrix[1][0] + matrix[1][1])+(matrix[0][1] + matrix[0][0]))
# accuracy = 96.6%

# Make predictions on the test set using predict_proba
probs = ctree.predict_proba(X_test)[:,1]

# Calculate the AUC metric
metrics.roc_auc_score(y_test, probs)
# 0.68.6

#Run cross val

cross_val_score(ctree, X, Y, cv=10, scoring='accuracy').mean()
# 96.6

cross_val_score(ctree, X, Y, cv=10, scoring='roc_auc').mean()
# 0.733

#
# Run against other models
#

from sklearn.naive_bayes import MultinomialNB
nb = MultinomialNB()
from sklearn.neighbors import KNeighborsClassifier  # import class
knn = KNeighborsClassifier(n_neighbors=5)           # instantiate the estimator

cross_val_score(nb, X, Y, cv=10, scoring='roc_auc').mean()
# 0.884

cross_val_score(nb, X, Y, cv=10, scoring='accuracy').mean()
# 86.8

cross_val_score(knn, X, Y, cv=10, scoring='roc_auc').mean()
# 0.730

cross_val_score(knn, X, Y, cv=10, scoring='accuracy').mean()
# 96.5


'''

FINE-TUNING THE TREE

'''
from sklearn.grid_search import GridSearchCV


# check CV score for max depth = 3
ctree = tree.DecisionTreeClassifier(max_depth=3)
np.mean(cross_val_score(ctree, X, Y, cv=5, scoring='roc_auc'))
# 0.787

# check CV score for max depth = 10
ctree = tree.DecisionTreeClassifier(max_depth=10)
np.mean(cross_val_score(ctree, X, Y, cv=5, scoring='roc_auc'))
# 0.594

# Conduct a grid search for the best tree depth
ctree = tree.DecisionTreeClassifier(random_state=1)
depth_range = range(1, 20)
param_grid = dict(max_depth=depth_range)
grid = GridSearchCV(ctree, param_grid, cv=5, scoring='roc_auc')
grid.fit(X, Y)


# Check out the scores of the grid search
grid_mean_scores = [result[1] for result in grid.grid_scores_]


# Plot the results of the grid search
plt.figure()
plt.plot(depth_range, grid_mean_scores)
plt.hold(True)
plt.grid(True)
plt.plot(grid.best_params_['max_depth'], grid.best_score_, 'ro', markersize=12, markeredgewidth=1.5,
         markerfacecolor='None', markeredgecolor='r')

# Get the best estimator
best = grid.best_estimator_

cross_val_score(best, X, Y, cv=10, scoring='roc_auc').mean()
# 0.807

cross_val_score(logreg, X, Y, cv=10, scoring='roc_auc').mean()
# 0.922


# Conduct a grid search for the best tree depth
ctree = tree.DecisionTreeClassifier(random_state=1)
depth_range = range(1, 20)
criterion_range = ['gini', 'entropy']
max_feaure_range = range(1,5)
param_grid = dict(max_depth=depth_range, criterion=criterion_range, max_features=max_feaure_range)
grid = GridSearchCV(ctree, param_grid, cv=5, scoring='roc_auc')
grid.fit(X, Y)

# Check out the scores of the grid search
grid_mean_scores = [result[1] for result in grid.grid_scores_]

# Get the best estimator

best = grid.best_estimator_

'''
calculate a cross-validated roc_auc score for the model and compare to 
# base logistic regression
'''

cross_val_score(best, X, Y, cv=10, scoring='roc_auc').mean()
# 0.858

cross_val_score(best, X, Y, cv=10, scoring='accuracy').mean()
# 96.3

cross_val_score(logreg, X, Y, cv=10, scoring='roc_auc').mean()
# 0.922

file_name = 'C:\Users\Nick\Desktop\GA\SF_DAT_15_WORK\Project\First_Draft\data\One.csv'
NBA_Rookie_Stats.to_csv(file_name,index=False)