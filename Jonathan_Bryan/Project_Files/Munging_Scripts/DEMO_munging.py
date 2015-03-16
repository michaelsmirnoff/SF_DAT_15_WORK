# -*- coding: utf-8 -*-
"""
Created on Sun Feb 15 21:12:01 2015

@author: jonbryan90
"""

import pandas as pd
import numpy as np

'''
FAERS DEMO.csv data retrieval
'''
 
#Script to populate Demo_df dataframe from 2004Q1-2011Q4
years = range(4,12)
qtrs = range(1,5)
Demo_df = pd.DataFrame()
for year in years:
    for qtr in qtrs:
        path ='C:\Users\jonbryan90\Documents\DEMO\\DEMO%dQ%d.txt' % (year,qtr)
        frame = pd.read_csv(path, names=['ISR','CASE','I_F_COD','FOLL_SEQ','IMAGE','EVENT_DT','MFR_DT','FDA_DT','REPT_COD','MFR_NUM','MFR_SNDR','AGE','AGE_COD','GNDR_COD','E_SUB','WT','WT_COD','REPT_DT','OCCP_COD','DEATH_DT','TO_MFR','CONFID','REPORTER_COUNTRY','YEAR','QTR'], sep='$', skiprows=1, low_memory=False, skipinitialspace=True)
        frame['YEAR'] = 2000 + int(year)
        frame['QTR'] = qtr
        Demo_df = Demo_df.append(frame, ignore_index=True)
        
#Drop a bunch of uneeded columns and keep ISR, I_F_COD, AGE, AGE_COD, GNDR_COD, REPORTER_COUNTRY, YEAR, QTR
Demo_df = Demo_df.drop(['CASE','FOLL_SEQ','IMAGE','EVENT_DT','MFR_DT','FDA_DT','REPT_COD','MFR_NUM','MFR_SNDR','E_SUB','WT','WT_COD','REPT_DT','OCCP_COD','DEATH_DT','TO_MFR','CONFID'], 1)

#Script to populate Drug_df2 dataframe from 2012Q1-2012Q3
years = 12
qtrs = range(1,4)
Demo_df2 = pd.DataFrame()
for qtr in qtrs:
    path ='C:\Users\jonbryan90\Documents\DEMO\\DEMO%dQ%d.txt' % (years,qtr)
    frame = pd.read_csv(path, names=['ISR','CASE','I_F_COD','FOLL_SEQ','IMAGE','EVENT_DT','MFR_DT','FDA_DT','REPT_COD','MFR_NUM','MFR_SNDR','AGE','AGE_COD','GNDR_COD','E_SUB','WT','WT_COD','REPT_DT','OCCP_COD','DEATH_DT','TO_MFR','CONFID','REPORTER_COUNTRY','YEAR','QTR'], sep='$', skiprows=1, low_memory=False, skipinitialspace=True)
    frame['YEAR'] = 2012
    frame['QTR'] = qtr
    Demo_df2 = Demo_df2.append(frame, ignore_index=True)

#Drop a bunch of uneeded columns and keep ISR, I_F_COD, AGE, AGE_COD, GNDR_COD, REPORTER_COUNTRY, YEAR, QTR
Demo_df2 = Demo_df2.drop(['CASE','FOLL_SEQ','IMAGE','EVENT_DT','MFR_DT','FDA_DT','REPT_COD','MFR_NUM','MFR_SNDR','E_SUB','WT','WT_COD','REPT_DT','OCCP_COD','DEATH_DT','TO_MFR','CONFID',], 1)

#Append Demo_df2 to Demo_df
Demo_df = Demo_df.append(Demo_df2, ignore_index=True)

#Script to populate Drug_df3 dataframe from 2012Q4
years = 12
qtr = 4
Demo_df3 = pd.DataFrame()
path ='C:\Users\jonbryan90\Documents\DEMO\\DEMO%dQ%d.txt' % (year,qtr)
frame = pd.read_csv(path, names=['primaryid','caseid','caseversion','I_F_COD','event_dt','mfr_dt','init_fda_dt','fda_dt','rept_cod','mfr_num','mfr_sndr','AGE','AGE_COD','GNDR_COD','e_sub','wt','wt_cod','rept_dt','to_mfr','occp_cod','REPORTER_COUNTRY','occr_country','YEAR','QTR'], sep='$', skiprows=1, skipinitialspace=True,low_memory=False)
frame['YEAR'] = 2000 + int(year)
frame['QTR'] = qtr
Demo_df3 = Demo_df3.append(frame, ignore_index=True)

#Script to populate Drug_df4 dataframe from 2013Q1-2014Q2
years = range(13,15)
qtrs = range(1,5)
Demo_df4 = pd.DataFrame()
for year in years:
    for qtr in qtrs:
        if year == 14 and qtr == 3:
            break
        else:
            path ='C:\Users\jonbryan90\Documents\DEMO\\DEMO%dQ%d.txt' % (year,qtr)
            frame = pd.read_csv(path, names=['primaryid','caseid','caseversion','I_F_COD','event_dt','mfr_dt','init_fda_dt','fda_dt','rept_cod','mfr_num','mfr_sndr','AGE','AGE_COD','GNDR_COD','e_sub','wt','wt_cod','rept_dt','to_mfr','occp_cod','REPORTER_COUNTRY','occr_country','YEAR','QTR'], sep='$', skiprows=1, skipinitialspace=True,low_memory=False)
            frame['YEAR'] = 2000 + int(year)
            frame['QTR'] = qtr
            Demo_df4 = Demo_df4.append(frame, ignore_index=True)

##Drop a bunch of uneeded columns and keep primaryid, I_F_COD, AGE, AGE_COD, GNDR_COD, REPORTER_COUNTRY, YEAR, QTR
Demo_df3 = Demo_df3.drop(['caseid','caseversion','event_dt','mfr_dt','init_fda_dt','fda_dt','rept_cod','mfr_num','mfr_sndr','e_sub','wt','wt_cod','rept_dt','to_mfr','occp_cod','occr_country'], 1)         
Demo_df4 = Demo_df4.drop(['caseid','caseversion','event_dt','mfr_dt','init_fda_dt','fda_dt','rept_cod','mfr_num','mfr_sndr','e_sub','wt','wt_cod','rept_dt','to_mfr','occp_cod','occr_country'], 1)         

#Rename primaryid to ISR
Demo_df3 = Demo_df3.rename(columns={'primaryid': 'ISR'})
Demo_df4 = Demo_df4.rename(columns={'primaryid': 'ISR'})
#Append Demo_df3 to Demo_df
Demo_df = Demo_df.append(Demo_df3, ignore_index=True)
Demo_df = Demo_df.append(Demo_df4, ignore_index=True)

#Write Demo_df to CSV
Demo_df.to_csv('C:\Users\jonbryan90\Desktop\DEMO_MASTER2')