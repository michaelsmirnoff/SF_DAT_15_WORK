# -*- coding: utf-8 -*-
"""
Created on Tue Feb 03 17:40:25 2015

@author: jonbryan90
"""

import pandas as pd
import numpy np

'''
FAERS DRUG.csv data retrieval
'''
 
#Script to populate Drug_df dataframe from 2004Q1-2011Q4
years = range(4,12)
qtrs = range(1,5)
Drug_df = pd.DataFrame()
for year in years:
    for qtr in qtrs:
        path ='C:\Users\jonbryan90\Documents\DRUG\\DRUG%dQ%d.txt' % (year,qtr)
        frame = pd.read_csv(path, names=['ISR','DRUG_SEQ','ROLE_COD','DRUGNAME','VAL_VBM','ROUTE','DOSE_VBM','DECHAL','RECHAL','LOT_NUM','EXP_DT','NDA_NUM','YEAR','QTR'], sep='$', skiprows=1, low_memory=False, skipinitialspace=True)
        frame['YEAR'] = 2000 + int(year)
        frame['QTR'] = qtr
        Drug_df = Drug_df.append(frame, ignore_index=True)

#Script to populate Drug_df2 dataframe from 2012Q1-2012Q3
years = 12
qtrs = range(1,4)
Drug_df2 = pd.DataFrame()
for qtr in qtrs:
    path ='C:\Users\jonbryan90\Documents\DRUG\\DRUG%dQ%d.txt' % (years,qtr)
    frame = pd.read_csv(path, names=['ISR','DRUG_SEQ','ROLE_COD','DRUGNAME','VAL_VBM','ROUTE','DOSE_VBM','DECHAL','RECHAL','LOT_NUM','EXP_DT','NDA_NUM','YEAR','QTR'], sep='$', skiprows=1, low_memory=False, skipinitialspace=True)
    frame['YEAR'] = 2012
    frame['QTR'] = qtr
    Drug_df2 = Drug_df2.append(frame, ignore_index=True)

#Append Drug_df2 to Drug_df
Drug_df = Drug_df.append(Drug_df2, ignore_index=True)

#Script to populate Drug_df3 dataframe from 2012Q4
year = 12
qtr = 4
Drug_df3 = pd.DataFrame()
path ='C:\Users\jonbryan90\Documents\DRUG\\DRUG%dQ%d.txt' % (year,qtr)
frame = pd.read_csv(path, names=['PRIMARYID','CASEID','DRUG_SEQ','ROLE_COD','DRUGNAME','VAL_VBM','ROUTE','DOSE_VBM','CUM_DOSE_CHR','CUM_DOSE_UNIT','DECHAL','RECHAL','LOT_NUM','EXP_DT','NDA_NUM','DOSE_AMT','DOSE_UNIT','DOSE_FORM','DOSE_FREQ','YEAR','QTR'], sep='$', skiprows=1, skipinitialspace=True,low_memory=False)
frame['YEAR'] = 2000 + int(year)
frame['QTR'] = qtr
Drug_df3 = Drug_df3.append(frame, ignore_index=True)

#Script to populate Drug_df4 dataframe from 2013Q1-2014Q2
years = range(13,15)
qtrs = range(1,5)
Drug_df4 = pd.DataFrame()
for year in years:
    for qtr in qtrs:
        if year == 14 and qtr == 3:
            break
        else:
            path ='C:\Users\jonbryan90\Documents\DRUG\\DRUG%dQ%d.txt' % (year,qtr)
            frame = pd.read_csv(path, names=['PRIMARYID','CASEID','DRUG_SEQ','ROLE_COD','DRUGNAME','VAL_VBM','ROUTE','DOSE_VBM','CUM_DOSE_CHR','CUM_DOSE_UNIT','DECHAL','RECHAL','LOT_NUM','EXP_DT','NDA_NUM','DOSE_AMT','DOSE_UNIT','DOSE_FORM','DOSE_FREQ','YEAR','QTR'], sep='$', skiprows=1, skipinitialspace=True,low_memory=False)
            frame['YEAR'] = 2000 + int(year)
            frame['QTR'] = qtr
            Drug_df4 = Drug_df4.append(frame, ignore_index=True)
        
        


#Drop CASEID, CUM_DOSE_CHR, CUM_DOSE_UNIT, DOSE_AMT,DOSE_UNIT,DOSE_FORM, and DOSE_FREQ
Drug_df3 = Drug_df3.drop(['CASEID','CUM_DOSE_CHR','CUM_DOSE_UNIT','DOSE_AMT','DOSE_UNIT','DOSE_FORM','DOSE_FREQ'], 1)         
Drug_df4 = Drug_df4.drop(['CASEID','CUM_DOSE_CHR','CUM_DOSE_UNIT','DOSE_AMT','DOSE_UNIT','DOSE_FORM','DOSE_FREQ'], 1)         

#Rename PRIMARYID to ISR
Drug_df3 = Drug_df3.rename(columns={'PRIMARYID': 'ISR'})
Drug_df4 = Drug_df4.rename(columns={'PRIMARYID': 'ISR'})

#Append Drug_df3 and Drug_df4 to Drug_df
Drug_df = Drug_df.append(Drug_df3, ignore_index=True)
Drug_df = Drug_df.append(Drug_df4, ignore_index=True)

#Write Drugs_df to CSV
Drug_df.to_csv('C:\Users\jonbryan90\Desktop\DRUGS_MASTER2')