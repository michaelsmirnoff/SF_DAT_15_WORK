# -*- coding: utf-8 -*-
"""
Created on Sun Mar 01 12:36:37 2015

@author: jonbryan90
"""

import pandas as pd
from pandas.tools.plotting import parallel_coordinates
import matplotlib.pyplot as plt
import scipy as sp
import scipy.stats as stats

'''
Testing if the data follows a normal distribution
'''

sp.stats.mstats.normaltest(Master_df.Num_Adv_Event)
sp.stats.mstats.normaltest(Master_df.Num_Serious)
sp.stats.mstats.normaltest(Master_df.Num_Other)
sp.stats.mstats.normaltest(Master_df.Num_Life_Threat)
sp.stats.mstats.normaltest(Master_df.Num_Hosp)
sp.stats.mstats.normaltest(Master_df.Num_Congen_Anom)
sp.stats.mstats.normaltest(Master_df.Num_Disable)
sp.stats.mstats.normaltest(Master_df.Num_Deaths)
sp.stats.mstats.normaltest(Master_df.Num_Male)
sp.stats.mstats.normaltest(Master_df.Num_Female)
sp.stats.mstats.normaltest(Master_df.AE_Per_Year)
sp.stats.mstats.normaltest(Master_df.Adj_Num_AE)
sp.stats.mstats.normaltest(Master_df.Adj_Per_Year)

'''
Correlation matrix

RESULT: Num_Adv_Event is highly correlated (>0.60 with every other column
except for Num_Congen_Anom, Num_Disable and Num_Deaths
'''
Corr_matrix = Master_df.corr()
Corr_matrix.to_csv('C:\Users\jonbryan90\Desktop\Corr_Matrix')

#Count total number of drugs in each Innovation_Cat
Master_df[Master_df.Innovation_Cat==0].Trade_Name.count()
Master_df[Master_df.Innovation_Cat==1].Trade_Name.count()
Master_df[Master_df.Innovation_Cat==2].Trade_Name.count()

#Percentage of total adverse events by Innovation Class | NON-ADJUSTED
total_AE = Master_df.Num_Adv_Event.sum()
Addition_AE = Master_df[Master_df.Innovation_Cat == 0].Num_Adv_Event.sum()
Advanced_AE = Master_df[Master_df.Innovation_Cat == 1].Num_Adv_Event.sum()
First_AE = Master_df[Master_df.Innovation_Cat == 2].Num_Adv_Event.sum()
percent_Add_AE = Addition_AE/float(total_AE)
percent_Adv_AE = Advanced_AE/float(total_AE)
percent_Fir_AE = First_AE/float(total_AE)

#Percentage of total adverse events by Innovation Class | 2004 Adjusted
total_Adj = Master_df.Adj_Num_AE.sum()
Addition_Adj = Master_df[Master_df.Innovation_Cat == 0].Adj_Num_AE.sum()
Advanced_Adj = Master_df[Master_df.Innovation_Cat == 1].Adj_Num_AE.sum()
First_Adj = Master_df[Master_df.Innovation_Cat == 2].Adj_Num_AE.sum()
percent_Add_Adj = Addition_Adj/float(total_Adj)
percent_Adv_Adj = Advanced_Adj/float(total_Adj)
percent_Fir_Adj = First_Adj/float(total_Adj)

Master_df.groupby('Innovation_Cat').Num_Serious.sum() / Master_df.Num_Serious.sum()
Master_df.groupby('Innovation_Cat').Num_Other.sum() / Master_df.Num_Other.sum()
Master_df.groupby('Innovation_Cat').Num_Life_Threat.sum() / Master_df.Num_Life_Threat.sum()
Master_df.groupby('Innovation_Cat').Num_Hosp.sum() / Master_df.Num_Hosp.sum()
Master_df.groupby('Innovation_Cat').Num_Congen_Anom.sum() / Master_df.Num_Congen_Anom.sum()
Master_df.groupby('Innovation_Cat').Num_Disable.sum() / Master_df.Num_Disable.sum()
Master_df.groupby('Innovation_Cat').Num_Deaths.sum() / Master_df.Num_Deaths.sum()
Master_df.groupby('Innovation_Cat').Num_Male.sum() / Master_df.Num_Male.sum()
Master_df.groupby('Innovation_Cat').Num_Female.sum() / Master_df.Num_Female.sum()




