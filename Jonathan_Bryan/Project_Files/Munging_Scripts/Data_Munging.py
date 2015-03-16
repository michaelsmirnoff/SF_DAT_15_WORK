# -*- coding: utf-8 -*-
"""
Created on Tue Feb 03 17:40:25 2015

@author: jonbryan90
"""

import pandas as pd
import numpy as np
import requests
import json

'''
FAERS DRUG.csv data retrieval
'''
 
#Script to populate Drug_df dataframe from 2004Q1-2011Q4
years = range(4,12)
qtr = 1
Drug_df = pd.DataFrame()
for year in years:
    path ='C:\Users\jonbryan90\Documents\DRUG\\DRUG%dQ%d.txt' % (year,qtr)
    frame = pd.read_csv(path, names=['ISR','DRUG_SEQ','ROLE_COD','DRUGNAME','VAL_VBM','ROUTE','DOSE_VBM','DECHAL','RECHAL','LOT_NUM','EXP_DT','NDA_NUM','YEAR','QTR'], sep='$', skiprows=1, low_memory=False, skipinitialspace=True)
    frame['YEAR'] = 2000 + int(year)
    frame['QTR'] = qtr
    Drug_df = Drug_df.append(frame, ignore_index=True)
    if qtr == 4:
        qtr = 1
    else:
        qtr = qtr + 1

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

#Script to populate Drug_df3 dataframe from 2012Q4-2014Q2
years = range(12,15)
qtr = 4
Drug_df3 = pd.DataFrame()
for year in years:
    path ='C:\Users\jonbryan90\Documents\DRUG\\DRUG%dQ%d.txt' % (year,qtr)
    frame = pd.read_csv(path, names=['PRIMARYID','CASEID','DRUG_SEQ','ROLE_COD','DRUGNAME','VAL_VBM','ROUTE','DOSE_VBM','CUM_DOSE_CHR','CUM_DOSE_UNIT','DECHAL','RECHAL','LOT_NUM','EXP_DT','NDA_NUM','DOSE_AMT','DOSE_UNIT','DOSE_FORM','DOSE_FREQ','YEAR','QTR'], sep='$', skiprows=1, skipinitialspace=True,low_memory=False)
    frame['YEAR'] = 2000 + int(year)
    frame['QTR'] = qtr
    Drug_df3 = Drug_df3.append(frame, ignore_index=True)
    if qtr == 4:
        qtr = 1
    else:
        qtr = qtr + 1

#Drop CASEID, CUM_DOSE_CHR, CUM_DOSE_UNIT, DOSE_AMT,DOSE_UNIT,DOSE_FORM, and DOSE_FREQ
Drug_df3 = Drug_df3.drop(['CASEID','CUM_DOSE_CHR','CUM_DOSE_UNIT','DOSE_AMT','DOSE_UNIT','DOSE_FORM','DOSE_FREQ'], 1)         

#Rename PRIMARYID to ISR
Drug_df3 = Drug_df3.rename(columns={'PRIMARYID': 'ISR'})

#Append Drug_df3 to Drug_df
Drug_df = Drug_df.append(Drug_df3, ignore_index=True)

#Write Drugs_df to CSV
Drug_df.to_csv('C:\Users\jonbryan90\Desktop\DRUGS_MASTER')
  




'''
openFDA data munging
'''

data = pd.read_csv('C:\Users\jonbryan90\Test_Git\DAT4-students\Jonathan_Bryan\master_data\DS_Master_Data.csv')

#Remove empty columns from Excel
data = data.drop(data.columns[18:91], axis=1, inplace=True)

#Remove empty rows from Excel
data = data.drop(data.index[645:659])

#Add 'Trade Name' Firmagon to [Trade Name][557] and Nucynta to [Trade Name][571] 
data['Trade Name'][557] = 'Firmagon'
data['Trade Name'][571] = 'Nucynta'

#openFDA API Key
api_key = 'OWXe47B9huFsgkfaBT2XfP0S8oky9k15J5ewRTTn'

