# -*- coding: utf-8 -*-
"""
Created on Mon Feb 23 17:59:56 2015

@author: Craig M. Lennon
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Sklearn imports
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.cross_validation import train_test_split
from sklearn import metrics
from sklearn.cross_validation import cross_val_score
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn import svm

# import a better looking Confusion matrix
from nltk import ConfusionMatrix

'''
  -- The database contains 3 potential classes, one for the number of times a
      certain type of solar flare occured in a 24 hour period.
   -- Each instance represents captured features for 1 active region on the 
      sun.
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

set(df[df.total_flares == 0].zpc).difference(set(df[df.total_flares > 0].zpc))
set(df[df.total_flares > 0].zpc).difference(set(df[df.total_flares == 0].zpc)) # types of sunspot that always flare

# plot a bar plot of types of spots
df.zpc.value_counts().plot(kind='bar')

# plot mean number of each flare class for each type of spot
df.groupby('zpc').c_class.mean().plot(kind='bar')
df.groupby('zpc').m_class.mean().plot(kind='bar')  # look at Dkc spots
df.groupby('zpc').x_class.mean().plot(kind='bar') # look at Dkc spots


# Create a list that represents each active region observation, but in arb. units
instance = range(len(df.zpc))

# Create a plot of C, M, and X flares versus active region
# The size of the points increases by an order of magnitude for C, M, X

p1 = plt.scatter(instance, df.c_class, s=5, c = 'blue', alpha = 0.5, label = 'C')
p2 = plt.scatter(instance, df.m_class, s=50, c = 'red', alpha = 0.5, label = 'M')
p3 = plt.scatter(instance, df.x_class, s=500, c = 'yellow', alpha = 0.5, label = 'X')
plt.ylim(.5, 10)
plt.xlim(0 , 1058)
plt.ylabel('Flare Count')
plt.xlabel('Active Region (Arbitrary Units)')
plt.legend(loc='upper right', shadow=False, scatterpoints = 1)

# Create dummy variables for sunspot classification labels 
zurich_dummy = pd.get_dummies(df.zurich).iloc[:, 1:]
penumbra_dummy = pd.get_dummies(df.penumbra).iloc[:, 1:]
compactness_dummy = pd.get_dummies(df.compactness).iloc[:, 1:]

# concatenate dummy variable to original df
df_2 = pd.concat([df, zurich_dummy, penumbra_dummy, compactness_dummy], axis = 1)

# Create an initial feature/response set.
X = df_2.iloc[:, 16:] # sunspot classifications, dummy variable for zpc
y = df_2.flare_occur # binary response.  0=no flare, 1=flare(s) measured

# Train test split for quick model evaluation.
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state = 1)

# Try logistic regression
logreg = LogisticRegression()
logreg.fit(X_train, y_train)
preds = logreg.predict(X_test)
logreg.score(X_test, y_test) # 0.835 but there are A LOT of non-flaring sunspots, the true negative rate is >> than the true positive rate making accuracy a poor metric
1 - logreg.score(X_test, y_test) # misclassification rate is low, but this is due to the large number of non-flaring instances.
metrics.recall_score(y_test, preds) # a sensitivity of only 0.1458, this is bad.  When a flare occurs it is only predicted 14.5% of the time
metrics.precision_score(y_test, preds) # 70% of the time the model is right if it does predict a flare
print ConfusionMatrix(list(y_test), list(preds)) 

cross_val_score(logreg, X_test, y_test, cv=10, scoring='roc_auc').mean()
cross_val_score(logreg, X_test, y_test, cv=10, scoring='accuracy').mean()
cross_val_score(logreg, X_test, y_test, cv=10, scoring='recall').mean()

probs = logreg.predict_proba(X_test)[:, 1]

# plot the roc auc curve
roc_auc_curve(y_test, probs) # roc auc is 0.798


# Add additional predictors
# For now always use zpc dummies and anything from  df_2.iloc[:, 3:10]

# The winning combination of predictors are all the zpc dummies, became_complex, activity, and 24_hr_activity

X = pd.concat([ df_2.iloc[:, 16:], df_2.iloc[:, 3:10]], axis = 1)
# X = pd.concat([ df_2.iloc[:, 16:], df_2.iloc[:, 7], df_2.activity, df_2.iloc[:,5]], axis = 1) # best thus far
y = df_2.flare_occur # binary response.  0=no flare, 1=flare(s) measured

# Train test split for quick model evaluation.
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state = 1)

# Repeat logistic regression
logreg = LogisticRegression()
logreg.fit(X_train, y_train)
preds = logreg.predict(X_test)
logreg.score(X_test, y_test) #
1 - logreg.score(X_test, y_test) #
metrics.recall_score(y_test, preds) 
metrics.precision_score(y_test, preds) 
print ConfusionMatrix(list(y_test), list(preds)) 

cross_val_score(logreg, X_test, y_test, cv=10, scoring='roc_auc').mean()
cross_val_score(logreg, X_test, y_test, cv=10, scoring='accuracy').mean()
cross_val_score(logreg, X_test, y_test, cv=10, scoring='recall').mean()

probs = logreg.predict_proba(X_test)[:, 1]

# plot the roc auc curve
roc_auc_curve(y_test, probs) 

# McIntosh classifications for active regions that produced x class flares.
df_2[df_2.x_class >0].zpc

# Decision Tree classifier

# Create an initial feature/response set.
X = df_2.iloc[:, 16:] # sunspot classifications, dummy variable for zpc
X = pd.concat([ df_2.iloc[:, 16:], df_2.iloc[:, 7], df_2.activity, df_2.iloc[:,5]], axis = 1)
y = df_2.flare_occur # binary response.  0=no flare, 1=flare(s) measured

# Train test split for quick model evaluation.
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state = 1)


# fit a classification tree
treeclf = DecisionTreeClassifier(max_depth = 4, random_state = 2)
treeclf.fit(X_train, y_train)
treeclf.score(X_test, y_test)

preds = treeclf.predict(X_test)

cross_val_score(treeclf, X_test, y_test, cv=10, scoring='roc_auc').mean()
cross_val_score(treeclf, X_test, y_test, cv=10, scoring='accuracy').mean()
cross_val_score(treeclf, X_test, y_test, cv=10, scoring='recall').mean()

preds = treeclf.predict(X_test)
print ConfusionMatrix(list(y_test), list(preds)) 


probs = treeclf.predict_proba(X_test)[:, 1]

# plot the roc auc curve
roc_auc_curve(y_test, probs) 

pd.DataFrame({'Feature':X.columns, 'Importance':treeclf.feature_importances_}) # Zurich = F, penumbra = k (most important), compactness = o


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

probs = nb.predict_proba(test_dtm)[:,1]
roc_auc_curve(y_test, probs) 

# SVM attempt, with dummy variables for zpc and numeric zpc values

X = df_2.iloc[:, 16:] # sunspot classifications, dummy variable for zpc
X = pd.concat([ df_2.iloc[:, 16:], df_2.iloc[:, 7], df_2.activity, df_2.iloc[:,5]], axis = 1)
y = df_2.flare_occur # binary response.  0=no flare, 1=flare(s) measured

# Train test split for quick model evaluation.
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state = 1)
clf = svm.SVC()
clf.fit(X_train, y_train)
clf.score(X_test, y_test)
clf.predict(X_test)

cross_val_score(clf, X_test, y_test, cv=10, scoring='roc_auc').mean()
cross_val_score(clf, X_test, y_test, cv=10, scoring='accuracy').mean()
cross_val_score(clf, X_test, y_test, cv=10, scoring='recall').mean()


# Assign numeric values to zpc classes (http://spaceweather.inf.brad.ac.uk/library/publications/solarphysic1.pdf)
df_3 = df
df_3['zurich'] = df_3.zurich.map({'A':0.1, 'H':0.15, 'B':0.3, 'C':0.45, 'D':0.6, 'E':0.75, 'F':0.9})
df_3['penumbra'] = df_3.penumbra.map({'x':0, 'r':0.1, 's':0.3, 'a':0.5, 'h':0.7, 'k':0.9})
df_3['compactness'] = df_3.compactness.map({'y':0, 'o':0.1, 'i':0.5, 'c':0.9})
df_3['flare_occur'] = df_3.flare_occur.map({0.1:0, 0.9:1})

X = df_3.iloc[:, 0:3] # sunspot classifications, dummy variable for zpc
#X = pd.concat([ df_2.iloc[:, 16:], df_2.iloc[:, 7], df_2.activity, df_2.iloc[:,5]], axis = 1)
y = df_3.flare_occur # binary response.  0=no flare, 1=flare(s) measured

# Train test split for quick model evaluation.
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state = 1)
clf = svm.SVC()
clf.fit(X_train, y_train)
clf.score(X_test, y_test)
clf.predict(X_test)

cross_val_score(clf, X_test, y_test, cv=10, scoring='roc_auc').mean()
cross_val_score(clf, X_test, y_test, cv=10, scoring='accuracy').mean()
cross_val_score(clf, X_test, y_test, cv=10, scoring='recall').mean()


# SVM does not perform well.  Looks like NB wins


#################Function definitions#########################

def roc_auc_curve(test_response, probability):
        
    fpr, tpr, thresholds = metrics.roc_curve(test_response, probability)
    roc_auc = metrics.auc(fpr, tpr)
    print "Area under the ROC curve : %f" % roc_auc

    # Plot ROC curve
    plt.clf()
    plt.plot(fpr, tpr, label='ROC curve (area = %0.5f)' % roc_auc)
    plt.plot([0, 1], [0, 1], 'k--')
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.0])
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('Receiver operating characteristic')
    plt.legend(loc="lower right")
    plt.show()
    