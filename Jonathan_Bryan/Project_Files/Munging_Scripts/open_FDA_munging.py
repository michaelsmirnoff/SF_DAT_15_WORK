# -*- coding: utf-8 -*-
"""
Created on Mon Feb 23 01:05:47 2015

@author: jonbryan90
"""
import pandas as pd
import numpy as np
import json
import requests

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