# -*- coding: utf-8 -*-
"""
Created on Fri Feb 27 14:44:16 2015

@author: jonbryan90
"""
import pandas as pd
import numpy as np

PS_df = pd.read_csv('C:\Users\jonbryan90\Desktop\DRUGS_PS_MASTER')
Index_df = pd.DataFrame()
Index_df['YEAR'] = range(2004,2015)
Index_df['YEAR_AE'] = 0
Index_df['AEI'] = 0.0

for index, row in Index_df.iterrows():
    print index + row
    Year_Count = PS_df[PS_df.YEAR == row.YEAR].ISR.count()
    row.YEAR_AE =  Year_Count
 
'''
Creates an index of the total number of AE recorded each year in "2004 AEs"
'''
   
start = float(Index_df.YEAR_AE[0])
for index, row in Index_df.iterrows():
    AEI = float(Index_df.YEAR_AE[index]) / start
    Index_df.AEI[index] = AEI


Index_df.to_csv('C:\Users\jonbryan90\Desktop\Index_MASTER')

'''
Populate Adj_Num_AE Column
'''
years = range(2004,2015)
Master_df['Adj_Num_AE'] = 0.0
for year in years:
    for index, row in Master_df.iterrows():
        string = row['Trade_Name']
        adj_AE = Master_df['Adj_Num_AE'][index]
        new_AE = Drug_PS_df[Drug_PS_df.YEAR == year].DRUGNAME.str.contains(string, case=False).sum()
        adj_AE = new_AE/Index_df[Index_df.YEAR == year].AEI + adj_AE
        Master_df['Adj_Num_AE'][index] = adj_AE
        print string + ' ' + str(Master_df['Adj_Num_AE'][index]) + ' ' + str(year)

'''
Populate Adj_Per_Year Column
'''
Master_df['Adj_Per_Year'] = Master_df.Adj_Num_AE / (2014 - Master_df.Approval_Year)