'''
PLOTS
'''
'''
Creates a df with only the numerical columns for a scatter matrix

RESULT: Nearly all of the independent variables follow some sort of power law distribution
'''
Numerical_df = Master_df[['Num_Adv_Event','Num_Serious',
                'Num_Other','Num_Life_Threat','Num_Hosp',
                'Num_Congen_Anom','Num_Disable','Num_Deaths',
                'Num_Male','Num_Female','AE_Per_Year','Adj_Num_AE', 'Adj_Per_Year']]

pd.scatter_matrix(Numerical_df, diagonal='kde')

'''
Correlation matrix

RESULT: Num_Adv_Event is highly correlated (>0.60 with every other column
except for Num_Congen_Anom, Num_Disable and Num_Deaths
'''
Corr_matrix = Master_df.corr()
Corr_matrix.to_csv('C:\Users\jonbryan90\Desktop\Corr_Matrix')

'''
Density plots by Innovation_Cat for the promising variabes (Num_Adv_Event, Num_Congen, Num_Disabe, Num_Deaths)
'''
Master_df.groupby('Innovation_Cat').Num_Adv_Event.plot(kind='kde',
                                                      linewidth=2.5, 
                                                      xlim = (0,Master_df.Num_Adv_Event.max()),
                                                      legend=True,
                                                      title='Density Plot of Total Adverse Events')

Master_df.groupby('Innovation_Cat').Num_Congen_Anom.plot(kind='kde',
                                                      linewidth=2.5,
                                                      xlim = (0,Master_df.Num_Congen_Anom.max()),
                                                      legend=True,
                                                      title='Density Plot of Total Congen Anom')
 
Master_df.groupby('Innovation_Cat').Num_Disable.plot(kind='kde',
                                                      linewidth=2.5,
                                                      legend=True,
                                                      xlim = (0,Master_df.Num_Disable.max()),
                                                      title='Density Plot of Total Disable')
 
Master_df.groupby('Innovation_Cat').Num_Deaths.plot(kind='kde',
                                                      linewidth=2.5,
                                                      legend=True,
                                                      xlim = (0,Master_df.Num_Disable.max()),
                                                      title='Density Plot of Total Deaths')



#Analysis of optimum regressors Num_Adv_Event, Num_Life_Threat, Num, Deaths
ax_X = Master_df[Master_df.Innovation_Cat == 0].plot(kind='scatter', 
                                                    x='Num_Adv_Event',
                                                    y='Num_Life_Threat',
                                                    label='Addition-to-Class',
                                                    s=50,
                                                    fontsize=80)
                                                    
ax_Y = Master_df[Master_df.Innovation_Cat == 1].plot(kind='scatter', 
                                                    x='Num_Adv_Event',
                                                    y='Num_Life_Threat',
                                                    label='Advance-in-Class',
                                                    color='Orange',
                                                    s=50,
                                                    fontsize=80,
                                                    ax=ax_X)
Master_df[Master_df.Num_Deaths > 5000][Master_df.Num_Life_Threat > 2000][Master_df.Num_Adv_Event>50000]
                                                    










ax_1 = Master_df[Master_df.Innovation_Cat == 0].plot(kind='scatter', 
                                                    x='Num_Adv_Event',
                                                    y='AE_Per_Year',
                                                    label='Addition-to-Class',
                                                    s=50,
                                                    fontsize=80)
                                                    
ax_2 = Master_df[Master_df.Innovation_Cat == 1].plot(kind='scatter', 
                                                    x='Num_Adv_Event',
                                                    y='AE_Per_Year',
                                                    label='Advance-in-Class',
                                                    color='Orange',
                                                    s=50,
                                                    fontsize=80,
                                                    ax=ax_1)
                                                    
Master_df[Master_df.Innovation_Cat == 2].plot(kind='scatter', 
                                                    x='Num_Adv_Event',
                                                    y='AE_Per_Year',
                                                    label='First-in-Class',
                                                    color='Green',
                                                    s=50,
                                                    fontsize=80,
                                                    ax=ax_2)

###

ax_3 = Master_df[Master_df.Innovation_Cat == 0].plot(kind='scatter', 
                                                    x='Adj_Num_AE',
                                                    y='Adj_Per_Year',
                                                    label='Addition-to-Class',
                                                    s=100,
                                                    fontsize=100)
                                                    
ax_4 = Master_df[Master_df.Innovation_Cat == 1].plot(kind='scatter', 
                                                    x='Adj_Num_AE',
                                                    y='Adj_Per_Year',
                                                    label='Advance-in-Class',
                                                    color='Orange',
                                                    s=100,
                                                    fontsize=100,
                                                    ax=ax_3)
                                                    