#iterator
a = 0
#populate the 'Num_Adv_Event' column
for e in data['Trade Name']:
    trade_name = e
    e = e.replace(' ','+')
    json_object = requests.get('https://api.fda.gov/drug/event.json?api_key='+api_key+'&search=patient.drug.medicinalproduct:"'+trade_name+'"+AND+patient.drug.drugcharacterization:1&count=safetyreport.exact')
    json_object_decode = json.loads(json_object.text)
    if json_object_decode.get('results') == None:
        data['Num_Adv_Event'][a] = 'NA'
        a = a + 1
    else:
        data['Num_Adv_Event'][a] = int(json_object_decode['results'][0]['count'])
        a = a + 1

#iterator
a = 0
#populate the 'Num_Serious' column
for e in data['Trade Name']:
    trade_name = e
    e = e.replace(' ','+')
    json_object = requests.get('https://api.fda.gov/drug/event.json?api_key='+api_key+'&search=patient.drug.medicinalproduct:"'+trade_name+'"+AND+patient.drug.drugcharacterization:1+AND+serious:1&count=safetyreport.exact')
    json_object_decode = json.loads(json_object.text)
    if json_object_decode.get('results') == None:
        data['Num_Serious'][a] = 'NA'
        a = a + 1
    else:
        data['Num_Serious'][a] = int(json_object_decode['results'][0]['count'])
        a = a + 1

#iterator
a = 0
#populate the 'Num_Other' column
for e in data['Trade Name']:
    trade_name = e
    e = e.replace(' ','+')
    json_object = requests.get('https://api.fda.gov/drug/event.json?api_key='+api_key+'&search=patient.drug.medicinalproduct:"'+trade_name+'"+AND+patient.drug.drugcharacterization:1+AND+seriousnessother:1&count=safetyreport.exact')
    json_object_decode = json.loads(json_object.text)
    if json_object_decode.get('results') == None:
        data['Num_Other'][a] = 'NA'
        a = a + 1
    else:
        data['Num_Other'][a] = int(json_object_decode['results'][0]['count'])
        a = a + 1

#iterator
a = 0
#populate the 'Num_Life_Threat' column
for e in data['Trade Name']:
    trade_name = e
    e = e.replace(' ','+')
    json_object = requests.get('https://api.fda.gov/drug/event.json?api_key='+api_key+'&search=patient.drug.medicinalproduct:"'+trade_name+'"+AND+patient.drug.drugcharacterization:1+AND+seriousnesslifethreatening:1&count=safetyreport.exact')
    json_object_decode = json.loads(json_object.text)
    if json_object_decode.get('results') == None:
        data['Num_Life_Threat'][a] = 'NA'
        a = a + 1
    else:
        data['Num_Life_Threat'][a] = int(json_object_decode['results'][0]['count'])
        a = a + 1
        
#iterator
a = 0
#populate the 'Num_Hosp' column
for e in data['Trade Name']:
    trade_name = e
    e = e.replace(' ','+')
    json_object = requests.get('https://api.fda.gov/drug/event.json?api_key='+api_key+'&search=patient.drug.medicinalproduct:"'+trade_name+'"+AND+patient.drug.drugcharacterization:1+AND+seriousnesshospitalization:1&count=safetyreport.exact')
    json_object_decode = json.loads(json_object.text)
    if json_object_decode.get('results') == None:
        data['Num_Hosp'][a] = 'NA'
        a = a + 1
    else:
        data['Num_Hosp'][a] = int(json_object_decode['results'][0]['count'])
        a = a + 1
        
#iterator
a = 0
#populate the 'Num_Congen_Anom' column
for e in data['Trade Name']:
    trade_name = e
    e = e.replace(' ','+')
    json_object = requests.get('https://api.fda.gov/drug/event.json?api_key='+api_key+'&search=patient.drug.medicinalproduct:"'+trade_name+'"+AND+patient.drug.drugcharacterization:1+AND+seriousnesscongenitalanomali:1&count=safetyreport.exact')
    json_object_decode = json.loads(json_object.text)
    if json_object_decode.get('results') == None:
        data['Num_Congen_Anom'][a] = 'NA'
        a = a + 1
    else:
        data['Num_Congen_Anom'][a] = int(json_object_decode['results'][0]['count'])
        a = a + 1

