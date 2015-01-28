# -*- coding: utf-8 -*-
"""
Created on Wed Jan 28 09:58:29 2015

@author: Jason
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


headers = ['grant_doc_num', # assigned patent number
'invention_title', 
'grant_kind', # type of patent granted
'grant_date', # when patent was granted
'appl_type', # type of patent applied for
'appl_date', # date of patent application
'main_class', # main US government classification of patent
'num_refs', # number of references cited by the patent applicant and examiners
'assignee_org', # holder of patent
'assignee_city',    
'assignee_state',
'assignee_country',
'applicant_name', # name of inventor(s)
'num_applicants', # number of applicants
'abstract', # synopsis of patent claims
'claims'] # explanation of patent   

date_cols = ['grant_date', 'appl_date']

patents = pd.read_csv('/Users/Jason/Documents/DataScience/DAT4-students/jason/final_project/data/patents.csv', 
                      sep = ';', header=None, names=headers, parse_dates = date_cols)

patents.info()

patents.columns

patents.appl_type.value_counts()
patents.main_class.value_counts()
patents.assignee_city.value_counts()
patents.num_refs.describe()
patents.num_refs.hist(bins = 500)
patents.num_applicants.describe()
patents.num_applicants.hist(bins = 40)

patents.sort_index(by='num_refs').tail(10) 
patents.sort_index(by='num_applicants').tail(10) 

patents.assignee_country.value_counts()
patents.assignee_state.value_counts()

cities = set()
for city in patents.assignee_city:
    cities.update(town for town in city.split())
cities = sorted(cities)

states = set()
for state in patents.assignee_state:
    states.update(st for st in state.split())
states = sorted(states)

countries = set()
for country in patents.assignee_country:
    countries.update(c for c in country.split())
countries = sorted(countries)

companies = set()
for company in patents.assignee_org:
    companies.update(comp for comp in company.split(','))
companies = sorted(companies)

patents.columns

patents['time_elapsed'] = patents['grant_date'] - patents['appl_date']

