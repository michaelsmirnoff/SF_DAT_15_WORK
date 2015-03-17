# -*- coding: utf-8 -*-
"""
Created on Sat Mar 07 16:11:15 2015

@author: jonbryan90
"""

import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
import matplotlib.pyplot as plt
from sklearn.cross_validation import train_test_split

'''
Load Master_df
'''
Master_df = pd.read_csv('C:\Users\jonbryan90\Desktop\Master5_NoNA')

'''
Converts all words in the 'Innovation_Column to uppercase and then numeral 0,1,2
'''
Master_df.Innovation_Cat = Master_df.Innovation_Cat.replace(to_replace=['ADDITION TO CLASS',
                                             'ADVANCE IN CLASS',
                                             'FIRST IN CLASS'], value=[0,1,2])
                                             
'''
Removes First-in-class drugs and puts remaining drugs into Add_Adv_df
'''
Add_Adv_df = Master_df[Master_df.Innovation_Cat != 2]

'''
Populate Adj_Per_Year Column
'''
Add_Adv_df['Adj_Per_Year'] = Add_Adv_df.Adj_Num_AE / (2014 - Add_Adv_df.Approval_Year)


'''
Split the data into train and test sets
'''
X = Add_Adv_df[['Num_Adv_Event','Num_Serious',
                'Num_Other','Num_Life_Threat','Num_Hosp',
                'Num_Congen_Anom','Num_Disable','Num_Deaths',
                'Num_Male','Num_Female','AE_Per_Year','Adj_Num_AE', 'Adj_Per_Year']]
y = Add_Adv_df.Innovation_Cat
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=1)

''' Convert them back into dataframes, for convenience '''
train = pd.DataFrame(data=X_train, columns=['Num_Adv_Event','Num_Serious',
                'Num_Other','Num_Life_Threat','Num_Hosp',
                'Num_Congen_Anom','Num_Disable','Num_Deaths',
                'Num_Male','Num_Female','AE_Per_Year','Adj_Num_AE', 'Adj_Per_Year'])
train['Innovation_Cat'] = y_train
test = pd.DataFrame(data=X_test, columns=['Num_Adv_Event','Num_Serious',
                'Num_Other','Num_Life_Threat','Num_Hosp',
                'Num_Congen_Anom','Num_Disable','Num_Deaths',
                'Num_Male','Num_Female','AE_Per_Year','Adj_Num_AE', 'Adj_Per_Year'])
test['Innovation_Cat'] = y_test


''''Logistic Regression'''

Comp = LogisticRegression()
Comp.fit(X_train, y_train)
B1 = Comp.coef_[0][0]
B0 = Comp.intercept_[0]
np.exp(B1)


Optimum = LogisticRegression()
Optimum.fit(train[['Num_Adv_Event','Num_Life_Threat','Num_Deaths',
                'Num_Male','Num_Female','Adj_Per_Year']], y_train)
B1_2 = Optimum.coef_[0][0]
B0_2 = Optimum.intercept_[0]
np.exp(B1_2)

Adj_Num_AE = LogisticRegression()
Adj_Num_AE.fit(train[['Adj_Num_AE']], y_train)
B1_3 = Adj_Num_AE.coef_[0][0]
B0_3 = Adj_Num_AE.intercept_[0]
np.exp(B1_3)

Num_Congen_Anom = LogisticRegression()
Num_Congen_Anom.fit(train[['Num_Congen_Anom']], y_train)
B1_4 = Num_Congen_Anom.coef_[0][0]
B0_4 = Num_Congen_Anom.intercept_[0]
np.exp(B1_4)

Num_Disable = LogisticRegression()
Num_Disable.fit(train[['Num_Disable']], y_train)
B1_5 = Num_Disable.coef_[0][0]
B0_5 = Num_Disable.intercept_[0]
np.exp(B1_5)

Num_Deaths = LogisticRegression()
Num_Deaths.fit(train[['Num_Deaths']], y_train)
B1_6 = Num_Deaths.coef_[0][0]
B0_6 = Num_Deaths.intercept_[0]
np.exp(B1_6)

# What does beta mean? Let's create some plots to find out!
x = np.linspace(test.Adj_Num_AE.min(), test.Adj_Num_AE.max(),500)
beta = [B0_2,B1_2]

y = np.exp(beta[0] + beta[1]*x) / (1 + np.exp(beta[0] + beta[1]*x))
odds = np.exp(beta[0] + beta[1]*x)
log_odds = beta[0] + beta[1]*x

prob = Adj_Per_Year.predict(pd.DataFrame({'Adj_Per_Year': [1200, 2500]}))

# 3 - Plot the fitted logistic function overtop of the data points
plt.figure()
plt.scatter(test.Num_Deaths, test.Innovation_Cat, alpha=0.1, s=30)
plt.plot(x, y, 'r', linewidth=2)
plt.xlabel("Adj_Num_AE")
plt.ylabel("Probability Innovation Category is Advance-in-Class")

plt.figure(figsize=(7, 8))
plt.subplot(311)
plt.plot(x, y, 'r', linewidth=2)
plt.ylabel('Probability')
plt.text(500, 0.7, r'$\frac{e^{\beta_o + \beta_1x}}{1+e^{\beta_o + \beta_1x}}$', fontsize=25)

plt.subplot(312)
plt.plot(x, odds, 'k', linewidth=2)
plt.ylabel('Odds')
plt.text(500, 10, r'$e^{\beta_o + \beta_1x}$', fontsize=20)

plt.subplot(313)
plt.plot(x, log_odds, 'c', linewidth=2)
plt.ylabel('Log(Odds)')
plt.xlabel('x')
plt.text(500, 1, r'$\beta_o + \beta_1x$', fontsize=15)

# 3 - Plot the fitted logistic function overtop of the data points
plt.figure()
plt.scatter(test.Adj_Num_AE, test.Innovation_Cat, alpha=0.1, s=30)
plt.plot(x, y, 'r', linewidth=2)
plt.xlabel("")
plt.ylabel("Probability Innovation Category is Advance-in-Class")
plt.plot([1200, 2500], prob, 'ko')

# 4 - Create predictions using the balance model on the test set
test['pred_class'] = Adj_Num_AE.predict(test[['Adj_Num_AE']])

# 5 - Compute the overall accuracy, the sensitivity and specificity
# Accuracy
accuracy = sum(test.pred_class == test.Innovation_Cat) / float(len(test.Innovation_Cat))

# Specificity
# For those who didn't default, how many did it predict correctly?
test_nd = test[test.Innovation_Cat == 0]
specificity = sum(test_nd.pred_class == test_nd.Innovation_Cat) / float(len(test_nd.Innovation_Cat))

# Sensitivity
# For those who did default, how many did it predict correctly? 
test_d = test[test.Innovation_Cat == 1]
sensitivity = sum(test_d.pred_class == test_d.Innovation_Cat) / float(len(test_d.Innovation_Cat))

# This raises the question, how does our overall 
# classification accuracy compare to the not-default rate?
null = 1 - sum(Add_Adv_df.Innovation_Cat) / float(len(Add_Adv_df.Innovation_Cat))