#iterator
a = 0
#populate the 'Num_Disable' column
for e in data['Trade Name']:
    trade_name = e
    e = e.replace(' ','+')
    json_object = requests.get('https://api.fda.gov/drug/event.json?api_key='+api_key+'&search=patient.drug.medicinalproduct:"'+trade_name+'"+AND+patient.drug.drugcharacterization:1+AND+seriousnessdisabling:1&count=safetyreport.exact')
    json_object_decode = json.loads(json_object.text)
    if json_object_decode.get('results') == None:
        data['Num_Disable'][a] = 'NA'
        a = a + 1
    else:
        data['Num_Disable'][a] = int(json_object_decode['results'][0]['count'])
        a = a + 1

#iterator
a = 0
#populate the 'Num_Deaths' column
for e in data['Trade Name']:
    trade_name = e
    e = e.replace(' ','+')
    json_object = requests.get('https://api.fda.gov/drug/event.json?api_key='+api_key+'&search=patient.drug.medicinalproduct:"'+trade_name+'"+AND+patient.drug.drugcharacterization:1+AND+seriousnessdeath:1&count=safetyreport.exact')
    json_object_decode = json.loads(json_object.text)
    if json_object_decode.get('results') == None:
        data['Num_Deaths'][a] = 'NA'
        a = a + 1
    else:
        data['Num_Deaths'][a] = int(json_object_decode['results'][0]['count'])
        a = a + 1
        
#iterator
a = 0
#populate the 'Num_Male' column
for e in data['Trade Name']:
    trade_name = e
    e = e.replace(' ','+')
    json_object = requests.get('https://api.fda.gov/drug/event.json?api_key='+api_key+'&search=patient.drug.medicinalproduct:"'+trade_name+'"+AND+patient.drug.drugcharacterization:1+AND+patient.patientsex:1&count=safetyreport.exact')
    json_object_decode = json.loads(json_object.text)
    if json_object_decode.get('results') == None:
        data['Num_Male'][a] = 'NA'
        a = a + 1
    else:
        data['Num_Male'][a] = int(json_object_decode['results'][0]['count'])
        a = a + 1
        
#iterator
a = 0
#populate the 'Num_Female' column
for e in data['Trade Name']:
    trade_name = e
    e = e.replace(' ','+')
    json_object = requests.get('https://api.fda.gov/drug/event.json?api_key='+api_key+'&search=patient.drug.medicinalproduct:"'+trade_name+'"+AND+patient.drug.drugcharacterization:1+AND+patient.patientsex:2&count=safetyreport.exact')
    json_object_decode = json.loads(json_object.text)
    if json_object_decode.get('results') == None:
        data['Num_Female'][a] = 'NA'
        a = a + 1
    else:
        data['Num_Female'][a] = int(json_object_decode['results'][0]['count'])
        a = a + 1
        
#iterator
a = 0
#populate the 'FDA_Drug_Class' column
for e in data['Trade Name']:
    trade_name = e
    e = e.replace(' ','+')
    json_object = requests.get('https://api.fda.gov/drug/event.json?api_key='+api_key+'&search=patient.drug.medicinalproduct:"'+trade_name+'"+AND+patient.drug.drugcharacterization:1+AND+_exists_:patient.drug.openfda.pharm_class_epc&limit=1')
    json_object_decode = json.loads(json_object.text)
    if json_object_decode.get('results') == None:
        data['FDA_Drug_Class'][a] = 'NA'
        a = a + 1
    else:
        data['FDA_Drug_Class'][a] = str(json_object_decode['results'][0]['patient']['drug'][1]['openfda']['pharm_class_epc'][0])
        a = a + 1