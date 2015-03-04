# -*- coding: utf-8 -*-
"""
Created on Mon Feb 16 20:35:35 2015

@author: deronhogans
"""

import pandas as pd
import numpy as np
from sklearn.neighbors import KNeighborsClassifier
import matplotlib.pyplot as plt
from sklearn.cross_validation import train_test_split
from sklearn.cross_validation import cross_val_score
from sklearn.grid_search import GridSearchCV
from sklearn.linear_model import LogisticRegression
# Read in the packages you'll be using for your data work

trips = pd.DataFrame.from_csv('2PointB_January_Trips.csv', sep= ",", header=0, index_col=0)
# Read Trips into a dataframe

trips
# Let's take a look at the data frame to see what the data looks like

trips.describe()
# Mixed data types: strings, integers
# About 65% of trips in January were completed
# The average trip cost/gross amount was $12.52 
# The average dscount applied to a trip was $9.85 

trips['Status'] = trips.Status.map({'Meter Off': 1, 'Unable to Auth': 0, 'Cancelled':-1})
# To make for eassier work with our data, I will transform all data into integers
# I've started with Status
# 'Meter Off' is valued as +1 to reflect a completed trip
# 'Unable to Auth' valued at 0 to reflect an incomplete transaction
# "Cancelled' is valued as -1 to reflect a cancelled trip

trips.Trip_Adjusted = trips.Trip_Adjusted.map({'Yes': 1, 'No': 0})
# Transforming Trip Adjustment to reflect Positive (1) or Negative (0) affirmation

trips.Existing_Passenger = trips.Existing_Passenger.map({'Yes': 1, 'No': 0})
# Doing a similar transformation to Existing Passenger

trips.Fleet = trips.Fleet.map({'Discount Cab': 1, 'Cab': 2, 'Black': 4, 'Ridehare': 3, 'SUV': 5})
# Final transformation for values
# Discount Cab = 1 
# Cab = 2 
# Black = 4 
# Rideshare = 3
# SUV = 5
# Black Car and SUV are rated highest as they are the most valuable

trips
# lets see what our data looks like now

FullTrips = trips.dropna()
# Saw a lot of missing values, will set FullTrips = to a trips without missing values

FullTrips.plot(kind='scatter', x='Existing_Passenger', y='Discount_Applied', alpha=0.3)
#

FullTrips.plot(kind='scatter', x='Gross_Amount', y='Discount_Applied', alpha=0.3)

FullTrips.plot(kind='scatter', x='Fleet', y='Discount_Applied', alpha=0.3)

FullTrips.plot(kind='scatter', x='Status', y='Discount_Applied', alpha=0.3)

FullTripsSelect = pd.DataFrame({'Fleet': FullTrips['Fleet'],'Gross_Amount': FullTrips['Gross_Amount'],'Trip_Adjusted': FullTrips['Trip_Adjusted'], 'Existing_Passenger': FullTrips['Existing_Passenger']})

Gross_AmountDF = pd.DataFrame({'Gross_Amount': FullTrips['Gross_Amount']})

X, y = FullTripsSelect, FullTrips.Discount_Applied
knn = KNeighborsClassifier(n_neighbors=1)
knn.fit(X, y)
knn.score(X, y)
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=4)
X_train.shape
X_test.shape
y_train.shape
y_test.shape

knn = KNeighborsClassifier(n_neighbors=1)
knn.fit(X_train, y_train)
knn.score(X_test, y_test)

knn = KNeighborsClassifier(n_neighbors=5)
knn.fit(X_train, y_train)
knn.score(X_test, y_test)

knn = KNeighborsClassifier(n_neighbors=3)
knn.fit(X_train, y_train)
knn.score(X_test, y_test)

knn = KNeighborsClassifier(n_neighbors=5)
knn.fit(X, y)
out_of_sample = [1, 1, 72, 0]
knn.predict(out_of_sample)

knn = KNeighborsClassifier(n_neighbors=5)
scores = cross_val_score(knn, X, y, cv=5, scoring='accuracy')
scores
np.mean(scores)

k_range = range(1, 30, 2)
param_grid = dict(n_neighbors=k_range)
grid = GridSearchCV(knn, param_grid, cv=5, scoring='accuracy')
grid.grid_scores_
grid_mean_scores = [result[1] for result in grid.grid_scores_]
plt.figure()
plt.plot(k_range, grid_mean_scores)
grid.best_score_
grid.best_params_
grid.best_estimator_

knn = KNeighborsClassifier(n_neighbors=9)
scores = cross_val_score(knn, X, y, cv=9, scoring='accuracy')
scores
np.mean(scores)

knn = KNeighborsClassifier(n_neighbors=5)
knn.fit(X, y)
out_of_sample = [1, 3, 10, 0]
knn.predict(out_of_sample)

total_cost = LogisticRegression()
total_cost.fit(X_train, y_train)
B1 = total_cost.coef_[0][0]
B0 = total_cost.intercept_[0]
np.exp(B1)
prob = total_cost.predict(pd.DataFrame({'Gross_Amount': [10, 25, 50, 70]}))
x = np.linspace(Gross_A.min(), test.total_cost.max(),500)
beta = [B0,B1]

y = np.exp(beta[0] + beta[1]*x) / (1 + np.exp(beta[0] + beta[1]*x))
odds = np.exp(beta[0] + beta[1]*x)
log_odds = beta[0] + beta[1]*x