Master_df[Master_df.Innovation_Cat == 2].plot(kind='scatter', 
                                                    x='Adj_Num_AE',
                                                    y='Adj_Per_Year',
                                                    label='First-in-Class',
                                                    color='Green',
                                                    s=100,
                                                    fontsize=100,
                                                    ax=ax_4)

###
Trun_Master_df = Master_df[Master_df.Adj_Num_AE < 20000][Master_df.Adj_Per_Year < 2000]
ax_5 = Trun_Master_df[Trun_Master_df.Innovation_Cat == 0].plot(kind='scatter', 
                                                    x='Adj_Num_AE',
                                                    y='Adj_Per_Year',
                                                    label='Addition-to-Class',
                                                    s=100,
                                                    fontsize=100)
                                                    
ax_6 = Trun_Master_df[Trun_Master_df.Innovation_Cat == 1].plot(kind='scatter', 
                                                    x='Adj_Num_AE',
                                                    y='Adj_Per_Year',
                                                    label='Advance-in-Class',
                                                    color='Orange',
                                                    s=100,
                                                    fontsize=100,
                                                    ax=ax_5)
                                                    
Trun_Master_df[Trun_Master_df.Innovation_Cat == 2].plot(kind='scatter', 
                                                    x='Adj_Num_AE',
                                                    y='Adj_Per_Year',
                                                    label='First-in-Class',
                                                    color='Green',
                                                    s=100,
                                                    fontsize=100,
                                                    ax=ax_6)
###
Trun_Master2_df = Trun_Master_df[Trun_Master_df.Adj_Per_Year > 30]
ax_6 = Trun_Master2_df[Trun_Master2_df.Innovation_Cat == 0].plot(kind='scatter', 
                                                    x='Adj_Num_AE',
                                                    y='Adj_Per_Year',
                                                    label='Addition-to-Class',
                                                    s=100,
                                                    fontsize=100)
                                                    
ax_7 = Trun_Master2_df[Trun_Master2_df.Innovation_Cat == 1].plot(kind='scatter', 
                                                    x='Adj_Num_AE',
                                                    y='Adj_Per_Year',
                                                    label='Advance-in-Class',
                                                    color='Orange',
                                                    s=100,
                                                    fontsize=100,
                                                    ax=ax_6)
                                                    
Trun_Master2_df[Trun_Master2_df.Innovation_Cat == 2].plot(kind='scatter', 
                                                    x='Adj_Num_AE',
                                                    y='Adj_Per_Year',
                                                    label='First-in-Class',
                                                    color='Green',
                                                    s=100,
                                                    fontsize=100,
                                                    ax=ax_7)
###
Trun_Master2_df = Trun_Master_df[Trun_Master_df.Adj_Per_Year > 30]
ax_8 = Trun_Master2_df[Trun_Master2_df.Innovation_Cat == 0].plot(kind='scatter', 
                                                    x='Adj_Num_AE',
                                                    y='Adj_Per_Year',
                                                    label='Addition-to-Class',
                                                    s=100,
                                                    fontsize=100)
                                                    
ax_9 = Trun_Master2_df[Trun_Master2_df.Innovation_Cat == 1].plot(kind='scatter', 
                                                    x='Adj_Num_AE',
                                                    y='Adj_Per_Year',
                                                    label='Advance-in-Class',
                                                    color='Orange',
                                                    s=100,
                                                    fontsize=100,
                                                    ax=ax_8)
                                                    
Trun_Master2_df[Trun_Master2_df.Innovation_Cat == 2].plot(kind='scatter', 
                                                    x='Adj_Num_AE',
                                                    y='Adj_Per_Year',
                                                    label='First-in-Class',
                                                    color='Green',
                                                    s=100,
                                                    fontsize=100,
                                                    ax=ax_9)
###
ax_10 = Master_df[Master_df.Innovation_Cat == 0].plot(kind='scatter', 
                                                    x='Num_Congen_Anom',
                                                    y='Num_Deaths',
                                                    label='Addition-to-Class',
                                                    s=100,
                                                    fontsize=100)
                                                    
ax_11 = Master_df[Master_df.Innovation_Cat == 1].plot(kind='scatter', 
                                                    x='Num_Congen_Anom',
                                                    y='Num_Deaths',
                                                    label='Advance-in-Class',
                                                    color='Orange',
                                                    s=100,
                                                    fontsize=100,
                                                    ax=ax_10)
                                                    
