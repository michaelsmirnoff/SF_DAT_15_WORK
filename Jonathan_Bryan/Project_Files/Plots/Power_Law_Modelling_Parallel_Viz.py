# -*- coding: utf-8 -*-
"""
Created on Tue Mar 10 18:27:58 2015

@author: jonbryan90
"""

import pandas as pd
import scipy as sp
import numpy as np
import matplotlib.pyplot as plt

Master_df = pd.read_csv('C:\Users\jonbryan90\Desktop\MASTER5_NoNA')

Add_Adv_df = Master_df[Master_df.Innovation_Cat != 2]
Add_Fir_df = Master_df[Master_df.Innovation_Cat != 1]
Adv_Fir_df = Master_df[Master_df.Innovation_Cat != 0]


Histo = Master_df.Num_Adv_Event.value_counts()
Histo = Histo.sort_index()
Histo.plot(loglog=True, title='Log-Log Histogram')


c, loc, scale = sp.stats.lomax.fit(Master_df.Num_Adv_Event)
x = np.linspace(stats.lomax.ppf(0.01, c),
                stats.lomax.ppf(0.99, c), 100)
log_x = np.log10(x)
mean, var, skew, kurt = stats.lomax.stats(c,loc=loc, scale=scale, moments='mvsk')                
plt.plot(x, stats.lomax.pdf(x, c, loc=loc),'r-', lw=5, alpha=0.6, label='lomax pdf')


#Generate randome data points using the estimated parameters
model_lomax = stats.lomax.rvs(c, loc=loc, scale=scale, size=644)
#Change random numbers to intergers for easier plotting
model_lomax = map(int,model_lomax)
#Change from list to df
model_lomax = pd.DataFrame(model_lomax, columns=['Random'])
#Remove really big values by keeping the max = Master_df.Num_Adv_Event max
model_lomax = model_lomax[model_lomax < Master_df.Num_Adv_Event.max()]
#Generate histogram
model_lomax.hist(bins=100)
plt.title('Lomax Random Numbers, Exponent = 0.45')
#Generate histogram of original Num_Adv_Event data for comparison
plt.hist(Master_df.Num_Adv_Event, bins=100, color='Orange',)
plt.title('Num_Adv_Event')

#Even though data has really fat tails I do a correlation matrix anyway
Corr_matrix = Master_df.corr()
Corr_matrix.to_html()

#Standardize columns and do parallel coordinates
from pandas.tools.plotting import parallel_coordinates
from sklearn.preprocessing import StandardScaler
Numerical_Add_Adv = Add_Adv_df
Numerical_Add_Adv = Numerical_Add_Adv.drop(['Unnamed: 0', 'Unnamed: 0.1', 
                        'Unnamed: 0.1','Unnamed: 0.1.1',
                        'Approval_Year','Trade_Name', 
                        'Active_Ing','Lan_Drug_Class',
                        'FDA_Drug_Class','Innovation_Cat',
                        'Top_25', 'Norm_Adv_Event'], axis=1)
scaler = StandardScaler()
scaler.fit(Numerical_Add_Adv)
X_scaled = scaler.transform(Numerical_Add_Adv)
X_scaled = pd.DataFrame(X_scaled, columns=['Num_Adv_Event','Num_Serious',
                                            'Num_Other','Num_Life_Threat',
                                            'Num_Hosp','Num_Congen_Anom',
                                            'Num_Disable','Num_Deaths',
                                            'Num_Male','Num_Female',
                                            'AE_Per_Year','Adj_Num_AE',
                                            'Adj_Per_Year'])
reindexed_Ino_Cat = Add_Adv_df.Innovation_Cat.reset_index(drop=True)                                         
X_scaled['Innovation_Cat'] = reindexed_Ino_Cat
parallel_coordinates(X_scaled, 'Innovation_Cat')