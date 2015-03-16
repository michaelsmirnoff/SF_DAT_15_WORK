# -*- coding: utf-8 -*-
"""
Created on Fri Feb 20 15:03:46 2015

@author: jonbryan90
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LogisticRegression
import matplotlib.pyplot as plt
from sklearn.cross_validation import train_test_split

'''Loads the combined data for 644 drugs'''
Master_df = pd.read_csv('C:\Users\jonbryan90\Desktop\MASTER4') #alter path to run!

'''
Removes the drugs with less than 30 adverse events per year in to isolate
the drugs with a significant, albeit arbitrarily, amount of adverse events per year
'''
Master_df = Master_df[Master_df.AE_Per_Year >= 30]

'''
Removes drugs with more than += 50,000 adverse events as I treat them as outliers
'''
Master_df = Master_df[Master_df.Num_Adv_Event < 50000]

'''
Removes drugs with more than 5,000 adverse events per year as I treat them as
outliers
''''
Master_df = Master_df[Master_df.AE_Per_Year < 5000]


'''
ANALYSIS
This scatter plot illustrates that the rate of adverse event reporting is postive
and growing each year. This could be problematic for comparisons across the 'Innovation_Cat'
variable. The this trend may need to be corrected by lowering the "signficance" of 
adverse events reported after each successive year. This will be explored further.
'''
Master_df.plot(kind='scatter', x='Approval_Year', y='AE_Per_Year')

'''
ANALYSIS
The following boxplot illustrates a number of additional "outliers" at the
+15,000 level. Whether these are truly outliers or not will be determined by future
analyses
'''
Master_df.boxplot(column='Num_Adv_Event',by='Innovation_Cat')

'''
ANALYSIS
The following bar chart illustrates that there are 
151 ADDITION TO CLASS drugs
128 FIRST IN CLASS drugs
77 ADVANCE IN CLASS drugs

Because the are almost 2X ADDITION TO CLASS drugs than ADVANCE IN CLASS adjustments 
in scale and composition of column variables may be needed to render "apples-to-apples" 
comparisons possible
''''
Master_df.Innovation_Cat.value_counts().plot(kind='bar')
plt.xlabel('Innovation Category')
plt.ylabel('Frequency')

'''
ANALYSIS
This line plot illustrates that FIRST IN CLASS > ADVANCE IN CLASS > ADDITION TO CLASS
for adverse events reported per year. This result is interesting as ADVANCE IN CLASS would 
at first glance be expected to be lower than ADDTION TO CLASS because ADVANCE IN CLASS should 
include superior drugs. Onewould, however, expect FIRST IN CLASS to have the highest median 
adverse events reported as these include drugs approved with previously unused metabolic mechanisms or
pathways. 

Possible reasons that ADVANCE IN CLASS has higer adverse events reported per year could include:
-More ADVANCE IN CLASS drugs are approved more recently than ADDITION TO CLASS
-Whike ADVANCE IN CLASS drugs have higher adverse events reported per year they have supierior therapuetic 
benefit which outweigh these negatives
'''

Master_df.groupby(by='Innovation_Cat').AE_Per_Year.median().plot(kind='bar')
plt.xlabel('Innovation Category')
plt.ylabel('Median Adverse Events Per Year')
plt.show()