Master_df[Master_df.Innovation_Cat == 2].plot(kind='scatter', 
                                                    x='Adj_Num_AE',
                                                    y='Num_Deaths',
                                                    label='First-in-Class',
                                                    color='Green',
                                                    s=100,
                                                    fontsize=100,
                                                    ax=ax_11)
###
ax_12 = Master_df[Master_df.Innovation_Cat == 0].plot(kind='scatter', 
                                                    x='Num_Disable',
                                                    y='Num_Deaths',
                                                    label='Addition-to-Class',
                                                    s=100,
                                                    fontsize=100)
                                                    
ax_13 = Master_df[Master_df.Innovation_Cat == 1].plot(kind='scatter', 
                                                    x='Num_Disable',
                                                    y='Num_Deaths',
                                                    label='Advance-in-Class',
                                                    color='Orange',
                                                    s=100,
                                                    fontsize=100,
                                                    ax=ax_12)
                                                
Master_df[Master_df.Innovation_Cat == 2].plot(kind='scatter', 
                                                    x='Adj_Num_AE',
                                                    y='Num_Hosp',
                                                    label='First-in-Class',
                                                    color='Green',
                                                    s=100,
                                                    fontsize=100,
                                                    ax=ax_13)
###
ax_14 = Master_df[Master_df.Innovation_Cat == 0].plot(kind='scatter', 
                                                    x='Num_Disable',
                                                    y='Num_Congen_Anom',
                                                    label='Addition-to-Class',
                                                    s=100,
                                                    fontsize=100)
                                                    
ax_15 = Master_df[Master_df.Innovation_Cat == 1].plot(kind='scatter', 
                                                    x='Num_Disable',
                                                    y='Num_Congen_Anom',
                                                    label='Advance-in-Class',
                                                    color='Orange',
                                                    s=100,
                                                    fontsize=100,
                                                    ax=ax_14)
                                                    
Master_df[Master_df.Innovation_Cat == 2].plot(kind='scatter', 
                                                    x='Num_Hosp',
                                                    y='Num_Disable',
                                                    label='First-in-Class',
                                                    color='Green',
                                                    s=100,
                                                    fontsize=100,
                                                    ax=ax_15)

Master_df[Master_df.Num_Hosp > 20000][Master_df.Num_Deaths > 5000][Master_df.Innovation_Cat==1]





Master_df.plot(kind='scatter',
               x='Num_Adv_Event',
               y='AE_Per_Year',
               colormap='seismic',
               c=Master_df.Innovation_Cat,
               s=50,
               legend=True,
               title='') #NEW TOO

Master_df.plot(kind='scatter',
               x='Adj_Num_AE',
               y='Adj_Per_Year',
               colormap='seismic',
               c=Master_df.Innovation_Cat,
               s=50,
               legend=True,
               title='')
               
Master_df.plot(kind='scatter',
               x='Adj_Num_AE',
               y='Num_Deaths',
               colormap='seismic',
               c=Master_df.Innovation_Cat,
               s=50,
               legend=True,
               title='') #NEW TOO

Master_df.Innovation_Cat.value_counts().plot(kind='bar') #ADD BAR LABELS


Master_df.Num_Adv_Event.hist(bins=100,
                             label='Frequency of Total Adverse Events')
                           
Master_df.Num_Adv_Event.plot(kind='kde', 
                             linewidth=3,
                             xlim = (0,Master_df.Num_Adv_Event.max()),
                             title='Density Plot of Total Adverse Events')
       
Master_df.groupby('Innovation_Cat').Num_Adv_Event.plot(kind='kde',
                                                      linewidth=2.5, 
                                                      xlim = (0,Master_df.Num_Adv_Event.max()),
                                                      legend=True,
                                                      title='Density Plot of Total Adverse Events')
 
Master_df.plot(kind='scatter',
               x='Num_Adv_Event',
               y='AE_Per_Year',
               colormap='Blues',
               c=Master_df.Innovation_Cat,
               s=50,
               legend=True,
               title='Density Plot of Total Adverse Events')
 
Master_df.AE_Per_Year.plot(kind='kde', 
                             linewidth=3,
                             xlim = (0,Master_df.AE_Per_Year.max()),
                             title='Density Plot of Adverse Events Reported Per Year ')

Histo = Master_df.Num_Adv_Event.value_counts()
Histo = Histo.sort_index()
Histo.plot(loglog=True)



r = sp.stats.lomax.rvs(c,size=1000)             
r = pd.DataFrame(r, columns=['Random'])
                                        
