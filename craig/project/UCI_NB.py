# -*- coding: utf-8 -*-
"""
Created on Sat Mar 07 10:51:28 2015

@author: Craig
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Sklearn imports
from sklearn.cross_validation import train_test_split
from sklearn import metrics
from sklearn.cross_validation import cross_val_score
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB

# import a better looking Confusion matrix
from nltk import ConfusionMatrix

'''
  -- The database contains 3 potential classes, one for the number of times a
      certain type of solar flare occured in a 24 hour period.
   -- Each instance represents captured features for 1 active region on the 
X      sun.
'''


#df = pd.read_table('https://archive.ics.uci.edu/ml/machine-learning-databases/solar-flare/flare.data2', sep = ' ')

cols = ['zurich', 'penumbra', 'compactness', 'activity', 'evolution', '24_hr_activity', 'hist_complex', 'became_complex', 'area', 'area_largest_spot', 'c_class', 'm_class', 'x_class']
df = pd.read_csv('C:\\Users\\Craig\\Documents\\Python_DS\\GA_DS\\solar.csv', names = cols)
df['penumbra'] = [item.lower() for item in df.penumbra]
df['compactness'] = [item.lower() for item in df.compactness]
df['compactness'] = ['y' if item == 'x' else item for item in df.compactness]


# create a column the sums all the flare events for each instance (active region)

df['total_flares'] = df.c_class + df.m_class + df.x_class

df.describe()

len(df[df.total_flares == 0].total_flares)
len(df[df.total_flares > 0].total_flares)


print "Only %s percent of active regions produced flares." % str(float(len(df[df.total_flares > 0].total_flares))/len(df.total_flares) * 100)

# create a binary response column, 0 if no flare of any type, 1 if a flare happened for each active region

df['flare_occur'] = np.where(df.total_flares == 0, 0, 1)
df['zpc'] = df.zurich + df.penumbra + df.compactness

# Create dummy variables for sunspot classification labels 
zurich_dummy = pd.get_dummies(df.zurich).iloc[:, 1:]
penumbra_dummy = pd.get_dummies(df.penumbra).iloc[:, 1:]
compactness_dummy = pd.get_dummies(df.compactness).iloc[:, 1:]

# concatenate dummy variable to original df
df_2 = pd.concat([df, zurich_dummy, penumbra_dummy, compactness_dummy], axis = 1)

# Create an initial feature/response set.
X = df_2.iloc[:, 16:] # sunspot classifications, dummy variable for zpc
y = df_2.flare_occur # binary response.  0=no flare, 1=flare(s) measured

# Use Naive Bayes as a classifier


# Split data into test and train sets for preliminary Naive Bayes test.
X_train, X_test, y_train, y_test = train_test_split(df_2.zpc, df_2.flare_occur)

# Instantantiate the vectorizer.
vect = CountVectorizer(analyzer = 'char', lowercase = False) 
# Create document term matrices
train_dtm = vect.fit_transform(X_train)
test_dtm = vect.transform(X_test)

train_features = vect.get_feature_names()

len(train_features)
train_arr = train_dtm.toarray()

for i in range(len(train_features)):
    print train_features[i], sum(train_arr[:, i]) 

nb = MultinomialNB()
nb.fit(train_dtm, y_train)

preds= nb.predict(test_dtm)

print metrics.accuracy_score(y_test, preds)
print ConfusionMatrix(list(y_test), list(preds)) 

cross_val_score(nb, vect.fit_transform(df_2.zpc), df_2.flare_occur, cv=10, scoring='roc_auc').mean()
cross_val_score(nb, vect.fit_transform(df_2.zpc), df_2.flare_occur, cv=10, scoring='accuracy').mean()
cross_val_score(nb, vect.fit_transform(df_2.zpc), df_2.flare_occur, cv=10, scoring='recall').mean()

# False negative
X_test[y_test > preds]

'''
Revisit this using NOAA data if time permits

# Cheack with oos data
X = df_2.zpc
y = df_2.flare_occur

# Instantantiate the vectorizer.
vect = CountVectorizer(analyzer = 'char', lowercase = False) 

# Create document term matrices


nb = MultinomialNB()
nb.fit(all_dtm, y)



oos = pd.DataFrame(['Dao', 1])

X_2 = X.append(oos.iloc[0]).reset_index()
X_2 = X_2.iloc[:,1:]

# Train on all the original data
all_dtm = vect.fit_transform(X_2.iloc[0:1066])
all_features = vect.get_feature_names()

all_dtm = vect.fit_transform(X_2.iloc[0:1066])


oos_dtm = vect.fit_transform(oos[0])
oos_arr = oos_dtm.toarray()
oos_response = oos[1]
oos_features = vect.get_feature_names()

len(oos_features)
oos_arr = oos_dtm.toarray()

for i in range(len(oos_features)):
    print oos_features[i], sum(oos_arr[:, i]) 
    
    '''