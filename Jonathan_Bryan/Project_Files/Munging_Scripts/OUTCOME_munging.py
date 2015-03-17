# -*- coding: utf-8 -*-
"""
Created on Sun Feb 15 22:26:49 2015

@author: jonbryan90
"""


import pandas as pd
import numpy as np



'''
FAERS OUTCOME.csv data retrieval
'''
 
#Script to populate Outcome_df dataframe from 2004Q1-2011Q4
years = range(4,12)
qtrs = range(1,5)
Outcome_df = pd.DataFrame()
for year in years:
    for qtr in qtrs:
        path ='C:\Users\jonbryan90\Documents\OUTCOME\OUTC%dQ%d.txt' % (year,qtr)
        frame = pd.read_csv(path, names=['ISR','OUTC_COD', 'YEAR','QTR'], sep='$', skiprows=1, low_memory=False, skipinitialspace=True)
        frame['YEAR'] = 2000 + int(year)
        frame['QTR'] = qtr
        Outcome_df = Outcome_df.append(frame, ignore_index=True)
        
#Script to populate Outcome_df2 dataframe from 2012Q1-2012Q3
years = 12
qtrs = range(1,4)
Outcome_df2 = pd.DataFrame()
for qtr in qtrs:
    path ='C:\Users\jonbryan90\Documents\OUTCOME\OUTC%dQ%d.txt' % (years,qtr)
    frame = pd.read_csv(path, names=['ISR','OUTC_COD', 'YEAR','QTR'], sep='$', skiprows=1, low_memory=False, skipinitialspace=True)
    frame['YEAR'] = 2012
    frame['QTR'] = qtr
    Outcome_df2 = Outcome_df2.append(frame, ignore_index=True)

#Append Outcome_df2 to Outcome_df
Outcome_df = Outcome_df.append(Outcome_df2, ignore_index=True)

#Script to populate Outcome_df3 dataframe from 2012Q4
years = 12
qtr = 4
Outcome_df3 = pd.DataFrame()
path ='C:\Users\jonbryan90\Documents\OUTCOME\OUTC%dQ%d.txt' % (years,qtr)
frame = pd.read_csv(path, names=['primaryid','caseid','OUTC_COD','YEAR','QTR'], sep='$', skiprows=1, skipinitialspace=True,low_memory=False)
frame['YEAR'] = 2000 + int(years)
frame['QTR'] = qtr
Outcome_df3 = Outcome_df3.append(frame, ignore_index=True)
   
        
#Script to populate Outcome_df4 dataframe from 2013Q1-2014Q2
years = range(13,15)
qtrs = range(1,5)
Outcome_df4 = pd.DataFrame()
for year in years:
    for qtr in qtrs:
        if year == 14 and qtr == 3:
            break
        else:
            path ='C:\Users\jonbryan90\Documents\OUTCOME\OUTC%dQ%d.txt' % (year,qtr)
            frame = pd.read_csv(path, names=['primaryid','caseid','OUTC_COD','YEAR','QTR'], sep='$', skiprows=1, skipinitialspace=True,low_memory=False)
            frame['YEAR'] = 2000 + int(year)
            frame['QTR'] = qtr
            Outcome_df4 = Outcome_df4.append(frame, ignore_index=True)
        

#Drop a caseid
Outcome_df3 = Outcome_df3.drop(['caseid'], 1)         
Outcome_df4 = Outcome_df4.drop(['caseid'], 1) 
#Rename primaryid to ISR
Outcome_df3 = Outcome_df3.rename(columns={'primaryid': 'ISR'})
Outcome_df4 = Outcome_df4.rename(columns={'primaryid': 'ISR'})
#Append Outcome_df3 to Outcome_df
Outcome_df = Outcome_df.append(Outcome_df3, ignore_index=True)
Outcome_df = Outcome_df.append(Outcome_df4, ignore_index=True)
#Write Outcome_df to CSV
Outcome_df.to_csv('C:\Users\jonbryan90\Desktop\OUTCOME_MASTER2')