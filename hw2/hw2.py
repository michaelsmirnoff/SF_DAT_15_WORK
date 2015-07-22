# -*- coding: utf-8 -*-
"""
Created on Thu Jul 16 01:07:53 2015

SF_DAT_15 HW2

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


import nltk
nltk.download('all')


##### Part 1 #####


# 1. read in the yelp dataset

git_yelp_data = 'https://raw.githubusercontent.com/sinanuozdemir/SF_DAT_15/master/hw/optional/yelp.csv'

YelpData = pd.read_csv(git_yelp_data)

YelpData.columns

# 2. Perform a linear regression using 
# "stars" as your response and 
# "cool", "useful", and "funny" as predictors

feature_cols = ['cool','useful','funny']

X = YelpData[feature_cols]
y = YelpData.stars

linreg = LinearRegression()

X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=1)

linreg.fit(X_train, y_train)
    
#y_pred = linreg.predict(X)
#y_true = y

zip(feature_cols, linreg.coef_)
''' Co-efs
cool:    0.2634
useful: -0.1471
funny: - 0.1289
'''

# 3. Show your MAE, R_Squared and RMSE

#R_Squared:
lm = smf.ols(formula='stars ~ cool + useful + funny', data=YelpData).fit()
lm.rsquared
#  R_Squared: 0.0442

y_pred = linreg.predict(X_test)

#MAE:
print metrics.mean_absolute_error(y_test, y_pred)
# MAE = 0.9471

#RMSE:
print np.sqrt(metrics.mean_squared_error(y_test, y_pred))
# RMSE = 1.1842

# 4. Use statsmodels to show your pvalues
# for each of the three predictors
# Using a .05 confidence level, 
# Should we eliminate any of the three?

lm = smf.ols(formula='stars ~ cool + useful + funny', data=YelpData).fit()
lm.pvalues 
'''
Cool:   2.988e-90
Useful: 1.205e-39
Funny:  1.850e-43
'''

lm = smf.ols(formula='stars ~ cool', data=YelpData).fit()
lm.pvalues #Nearly 0  1.425e-07

lm = smf.ols(formula='stars ~ useful', data=YelpData).fit()
lm.pvalues #   0.0188

lm = smf.ols(formula='stars ~ funny', data=YelpData).fit()
lm.pvalues # Nearly 0  8.48e-10

#Useful has the least correlation but is still a strong predictor 

# 5. Create a new column called "good_rating"
# this could column should be True iff stars is 4 or 5
# and False iff stars is below 4

YelpData['good rating'] = YelpData['stars'].apply(lambda x: True if x > 3 else False)


# 6. Perform a Logistic Regression using 
# "good_rating" as your response and the same
# three predictors

Cond_y = YelpData['good rating']

X_train, X_test, y_train, y_test = train_test_split(X, Cond_y, random_state=1)
logreg = LogisticRegression()
logreg.fit(X_train, y_train)

Yelp_Prediction = logreg.predict(X_test)
matrix = metrics.confusion_matrix(y_test, Yelp_Prediction)

'''  Confusion Matrix
        [[ 51,  733],
         [ 38, 1678]]

'''

# 7. Show your Accuracy, Sensitivity, Specificity
# and Confusion Matrix

sensitivity = float(matrix[1][1]) / (matrix[1][0] + matrix[1][1])
# sensitivity = 97.7% 
specificity = float(matrix[0][0]) / (matrix[0][1] + matrix[0][0])
# specificity = 6.5 %
accuracy = (float(matrix[0][0]) + matrix[1][1]) / ((matrix[1][0] + matrix[1][1])+(matrix[0][1] + matrix[0][0]))
# accuracy = 69.1%

# 8. Perform one NEW operation of your 
# choosing to try to boost your metrics!

#YelpData['good rating'] = YelpData['stars'].apply(lambda x: True if x > 3 else False)
YelpData['useful_cool'] = (YelpData['cool'] >= 1) & (YelpData['useful'] >= 1)


Cond_y = YelpData['useful_cool']

X_train, X_test, y_train, y_test = train_test_split(X, Cond_y, random_state=1)
logreg = LogisticRegression()
logreg.fit(X_train, y_train)

Yelp_Prediction = logreg.predict(X_test)
matrix = metrics.confusion_matrix(y_test, Yelp_Prediction)

'''  Confusion Matrix
        [[ 1602, 16],
         [ 0,   882]]

'''

sensitivity = float(matrix[1][1]) / (matrix[1][0] + matrix[1][1])
# sensitivity = 100% 
specificity = float(matrix[0][0]) / (matrix[0][1] + matrix[0][0])
# specificity = 99.0 %
accuracy = (float(matrix[0][0]) + matrix[1][1]) / ((matrix[1][0] + matrix[1][1])+(matrix[0][1] + matrix[0][0]))
# accuracy = 99.4%

##### Part 2 ######

# 1. Read in the titanic data set.

git_titanic_data = 'https://raw.githubusercontent.com/sinanuozdemir/SF_DAT_15/master/data/titanic.csv'
titanic_data = pd.read_csv(git_titanic_data, index_col='PassengerId')

titanic_data.columns

# 4. Create a new column called "wife" that is True
# if the name of the person contains Mrs.
# AND their SibSp is at least 1

titanic_data['Wife'] = (titanic_data['Name'].str.contains("Mrs.", na=False) & titanic_data['SibSp'] >= 1)

#titanic_data.Name[titanic_data.SibSp == 1][titanic_data.Name.str.contains("Mrs.", na=False)]

titanic_data[['Wife','Name']]

# 5. What is the average age of a male and
# the average age of a female on board?

avg_male_age = titanic_data.Age[titanic_data.Sex == 'male'].mean()
#Male Age = 30.73 years
avg_female_age = titanic_data.Age[titanic_data.Sex == 'female'].mean()
#Female Age = 27.92 years

# 5. Fill in missing MALE age values with the
# average age of the remaining MALE ages

titanic_data[titanic_data.Sex == 'male'].Age.isnull().sum()
# Males with null ages = 124
titanic_data.Age[titanic_data.Sex == 'female'].isnull().sum()
# Females with null ages = 53

#drinks.fillna(value='NA')   
#ufo.Colors.fillna(value='Unknown', inplace=True)
titanic_data[titanic_data.Sex == 'male'].Age.fillna(value=avg_male_age, inplace=True)



# 6. Fill in missing FEMALE age values with the
# average age of the remaining FEMALE ages

titanic_data[titanic_data.Sex == 'female'].Age.fillna(value=avg_female_age, inplace=True)


#drinks.fillna(value='NA')   
#titanic.Age[titanic_data.Sex == 'female'].fillna(avg_male_age, inplace=True)


# 7. Perform a Logistic Regression using
# Survived as your response and 
#age, wife as predictors

feature_cols = ['Age','Wife']

X = titanic_data[feature_cols]
y = titanic_data.Survived

X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=1)
logreg = LogisticRegression()
logreg.fit(X_train, y_train)

Titanic_Prediction = logreg.predict(X_test)
matrix = metrics.confusion_matrix(y_test, Titanic_Prediction)

'''  Confusion Matrix
        [[ ###, ###],
         [ ###, ###]]

'''

# 8. Show Accuracy, Sensitivity, Specificity and 
# Confusion matrix

sensitivity = float(matrix[1][1]) / (matrix[1][0] + matrix[1][1])
# sensitivity =  %
specificity = float(matrix[0][0]) / (matrix[0][1] + matrix[0][0])
# specificity =  %
accuracy = (float(matrix[0][0]) + matrix[1][1]) / ((matrix[1][0] + matrix[1][1])+(matrix[0][1] + matrix[0][0]))
# accuracy =  %

# 9. now use ANY of your variables as predictors
# Still using survived as a response to boost metrics!

feature_cols = ['Age','Wife','Pclass','Sex']

X = titanic_data[feature_cols]
y = titanic_data.Survived

X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=1)
logreg = LogisticRegression()
logreg.fit(X_train, y_train)

Titanic_Prediction = logreg.predict(X_test)
matrix = metrics.confusion_matrix(y_test, Titanic_Prediction)

'''  Confusion Matrix
        [[ ###, ###],
         [ ###, ###]]

'''

# 10. Show Accuracy, Sensitivity, Specificity

sensitivity = float(matrix[1][1]) / (matrix[1][0] + matrix[1][1])
# sensitivity =  %
specificity = float(matrix[0][0]) / (matrix[0][1] + matrix[0][0])
# specificity =  %
accuracy = (float(matrix[0][0]) + matrix[1][1]) / ((matrix[1][0] + matrix[1][1])+(matrix[0][1] + matrix[0][0]))
# accuracy =  %
