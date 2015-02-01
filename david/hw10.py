'''
## Class 10 Homework: Model Evaluation

Practice what we've learned in class using the [Glass Identification Data Set](http://archive.ics.uci.edu/ml/datasets/Glass+Identification). This is due by midnight on Sunday.

* Part 1:
    * Read the data into a DataFrame.
    * Briefly explore the data to make sure the DataFrame matches your expectations.
    * Create a new column called 'binary' that maps the glass type from 7 classes to 2 classes:
        * If type of glass = 1/2/3/4, binary = 0.
        * If type of glass = 5/6/7, binary = 1.
* Part 2:
    * Create 'X' using all features, and create 'y' using the binary column.
        * Don't use the ID number or the glass type as features!
    * Split X and y into training and test sets.
* Part 3:
    * Fit a logistic regression model on your training set, and make predictions on your test set.
    * Print the confusion matrix.
    * Calculate the accuracy and compare it to the null accuracy rate.
    * Calculate the AUC.
* Part 4:
    * Use cross-validation (with AUC as the scoring metric) to compare these three models:
        * logistic regression
        * KNN (K = 1)
        * KNN (K = 3)
* Part 5 (Optional):
    * Explore the data to see if any features look like good predictors.
    * Use cross-validation to compare a model with a smaller set of features with your best model from Part 4.

7. Attribute Information:
   1. Id number: 1 to 214
   2. RI: refractive index
   3. Na: Sodium (unit measurement: weight percent in corresponding oxide, as
                  are attributes 4-10)
   4. Mg: Magnesium
   5. Al: Aluminum
   6. Si: Silicon
   7. K: Potassium
   8. Ca: Calcium
   9. Ba: Barium
  10. Fe: Iron
  11. Type of glass: (class attribute)
      -- 1 building_windows_float_processed
      -- 2 building_windows_non_float_processed
      -- 3 vehicle_windows_float_processed
      -- 4 vehicle_windows_non_float_processed (none in this database)
      -- 5 containers
      -- 6 tableware
      -- 7 headlamps
'''

import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
import matplotlib.pyplot as plt
from sklearn.cross_validation import train_test_split
from sklearn.cross_validation import cross_val_score
#set headers for the dataframe
headers = ['ID num', 'Ref Index', 'Sodium', 'Mag', 'Alum', 'Silicon', 'Potas', 'Calcium', 'Barium', 'Iron', 'Type']
#read data from CSV into the dataframe
glass_data = pd.read_csv('/Users/roellk/Desktop/Python/DAT4-students/david/glass.data', header=None, names=headers)
glass_data.columns = headers

#basic data exploration
print 'type\n', "*"*10
#print type(glass_data)
print 'head\n', "*"*10
print glass_data.head()
print 'shape\n', "*"*10
print glass_data.shape
print 'describe\n', "*"*10
#print glass_data.describe
print 'dtypes\n', "*"*10
print glass_data.dtypes
print 'values\n', "*"*10
#print glass_data.values

#add a binary column to the dataframe for holding glass types 1-4 and 5-7
glass_data['binary'] = 1
glass_data.loc[glass_data.Type.between(1, 4), 'binary'] = 0
glass_data.loc[glass_data.Type.between(5, 7), 'binary'] = 1
print glass_data.head()
#print glass_data[(glass_data.Type > 2) & (glass_data.Type < 7)]


#part 2
X = glass_data[['Ref Index', 'Sodium', 'Mag', 'Alum', 'Silicon', 'Potas', 'Calcium', 'Barium', 'Iron', 'Type']]
y = glass_data.binary

print X.shape
print y.shape
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=1)


#part 3
#fit the model
LR = LogisticRegression()
LR.fit(X_train, y_train)
B1 = LR.coef_[0][0]
B0 = LR.intercept_[0]
print B1, "B1", B0, "B0"
print np.exp(B1), "significant? Yes, I believe so."

prob = LR.score(X_test, y_test)
print prob, "model accuracy score"
#make predictions
preds = LR.predict(X_test)
print "Predictions for X_test\n", preds
print "Actual y_test\n", y_test

# predict in one step, calculate accuracy in a separate step
from sklearn import metrics
print "accuracy score\n", metrics.accuracy_score(y_test, preds)

#null accuracy rate
print "y_test mean\n", y_test.mean()
print "1-y_test mean\n", 1-y_test.mean()

print metrics.confusion_matrix(y_test, preds)
from nltk import ConfusionMatrix
print ConfusionMatrix(list(y_test), list(preds))


# predict probabilities
import matplotlib.pyplot as plt
probs = LR.predict_proba(X_test)[:, 1]
plt.hist(probs)
plt.show()

# plot ROC curve
fpr, tpr, thresholds = metrics.roc_curve(y_test, probs)
plt.plot(fpr, tpr)
plt.xlim([0.0, 2.0])
plt.ylim([0.0, 2.0])
plt.xlabel('False Positive Rate (1 - Specificity)')
plt.ylabel('True Positive Rate (Sensitivity)')
plt.show()

#calculate AUC
print "AUC: ",metrics.roc_auc_score(y_test, probs)

#refit model with all data
LR.fit(X, y)
#prob = LR.predict(pd.DataFrame({'Ref Index' : 1.522, 'Sodium' : 13.1, 'Mag' : 3.70, 'Alum' : 1.13, 'Silicon' : 73, 'Potas' : .55, 'Calcium' : 8.77, 'Barium' : 0, 'Iron' : 0 , 'Type' : 2}))
#print prob

# part 4
#compare models LogReg, KNN-1, KNN-3

#Logistic Regression Model
logreg = LogisticRegression()
print cross_val_score(logreg, X, y, cv=3, scoring='roc_auc')

#KNN - 1
from sklearn.neighbors import KNeighborsClassifier
knn = KNeighborsClassifier(n_neighbors=1)
print cross_val_score(knn, X, y, cv=3, scoring='roc_auc').mean()

#KNN - 3
knn = KNeighborsClassifier(n_neighbors=3)
print cross_val_score(knn, X, y, cv=3, scoring='roc_auc').mean()

'''
X = data[['balance']]
y = data.default
logreg = LogisticRegression()
cross_val_score(logreg, X, y, cv=10, scoring='roc_auc').mean()

# compare to a model with an additional feature
X = data[['balance', 'income']]
cross_val_score(logreg, X, y, cv=10, scoring='roc_auc').mean()

'''