x,q,c = sp.stats.lomax.fit(Master_df.Num_Male)
mean, var, skew, kurt = sp.stats.lomax.stats(c,moments='mvsk')
x = np.linspace(sp.stats.lomax.ppf(0.001,c), sp.stats.lomax.ppf(0.999, c), 2000)
lomax_pdf = sp.stats.lomax.pdf(x,c)
plt.plot(x,lomax_pdf)


sp.stats.lomax.pdf(x,c)

ax =
ax.plot(x, lomax.pdf(x, c),'r-', lw=5, alpha=0.6, label='lomax pdf')
                      



               
ax_A = Master_df.plot(kind='scatter', 
               x='Approval_Year', 
               y='Num_Adv_Event',
               color='Blue',
               s=30,
               title='Scatterplot of Total Adverse Events by Approval Year')
Master_df.plot(kind='scatter', 
               x='Approval_Year', 
               y='Adj_Num_AE',
               color='Orange',
               s=30,
               ax = ax_A,
               title='Scatterplot of Total Adjusted (2004) Adverse Events by Approval Year')
               
Master_df.Num_Adv_Event.plot(kind='density', 
                             xlim=(0,400000))
Add_Adv_df.plot(kind='scatter', 
               x='Num_Adv_Event', 
               y='AE_Per_Year',
               colormap='Blues',
               c=Add_Adv_df.Innovation_Cat,
               fontsize=3,
               title=' ')
    







           
Numerical_df['Innovation_Cat'] = Master_df.Innovation_Cat
Numerical_df.append(Master_df.iloc[:,6])
pd.scatter_matrix(Numerical_df)







'''
Num_Adv_Event:
Gengamma D = 0.052
Genpareto D = 0.10
Log-Laplace = 0.093
Lomax = 0.10
'''

cdfs = [
    "norm",            #Normal (Gaussian)
    "alpha",           #Alpha
    "beta",            #Beta
    "betaprime",       #Beta Prime
    "cauchy",          #Cauchy
    "chi",             #Chi
    "chi2",            #Chi-squared
    "expon",           #Exponential
    "exponweib",       #Exponentiated Weibull
    "exponpow",        #Exponential Power
    "f",               #F (Snecdor F)
    "fisk",            #Fisk
    "gausshyper",      #Gauss Hypergeometric
    "genexpon",        #Generalized Exponential
    "genextreme",      #Generalized Extreme Value
    "gengamma",        #Generalized gamma
    "genlogistic",     #Generalized Logistic
    "genpareto",       #Generalized Pareto
    "genhalflogistic", #Generalized Half Logistic
    "halfcauchy",      #Half Cauchy
    "halflogistic",    #Half Logistic
    "halfnorm",        #Half Normal
    "hypsecant",       #Hyperbolic Secant
    "invgamma",        #Inverse Gamma
    "invweibull",      #Inverse Weibull
    "johnsonsb",       #Johnson SB
    "johnsonsu",       #Johnson SU
    "laplace",         #Laplace
    "logistic",        #Logistic
    "loggamma",        #Log-Gamma
    "loglaplace",      #Log-Laplace (Log Double Exponential)
    "lognorm",         #Log-Normal
    "lomax",           #Lomax (Pareto of the second kind)
    "maxwell",         #Maxwell
    "mielke",          #Mielke's Beta-Kappa
    "nakagami",        #Nakagami
    "ncx2",            #Non-central chi-squared
    "ncf",             #Non-central F
    "nct",             #Non-central Student's T
    "pareto",          #Pareto
    "powerlaw",        #Power-function
    "powerlognorm",    #Power log normal
    "powernorm",       #Power normal
    "rdist",           #R distribution
    "reciprocal",      #Reciprocal
    "rayleigh",        #Rayleigh
    "rice",            #Rice
    "recipinvgauss",   #Reciprocal Inverse Gaussian
    "semicircular",    #Semicircular
    "t",               #Student's T
    "triang",          #Triangular
    "truncexpon",      #Truncated Exponential
    "truncnorm",       #Truncated Normal
    "tukeylambda",     #Tukey-Lambda
    "uniform",]      #uniform
New = Master_df[Master_df.Adj_Num_AE < 20000]


sample = Master_df.Num_Adv_Event

for cdf in cdfs:
    #fit our data set against every probability distribution
    parameters = eval("stats."+cdf+".fit(sample)");
 
    #Applying the Kolmogorov-Smirnof one sided test
    D, p = stats.kstest(sample, cdf, args=parameters);
 
    #pretty-print the results
    print cdf.ljust(16) + ("p: "+str(p)).ljust(25)+"D: "+str(D);
