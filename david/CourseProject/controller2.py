import json
import psycopg2
import psycopg2.extras
from DAT4_library import queries
from DAT4_library import connect_DB
from DAT4_library import parse_inputs
import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
import pylab as pl
from sklearn import tree
from sklearn.ensemble import RandomForestClassifier as RF
import matplotlib.pyplot as plt
from sklearn.cross_validation import train_test_split
from pylab import *
from sklearn.cross_validation import cross_val_score
#from years_of_milwaukee import call_2009
#from years_of_milwaukee import call_2010
#from years_of_milwaukee import call_2011
#from years_of_milwaukee import call_2012
#from years_of_milwaukee import call_2013
#from years_of_milwaukee import call_tracts_2013 as tracts_2013
#from years_of_milwaukee import call_tracts_2012 as tracts_2012
#from years_of_milwaukee import call_tracts_2011 as tracts_2011
#from years_of_milwaukee import call_tracts_2010 as tracts_2010
#from years_of_milwaukee import call_tracts_2009 as tracts_2009
#instantiate classes
#geo = geo_aggregator() #disabled geo_aggregator as it has been used and is not needed
query = queries()
connect = connect_DB()
parse = parse_inputs()

HMDA_cols = ['statecode', 'countycode', 'censustractnumber', 'applicantrace1', 'applicantrace2', 'applicantrace3', 'applicantrace4', 'applicantrace5',
                            'coapplicantrace1', 'coapplicantrace2', 'coapplicantrace3', 'coapplicantrace4', 'coapplicantrace5', 'applicantethnicity', 'coapplicantethnicity',
                            'applicantincome', 'ratespread', 'lienstatus', 'hoepastatus', 'purchasertype', 'loanamount', 'year', 'median_family_income',
                            'minority_population_pct', 'tract_to_msa_md_income', 'actiontype', 'gender']

'''data have been filtered as follows in SQL queries
    loan type: conventional only, code 1
    property type: 1-4 family only, code 1
    loan purpose: purchase only, code 1
    occupancy status: owner occupied only, code 1
    lien status: first liens only, code 1
    income != 0 #removes most non-natural person loans
    action type: originations includes only originated loans, applications includes codes 1-4
    these filters were used to standardize the underwriting criteria for the logistic model
    standardizing type also allows comparison on pricing as collateral type, loan type, loan purpose, and occupancy status all affect pricing
'''

cur = connect.connect()
SQL = query.all_years_union()
cur.execute(SQL)
all_dbs = pd.DataFrame(cur.fetchall(), columns = HMDA_cols) #how do i reference HMDA cols from an object?
#change year variables to HMDA variables
all_dbs['minority_status'] = 0 #initialize series in dataframe
all_dbs['tract_cat'] = 0
tract_cat = [] #create a list to store tract minority percent categories
minority_status = [] #create a list to store minority flags
for row in all_dbs.iterrows():
	parse.parse(row) #parse database rows to determine minority status
	minority_status.append(parse.inputs['minority status']) #append minority flag
	tract_cat.append(parse.inputs['minority_tract_category']) #fill the list with flags
all_dbs['minority_status'] = minority_status #input minority flags into the dataframe
all_dbs['tract_cat'] = tract_cat

#2009 data
data_2009 = all_dbs[all_dbs.year == '2009']
data_2010 = all_dbs[all_dbs.year == '2010']
data_2011 = all_dbs[all_dbs.year == '2011']
data_2012 = all_dbs[all_dbs.year == '2012']
data_2013 = all_dbs[all_dbs.year == '2013']
#print data_2009.shape

income_means = [] #baseline income information
income_means.append(round(data_2009[data_2009.minority_status == 0].applicantincome.mean(),2))
income_means.append(round(data_2010[data_2010.minority_status == 0].applicantincome.mean(),2))
income_means.append(round(data_2011[data_2011.minority_status == 0].applicantincome.mean(),2))
income_means.append(round(data_2012[data_2012.minority_status == 0].applicantincome.mean(),2))
income_means.append(round(data_2013[data_2013.minority_status == 0].applicantincome.mean(),2))
print income_means

min_income_means = [] #baseline income information
min_income_means.append(round(data_2009[data_2009.minority_status == 1].applicantincome.mean(),2))
min_income_means.append(round(data_2010[data_2010.minority_status == 1].applicantincome.mean(),2))
min_income_means.append(round(data_2011[data_2011.minority_status == 1].applicantincome.mean(),2))
min_income_means.append(round(data_2012[data_2012.minority_status == 1].applicantincome.mean(),2))
min_income_means.append(round(data_2013[data_2013.minority_status == 1].applicantincome.mean(),2))
print min_income_means

min_income_low = [] #low minority tract incomes
min_income_low.append(round(data_2009[(data_2009.tract_cat == 'low') &(data_2009.minority_status == 1)].applicantincome.mean(),2))
min_income_low.append(round(data_2010[(data_2010.tract_cat == 'low') &(data_2010.minority_status == 1)].applicantincome.mean(),2))
min_income_low.append(round(data_2011[(data_2011.tract_cat == 'low') &(data_2011.minority_status == 1)].applicantincome.mean(),2))
min_income_low.append(round(data_2012[(data_2012.tract_cat == 'low') &(data_2012.minority_status == 1)].applicantincome.mean(),2))
min_income_low.append(round(data_2013[(data_2013.tract_cat == 'low') &(data_2013.minority_status == 1)].applicantincome.mean(),2))
print min_income_low

non_min_income_low = [] #low minority tract incomes
non_min_income_low.append(round(data_2009[(data_2009.tract_cat == 'low') &(data_2009.minority_status == 0)].applicantincome.mean(),2))
non_min_income_low.append(round(data_2010[(data_2010.tract_cat == 'low') &(data_2010.minority_status == 0)].applicantincome.mean(),2))
non_min_income_low.append(round(data_2011[(data_2011.tract_cat == 'low') &(data_2011.minority_status == 0)].applicantincome.mean(),2))
non_min_income_low.append(round(data_2012[(data_2012.tract_cat == 'low') &(data_2012.minority_status == 0)].applicantincome.mean(),2))
non_min_income_low.append(round(data_2013[(data_2013.tract_cat == 'low') &(data_2013.minority_status == 0)].applicantincome.mean(),2))
print non_min_income_low

min_income_mid = [] #mid minority tract incomes
min_income_mid.append(round(data_2009[(data_2009.tract_cat == 'middle') & (data_2009.minority_status == 1)].applicantincome.mean(),2))
min_income_mid.append(round(data_2010[(data_2010.tract_cat == 'middle') & (data_2010.minority_status == 1)].applicantincome.mean(),2))
min_income_mid.append(round(data_2011[(data_2011.tract_cat == 'middle') & (data_2011.minority_status == 1)].applicantincome.mean(),2))
min_income_mid.append(round(data_2012[(data_2012.tract_cat == 'middle') & (data_2012.minority_status == 1)].applicantincome.mean(),2))
min_income_mid.append(round(data_2013[(data_2013.tract_cat == 'middle') & (data_2013.minority_status == 1)].applicantincome.mean(),2))
print min_income_mid

non_min_income_mid = [] #mid minority tract incomes
non_min_income_mid.append(round(data_2009[(data_2009.tract_cat == 'middle') & (data_2009.minority_status == 0)].applicantincome.mean(),2))
non_min_income_mid.append(round(data_2010[(data_2010.tract_cat == 'middle') & (data_2010.minority_status == 0)].applicantincome.mean(),2))
non_min_income_mid.append(round(data_2011[(data_2011.tract_cat == 'middle') & (data_2011.minority_status == 0)].applicantincome.mean(),2))
non_min_income_mid.append(round(data_2012[(data_2012.tract_cat == 'middle') & (data_2012.minority_status == 0)].applicantincome.mean(),2))
non_min_income_mid.append(round(data_2013[(data_2013.tract_cat == 'middle') & (data_2013.minority_status == 0)].applicantincome.mean(),2))
print non_min_income_mid

min_income_upp = [] #upper minority tract incomes
min_income_upp.append(round(data_2009[(data_2009.tract_cat == 'upper') & (data_2009.minority_status == 1)].applicantincome.mean(),2))
min_income_upp.append(round(data_2010[(data_2010.tract_cat == 'upper') & (data_2010.minority_status == 1)].applicantincome.mean(),2))
min_income_upp.append(round(data_2011[(data_2011.tract_cat == 'upper') & (data_2011.minority_status == 1)].applicantincome.mean(),2))
min_income_upp.append(round(data_2012[(data_2012.tract_cat == 'upper') & (data_2012.minority_status == 1)].applicantincome.mean(),2))
min_income_upp.append(round(data_2013[(data_2013.tract_cat == 'upper') & (data_2013.minority_status == 1)].applicantincome.mean(),2))
print min_income_upp

non_min_income_upp = [] #upper minority tract incomes
non_min_income_upp.append(round(data_2009[(data_2009.tract_cat == 'upper') & (data_2009.minority_status == 0)].applicantincome.mean(),2))
non_min_income_upp.append(round(data_2010[(data_2010.tract_cat == 'upper') & (data_2010.minority_status == 0)].applicantincome.mean(),2))
non_min_income_upp.append(round(data_2011[(data_2011.tract_cat == 'upper') & (data_2011.minority_status == 0)].applicantincome.mean(),2))
non_min_income_upp.append(round(data_2012[(data_2012.tract_cat == 'upper') & (data_2012.minority_status == 0)].applicantincome.mean(),2))
non_min_income_upp.append(round(data_2013[(data_2013.tract_cat == 'upper') & (data_2013.minority_status == 0)].applicantincome.mean(),2))
print non_min_income_upp

min_income_high = [] #high minority tract incomes
min_income_high.append(round(data_2009[(data_2009.tract_cat == 'high') & (data_2009.minority_status == 1)].applicantincome.mean(),2))
min_income_high.append(round(data_2010[(data_2010.tract_cat == 'high') & (data_2010.minority_status == 1)].applicantincome.mean(),2))
min_income_high.append(round(data_2011[(data_2011.tract_cat == 'high') & (data_2011.minority_status == 1)].applicantincome.mean(),2))
min_income_high.append(round(data_2012[(data_2012.tract_cat == 'high') & (data_2012.minority_status == 1)].applicantincome.mean(),2))
min_income_high.append(round(data_2013[(data_2013.tract_cat == 'high') & (data_2013.minority_status == 1)].applicantincome.mean(),2))
print min_income_high

non_min_income_high = [] #high minority tract incomes
non_min_income_high.append(round(data_2009[(data_2009.tract_cat == 'high') & (data_2009.minority_status == 0)].applicantincome.mean(),2))
non_min_income_high.append(round(data_2010[(data_2010.tract_cat == 'high') & (data_2010.minority_status == 0)].applicantincome.mean(),2))
non_min_income_high.append(round(data_2011[(data_2011.tract_cat == 'high') & (data_2011.minority_status == 0)].applicantincome.mean(),2))
non_min_income_high.append(round(data_2012[(data_2012.tract_cat == 'high') & (data_2012.minority_status == 0)].applicantincome.mean(),2))
non_min_income_high.append(round(data_2013[(data_2013.tract_cat == 'high') & (data_2013.minority_status == 0)].applicantincome.mean(),2))
print non_min_income_high

#initialize lists of minority and non-minority approval rates for graphing
#baseline graph
#plot minority incomes
years = [2009, 2010, 2011, 2012, 2013]
years2 = ['2009', ' ', '2010', ' ', '2011', ' ', '2012', ' ', '2013']
axes = figure().add_subplot(111)
a = axes.get_xticks().tolist()
a = years2
axes.set_xticklabels(years2)
plt.plot(years, min_income_low, marker = 'o', color = 'r', label = 'low minority')
plt.plot(years, min_income_mid, label='mid minority')
plt.plot(years, min_income_upp, label='upper minority')
plt.plot(years, min_income_high, label='high minority')
plt.ylabel('Income in 000s')
plt.ylim((0,130))
plt.title('Minority Applicant Income by Year')
plt.legend(bbox_to_anchor=[1,0], loc='center')
plt.legend()
plt.show()

#plot non-minority incomes
years = [2009, 2010, 2011, 2012, 2013]
years2 = ['2009', ' ', '2010', ' ', '2011', ' ', '2012', ' ', '2013']
axes = figure().add_subplot(111)
a = axes.get_xticks().tolist()
a = years2
axes.set_xticklabels(years2)
plt.plot(years, non_min_income_low, marker = 'o', color = 'r', label = 'low minority')
plt.plot(years, non_min_income_mid, label='mid minority')
plt.plot(years, non_min_income_upp, label='upper minority')
plt.plot(years, non_min_income_high, label='high minority')
plt.ylabel('Income in 000s')
plt.ylim((0,130))
plt.title('Non-Minority Applicant Income by Year')
plt.legend(bbox_to_anchor=[1,0], loc='center')
plt.legend()
plt.show()


min_loanval_low = [] #low minority tract incomes
min_loanval_low.append(round(data_2009[(data_2009.tract_cat == 'low') &(data_2009.minority_status == 1)].loanamount.mean(),2))
min_loanval_low.append(round(data_2010[(data_2010.tract_cat == 'low') &(data_2010.minority_status == 1)].loanamount.mean(),2))
min_loanval_low.append(round(data_2011[(data_2011.tract_cat == 'low') &(data_2011.minority_status == 1)].loanamount.mean(),2))
min_loanval_low.append(round(data_2012[(data_2012.tract_cat == 'low') &(data_2012.minority_status == 1)].loanamount.mean(),2))
min_loanval_low.append(round(data_2013[(data_2013.tract_cat == 'low') &(data_2013.minority_status == 1)].loanamount.mean(),2))
print min_loanval_low

non_min_loanval_low = [] #low minority tract incomes
non_min_loanval_low.append(round(data_2009[(data_2009.tract_cat == 'low') &(data_2009.minority_status == 0)].loanamount.mean(),2))
non_min_loanval_low.append(round(data_2010[(data_2010.tract_cat == 'low') &(data_2010.minority_status == 0)].loanamount.mean(),2))
non_min_loanval_low.append(round(data_2011[(data_2011.tract_cat == 'low') &(data_2011.minority_status == 0)].loanamount.mean(),2))
non_min_loanval_low.append(round(data_2012[(data_2012.tract_cat == 'low') &(data_2012.minority_status == 0)].loanamount.mean(),2))
non_min_loanval_low.append(round(data_2013[(data_2013.tract_cat == 'low') &(data_2013.minority_status == 0)].loanamount.mean(),2))
print non_min_loanval_low

min_loanval_mid = [] #mid minority tract incomes
min_loanval_mid.append(round(data_2009[(data_2009.tract_cat == 'middle') & (data_2009.minority_status == 1)].loanamount.mean(),2))
min_loanval_mid.append(round(data_2010[(data_2010.tract_cat == 'middle') & (data_2010.minority_status == 1)].loanamount.mean(),2))
min_loanval_mid.append(round(data_2011[(data_2011.tract_cat == 'middle') & (data_2011.minority_status == 1)].loanamount.mean(),2))
min_loanval_mid.append(round(data_2012[(data_2012.tract_cat == 'middle') & (data_2012.minority_status == 1)].loanamount.mean(),2))
min_loanval_mid.append(round(data_2013[(data_2013.tract_cat == 'middle') & (data_2013.minority_status == 1)].loanamount.mean(),2))
print min_loanval_mid

non_min_loanval_mid = [] #mid minority tract incomes
non_min_loanval_mid.append(round(data_2009[(data_2009.tract_cat == 'middle') & (data_2009.minority_status == 0)].loanamount.mean(),2))
non_min_loanval_mid.append(round(data_2010[(data_2010.tract_cat == 'middle') & (data_2010.minority_status == 0)].loanamount.mean(),2))
non_min_loanval_mid.append(round(data_2011[(data_2011.tract_cat == 'middle') & (data_2011.minority_status == 0)].loanamount.mean(),2))
non_min_loanval_mid.append(round(data_2012[(data_2012.tract_cat == 'middle') & (data_2012.minority_status == 0)].loanamount.mean(),2))
non_min_loanval_mid.append(round(data_2013[(data_2013.tract_cat == 'middle') & (data_2013.minority_status == 0)].loanamount.mean(),2))
print non_min_loanval_mid

min_loanval_upp = [] #upper minority tract incomes
min_loanval_upp.append(round(data_2009[(data_2009.tract_cat == 'upper') & (data_2009.minority_status == 1)].loanamount.mean(),2))
min_loanval_upp.append(round(data_2010[(data_2010.tract_cat == 'upper') & (data_2010.minority_status == 1)].loanamount.mean(),2))
min_loanval_upp.append(round(data_2011[(data_2011.tract_cat == 'upper') & (data_2011.minority_status == 1)].loanamount.mean(),2))
min_loanval_upp.append(round(data_2012[(data_2012.tract_cat == 'upper') & (data_2012.minority_status == 1)].loanamount.mean(),2))
min_loanval_upp.append(round(data_2013[(data_2013.tract_cat == 'upper') & (data_2013.minority_status == 1)].loanamount.mean(),2))
print min_loanval_upp

non_min_loanval_upp = [] #upper minority tract incomes
non_min_loanval_upp.append(round(data_2009[(data_2009.tract_cat == 'upper') & (data_2009.minority_status == 0)].loanamount.mean(),2))
non_min_loanval_upp.append(round(data_2010[(data_2010.tract_cat == 'upper') & (data_2010.minority_status == 0)].loanamount.mean(),2))
non_min_loanval_upp.append(round(data_2011[(data_2011.tract_cat == 'upper') & (data_2011.minority_status == 0)].loanamount.mean(),2))
non_min_loanval_upp.append(round(data_2012[(data_2012.tract_cat == 'upper') & (data_2012.minority_status == 0)].loanamount.mean(),2))
non_min_loanval_upp.append(round(data_2013[(data_2013.tract_cat == 'upper') & (data_2013.minority_status == 0)].loanamount.mean(),2))
print non_min_loanval_upp

min_loanval_high = [] #high minority tract incomes
min_loanval_high.append(round(data_2009[(data_2009.tract_cat == 'high') & (data_2009.minority_status == 1)].loanamount.mean(),2))
min_loanval_high.append(round(data_2010[(data_2010.tract_cat == 'high') & (data_2010.minority_status == 1)].loanamount.mean(),2))
min_loanval_high.append(round(data_2011[(data_2011.tract_cat == 'high') & (data_2011.minority_status == 1)].loanamount.mean(),2))
min_loanval_high.append(round(data_2012[(data_2012.tract_cat == 'high') & (data_2012.minority_status == 1)].loanamount.mean(),2))
min_loanval_high.append(round(data_2013[(data_2013.tract_cat == 'high') & (data_2013.minority_status == 1)].loanamount.mean(),2))
print min_loanval_high

non_min_loanval_high = [] #high minority tract incomes
non_min_loanval_high.append(round(data_2009[(data_2009.tract_cat == 'high') & (data_2009.minority_status == 0)].loanamount.mean(),2))
non_min_loanval_high.append(round(data_2010[(data_2010.tract_cat == 'high') & (data_2010.minority_status == 0)].loanamount.mean(),2))
non_min_loanval_high.append(round(data_2011[(data_2011.tract_cat == 'high') & (data_2011.minority_status == 0)].loanamount.mean(),2))
non_min_loanval_high.append(round(data_2012[(data_2012.tract_cat == 'high') & (data_2012.minority_status == 0)].loanamount.mean(),2))
non_min_loanval_high.append(round(data_2013[(data_2013.tract_cat == 'high') & (data_2013.minority_status == 0)].loanamount.mean(),2))
print non_min_loanval_high

years = [2009, 2010, 2011, 2012, 2013]
years2 = ['2009', ' ', '2010', ' ', '2011', ' ', '2012', ' ', '2013']
axes = figure().add_subplot(111)
a = axes.get_xticks().tolist()
a = years2
axes.set_xticklabels(years2)
plt.plot(years, min_loanval_low, marker = 'o', color = 'r', label = 'low minority')
plt.plot(years, min_loanval_mid, label='mid minority')
plt.plot(years, min_loanval_upp, label='upper minority')
plt.plot(years, min_loanval_high, label='high minority')
plt.ylabel('Income in 000s')
plt.ylim((0,250))
plt.title('Minority Loan Values by Year')
plt.legend(bbox_to_anchor=[1,0], loc='center')
plt.legend()
plt.show()

#plot non-minority incomes
years = [2009, 2010, 2011, 2012, 2013]
years2 = ['2009', ' ', '2010', ' ', '2011', ' ', '2012', ' ', '2013']
axes = figure().add_subplot(111)
a = axes.get_xticks().tolist()
a = years2
axes.set_xticklabels(years2)
plt.plot(years, non_min_loanval_low, marker = 'o', color = 'r', label = 'low minority')
plt.plot(years, non_min_loanval_mid, label='mid minority')
plt.plot(years, non_min_loanval_upp, label='upper minority')
plt.plot(years, non_min_loanval_high, label='high minority')
plt.ylabel('Income in 000s')
plt.ylim((0,250))
plt.title('Non-Minority Loan Values by Year')
plt.legend(bbox_to_anchor=[1,0], loc='center')
plt.legend()
plt.show()


#baseline information for the MSA
app_counts = [] #total counts of applications
app_counts.append(data_2009.shape[0])
app_counts.append(data_2010.shape[0])
app_counts.append(data_2011.shape[0])
app_counts.append(data_2012.shape[0])
app_counts.append(data_2013.shape[0])
print "app counts\n", "*"*40, "\n", app_counts, "\n"

min_app_counts = [] #minority application count per year
min_app_counts.append(data_2009[data_2009.minority_status == 1].shape[0])
min_app_counts.append(data_2010[data_2010.minority_status == 1].shape[0])
min_app_counts.append(data_2011[data_2011.minority_status == 1].shape[0])
min_app_counts.append(data_2012[data_2012.minority_status == 1].shape[0])
min_app_counts.append(data_2013[data_2013.minority_status == 1].shape[0])

orig_counts = [] #holds origination counts for minorities
orig_counts.append(data_2009[data_2009.actiontype == '1'].shape[0])
orig_counts.append(data_2010[data_2010.actiontype == '1'].shape[0])
orig_counts.append(data_2011[data_2011.actiontype == '1'].shape[0])
orig_counts.append(data_2012[data_2012.actiontype == '1'].shape[0])
orig_counts.append(data_2013[data_2013.actiontype == '1'].shape[0])

min_orig_counts = [] #holds minority origination counts
min_orig_counts.append(data_2009[data_2009.minority_status == 1].shape[0])
min_orig_counts.append(data_2010[data_2010.minority_status == 1].shape[0])
min_orig_counts.append(data_2011[data_2011.minority_status == 1].shape[0])
min_orig_counts.append(data_2012[data_2012.minority_status == 1].shape[0])
min_orig_counts.append(data_2013[data_2013.minority_status == 1].shape[0])
print "minority origination counts \n", "*"*40
print "low:", min_orig_low
print "mid:", min_orig_mid
print "upp:", min_orig_upp
print "high:", min_orig_high
print "\n"

non_min_app_counts = [app_counts[i]-min_app_counts[i] for i in range(0,len(app_counts))] #non minority application count per year
non_min_orig_counts = [orig_counts[i]-min_orig_counts[i] for i in range(0, len(orig_counts))] #non-minority origination counts
approval_rates = [round(orig_counts[i]/float(app_counts[i]),2) for i in range(0, len(app_counts))] #approval rates baseline
min_pct_apps = [round(min_app_counts[i]/float(app_counts[i]),2) for i in range(0, len(app_counts))] #percent of applications by minorities
min_pct_orig = [round(min_orig_counts[i]/float(orig_counts[i]),2) for i in range(0, len(orig_counts))] #percent of originations to minorities
min_approval_rates = [round(min_orig_counts[i]/float(min_app_counts[i]),2) for i in range(0, len(orig_counts))] #minority borrower approval rate
non_min_approval_rates = [round(non_min_orig_counts[i]/float(non_min_app_counts[i]),2) for i in range(0, len(non_min_orig_counts))]

#information by tract categories, low, middle, upper, high
low_app_counts = [] #low minority tract application counts <= 30% minority
low_app_counts.append(data_2009[data_2009.tract_cat == 'low'].shape[0])
low_app_counts.append(data_2010[data_2010.tract_cat == 'low'].shape[0])
low_app_counts.append(data_2011[data_2011.tract_cat == 'low'].shape[0])
low_app_counts.append(data_2012[data_2012.tract_cat == 'low'].shape[0])
low_app_counts.append(data_2013[data_2013.tract_cat == 'low'].shape[0])
#print low_app_counts

mid_app_counts = []
mid_app_counts.append(data_2009[data_2009.tract_cat == 'middle'].shape[0])
mid_app_counts.append(data_2010[data_2010.tract_cat == 'middle'].shape[0])
mid_app_counts.append(data_2011[data_2011.tract_cat == 'middle'].shape[0])
mid_app_counts.append(data_2012[data_2012.tract_cat == 'middle'].shape[0])
mid_app_counts.append(data_2013[data_2013.tract_cat == 'middle'].shape[0])
#print mid_app_counts

upp_app_counts = []
upp_app_counts.append(data_2009[data_2009.tract_cat == 'upper'].shape[0])
upp_app_counts.append(data_2010[data_2010.tract_cat == 'upper'].shape[0])
upp_app_counts.append(data_2011[data_2011.tract_cat == 'upper'].shape[0])
upp_app_counts.append(data_2012[data_2012.tract_cat == 'upper'].shape[0])
upp_app_counts.append(data_2013[data_2013.tract_cat == 'upper'].shape[0])
#print upp_app_counts

high_app_counts = []
high_app_counts.append(data_2009[data_2009.tract_cat == 'high'].shape[0])
high_app_counts.append(data_2010[data_2010.tract_cat == 'high'].shape[0])
high_app_counts.append(data_2011[data_2011.tract_cat == 'high'].shape[0])
high_app_counts.append(data_2012[data_2012.tract_cat == 'high'].shape[0])
high_app_counts.append(data_2013[data_2013.tract_cat == 'high'].shape[0])
#print high_app_counts

#origination counts for minority tract categories
low_orig_counts = [] #origination counts for low minority tracts
low_orig_counts.append(data_2009[(data_2009.tract_cat == 'low') & (data_2009.actiontype == '1')].shape[0])
low_orig_counts.append(data_2010[(data_2010.tract_cat == 'low') & (data_2010.actiontype == '1')].shape[0])
low_orig_counts.append(data_2011[(data_2011.tract_cat == 'low') & (data_2011.actiontype == '1')].shape[0])
low_orig_counts.append(data_2012[(data_2012.tract_cat == 'low') & (data_2012.actiontype == '1')].shape[0])
low_orig_counts.append(data_2013[(data_2013.tract_cat == 'low') & (data_2013.actiontype == '1')].shape[0])

mid_orig_counts = [] #origination counts for middle minority tracts
mid_orig_counts.append(data_2009[(data_2009.tract_cat == 'middle') & (data_2009.actiontype == '1')].shape[0])
mid_orig_counts.append(data_2010[(data_2010.tract_cat == 'middle') & (data_2010.actiontype == '1')].shape[0])
mid_orig_counts.append(data_2011[(data_2011.tract_cat == 'middle') & (data_2011.actiontype == '1')].shape[0])
mid_orig_counts.append(data_2012[(data_2012.tract_cat == 'middle') & (data_2012.actiontype == '1')].shape[0])
mid_orig_counts.append(data_2013[(data_2013.tract_cat == 'middle') & (data_2013.actiontype == '1')].shape[0])

upp_orig_counts = [] #origination counts for upper minority tracts
upp_orig_counts.append(data_2009[(data_2009.tract_cat == 'upper') & (data_2009.actiontype == '1')].shape[0])
upp_orig_counts.append(data_2010[(data_2010.tract_cat == 'upper') & (data_2010.actiontype == '1')].shape[0])
upp_orig_counts.append(data_2011[(data_2011.tract_cat == 'upper') & (data_2011.actiontype == '1')].shape[0])
upp_orig_counts.append(data_2012[(data_2012.tract_cat == 'upper') & (data_2012.actiontype == '1')].shape[0])
upp_orig_counts.append(data_2013[(data_2013.tract_cat == 'upper') & (data_2013.actiontype == '1')].shape[0])

high_orig_counts = [] #origination counts for high minority tracts
high_orig_counts.append(data_2009[(data_2009.tract_cat == 'high') & (data_2009.actiontype == '1')].shape[0])
high_orig_counts.append(data_2010[(data_2010.tract_cat == 'high') & (data_2010.actiontype == '1')].shape[0])
high_orig_counts.append(data_2011[(data_2011.tract_cat == 'high') & (data_2011.actiontype == '1')].shape[0])
high_orig_counts.append(data_2012[(data_2012.tract_cat == 'high') & (data_2012.actiontype == '1')].shape[0])
high_orig_counts.append(data_2013[(data_2013.tract_cat == 'high') & (data_2013.actiontype == '1')].shape[0])

#approval rates by minority population tract category
low_approval_rates = [round(low_orig_counts[i]/float(low_app_counts[i]),2) for i in range(0, len(low_orig_counts))] #approval rates for low minority tracts
mid_approval_rates = [round(mid_orig_counts[i]/float(mid_app_counts[i]),2) for i in range(0, len(mid_orig_counts))] #approval rates for mid minority tracts
upp_approval_rates = [round(upp_orig_counts[i]/float(upp_app_counts[i]),2) for i in range(0, len(upp_orig_counts))] #approval rates for upper minority tracts
high_approval_rates = [round(high_orig_counts[i]/float(high_app_counts[i]),2) for i in range(0, len(high_orig_counts))] #approval rates for high minority tracts

#minority application counts by tract cateogry
min_app_low = [] #minority application count for low minority tract
min_app_low.append(data_2009[(data_2009.tract_cat == 'low') & (data_2009.minority_status == 1)].shape[0])
min_app_low.append(data_2010[(data_2010.tract_cat == 'low') & (data_2010.minority_status == 1)].shape[0])
min_app_low.append(data_2011[(data_2011.tract_cat == 'low') & (data_2011.minority_status == 1)].shape[0])
min_app_low.append(data_2012[(data_2012.tract_cat == 'low') & (data_2012.minority_status == 1)].shape[0])
min_app_low.append(data_2013[(data_2013.tract_cat == 'low') & (data_2013.minority_status == 1)].shape[0])
print min_app_low

min_app_mid = [] #minority application count ofr middle minority tract
min_app_mid.append(data_2009[(data_2009.tract_cat == 'middle') & (data_2009.minority_status == 1)].shape[0])
min_app_mid.append(data_2010[(data_2010.tract_cat == 'middle') & (data_2010.minority_status == 1)].shape[0])
min_app_mid.append(data_2011[(data_2011.tract_cat == 'middle') & (data_2011.minority_status == 1)].shape[0])
min_app_mid.append(data_2012[(data_2012.tract_cat == 'middle') & (data_2012.minority_status == 1)].shape[0])
min_app_mid.append(data_2013[(data_2013.tract_cat == 'middle') & (data_2013.minority_status == 1)].shape[0])
print min_app_mid

min_app_upp = [] #minority application count for upper minority tract
min_app_upp.append(data_2009[(data_2009.tract_cat == 'upper') & (data_2009.minority_status == 1)].shape[0])
min_app_upp.append(data_2010[(data_2010.tract_cat == 'upper') & (data_2010.minority_status == 1)].shape[0])
min_app_upp.append(data_2011[(data_2011.tract_cat == 'upper') & (data_2011.minority_status == 1)].shape[0])
min_app_upp.append(data_2012[(data_2012.tract_cat == 'upper') & (data_2012.minority_status == 1)].shape[0])
min_app_upp.append(data_2013[(data_2013.tract_cat == 'upper') & (data_2013.minority_status == 1)].shape[0])
print min_app_upp

min_app_high = [] #minority application count for high minority tract
min_app_high.append(data_2009[(data_2009.tract_cat == 'high') & (data_2009.minority_status == 1)].shape[0])
min_app_high.append(data_2010[(data_2010.tract_cat == 'high') & (data_2010.minority_status == 1)].shape[0])
min_app_high.append(data_2011[(data_2011.tract_cat == 'high') & (data_2011.minority_status == 1)].shape[0])
min_app_high.append(data_2012[(data_2012.tract_cat == 'high') & (data_2012.minority_status == 1)].shape[0])
min_app_high.append(data_2013[(data_2013.tract_cat == 'high') & (data_2013.minority_status == 1)].shape[0])
print min_app_high

#non minority application counts by tract
non_min_app_low = [low_app_counts[i] - min_app_low[i] for i in range(0, len(min_app_low))]
non_min_app_mid = [mid_app_counts[i] - min_app_mid[i] for i in range(0, len(min_app_mid))]
non_min_app_upp = [upp_app_counts[i] - min_app_upp[i] for i in range(0, len(min_app_upp))]
non_min_app_high = [high_app_counts[i] - min_app_high[i] for i in range(0, len(min_app_high))]
print "non-minority application counts \n", "*"*40
print "low:", non_min_app_low
print "mid:", non_min_app_mid
print "upp:", non_min_app_upp
print "high:", non_min_app_high

#minority origination counts by tract cateogry
min_orig_low = [] #minority origination count for low minority tract
min_orig_low.append(data_2009[(data_2009.tract_cat == 'low') & (data_2009.minority_status == 1)].shape[0])
min_orig_low.append(data_2010[(data_2010.tract_cat == 'low') & (data_2010.minority_status == 1)].shape[0])
min_orig_low.append(data_2011[(data_2011.tract_cat == 'low') & (data_2011.minority_status == 1)].shape[0])
min_orig_low.append(data_2012[(data_2012.tract_cat == 'low') & (data_2012.minority_status == 1)].shape[0])
min_orig_low.append(data_2013[(data_2013.tract_cat == 'low') & (data_2013.minority_status == 1)].shape[0])
print min_orig_low

min_orig_mid = [] #minority origination count ofr middle minority tract
min_orig_mid.append(data_2009[(data_2009.tract_cat == 'middle') & (data_2009.minority_status == 1)].shape[0])
min_orig_mid.append(data_2010[(data_2010.tract_cat == 'middle') & (data_2010.minority_status == 1)].shape[0])
min_orig_mid.append(data_2011[(data_2011.tract_cat == 'middle') & (data_2011.minority_status == 1)].shape[0])
min_orig_mid.append(data_2012[(data_2012.tract_cat == 'middle') & (data_2012.minority_status == 1)].shape[0])
min_orig_mid.append(data_2013[(data_2013.tract_cat == 'middle') & (data_2013.minority_status == 1)].shape[0])
print min_orig_mid

min_orig_upp = [] #minority origination count for upper minority tract
min_orig_upp.append(data_2009[(data_2009.tract_cat == 'upper') & (data_2009.minority_status == 1)].shape[0])
min_orig_upp.append(data_2010[(data_2010.tract_cat == 'upper') & (data_2010.minority_status == 1)].shape[0])
min_orig_upp.append(data_2011[(data_2011.tract_cat == 'upper') & (data_2011.minority_status == 1)].shape[0])
min_orig_upp.append(data_2012[(data_2012.tract_cat == 'upper') & (data_2012.minority_status == 1)].shape[0])
min_orig_upp.append(data_2013[(data_2013.tract_cat == 'upper') & (data_2013.minority_status == 1)].shape[0])
print min_orig_upp

min_orig_high = [] #minority origination count for high minority tract
min_orig_high.append(data_2009[(data_2009.tract_cat == 'high') & (data_2009.minority_status == 1)].shape[0])
min_orig_high.append(data_2010[(data_2010.tract_cat == 'high') & (data_2010.minority_status == 1)].shape[0])
min_orig_high.append(data_2011[(data_2011.tract_cat == 'high') & (data_2011.minority_status == 1)].shape[0])
min_orig_high.append(data_2012[(data_2012.tract_cat == 'high') & (data_2012.minority_status == 1)].shape[0])
min_orig_high.append(data_2013[(data_2013.tract_cat == 'high') & (data_2013.minority_status == 1)].shape[0])
print min_orig_high

#non minority origination counts
non_min_orig_low = [low_orig_counts[i] - min_orig_low[i] for i in range(0, len(min_orig_low))]
non_min_orig_mid = [mid_orig_counts[i] - min_orig_mid[i] for i in range(0, len(min_orig_mid))]
non_min_orig_upp = [upp_orig_counts[i] - min_orig_upp[i] for i in range(0, len(min_orig_upp))]
non_min_orig_high = [high_orig_counts[i] - min_orig_high[i] for i in range(0, len(min_orig_high))]
print "non-minority origination counts \n", "*"*40
print "low:", non_min_orig_low
print "mid:", non_min_orig_mid
print "upp:", non_min_orig_upp
print "high:", non_min_orig_high
#minority approval rates by tract category
min_low_approval_rates = [round((min_orig_low[i]/float(min_app_low[i]))*100,2) for i in range(0, len(min_orig_low))] #approval rates for low minority tracts
min_mid_approval_rates = [round((min_orig_mid[i]/float(min_app_mid[i]))*100,2) for i in range(0, len(min_orig_mid))] #approval rates for mid minority tracts
min_upp_approval_rates = [round((min_orig_upp[i]/float(min_app_upp[i]))*100,2) for i in range(0, len(min_orig_upp))] #approval rates for upper minority tracts
min_high_approval_rates = [round((min_orig_high[i]/float(min_app_high[i]))*100,2) for i in range(0, len(min_orig_high))] #approval rates for high minority tracts
print "minority approval rates\n", "*"*40
print "low:", min_low_approval_rates
print "mid:", min_mid_approval_rates
print "upp:", min_upp_approval_rates
print "high:", min_high_approval_rates

#non minority approval rates by tract category
non_min_low_approval_rates = [round((non_min_orig_low[i]/float(non_min_app_low[i]))*100,2) for i in range(0, len(non_min_orig_low))]
non_min_mid_approval_rates = [round((non_min_orig_mid[i]/float(non_min_app_mid[i]))*100,2) for i in range(0, len(non_min_orig_mid))]
non_min_upp_approval_rates = [round((non_min_orig_upp[i]/float(non_min_app_upp[i]))*100,2) for i in range(0, len(non_min_orig_upp))]
non_min_high_approval_rates = [round((non_min_orig_high[i]/float(non_min_app_high[i]))*100,2) for i in range(0, len(non_min_orig_high))]
print "non minority approval rates\n", "*"*40
print "low:", non_min_low_approval_rates
print "mid:", non_min_mid_approval_rates
print "upp:", non_min_upp_approval_rates
print "high:", non_min_high_approval_rates

axes = figure().add_subplot(111)
a = axes.get_xticks().tolist()
a = years2
axes.set_xticklabels(years2)
plt.plot(years, min_low_approval_rates, marker = 'o', color = 'r', label = 'low minority')
plt.plot(years, min_mid_approval_rates, label='mid minority')
plt.plot(years, min_upp_approval_rates, label='upper minority')
plt.plot(years, min_high_approval_rates, label='high minority')
plt.ylabel('percent')
plt.ylim((0,100))
plt.title('Minority approval rates')
plt.legend(bbox_to_anchor=[1,0], loc='center')
plt.legend()
plt.show()


axes = figure().add_subplot(111)
a = axes.get_xticks().tolist()
a = years2
axes.set_xticklabels(years2)
plt.plot(years, non_min_low_approval_rates, marker = 'o', color = 'r', label = 'low minority')
plt.plot(years, non_min_mid_approval_rates, label='mid minority')
plt.plot(years, non_min_upp_approval_rates, label='upper minority')
plt.plot(years, non_min_high_approval_rates, label='high minority')
plt.ylabel('percent')
plt.ylim((0,100))
plt.title('Non-Minority approval rates')
plt.legend(bbox_to_anchor=[1,0], loc='center')
plt.legend()
plt.show()

#process data to create binary output values and replace NAs
all_dbs['origination_status'] = np.where(all_dbs.actiontype =='1', 1, 0) #convert 1-4 to binary. 1 = origination
all_dbs.applicantincome.replace(to_replace=0, value=all_dbs.applicantincome.median(), inplace = True)
dummies = pd.get_dummies(all_dbs.year)




#print all_dbs.head()
#create a dataframe for the logistic regression, goal is to determine the weight of minority status and minorty tract pct
LogRegCols = ['minority_status', 'applicantincome', 'loanamount', 'median_family_income', 'minority_population_pct']
LogRegCols = all_dbs[LogRegCols].join(dummies.ix[:,'2010':])
#print LogRegCols.head()
X = LogRegCols
y = all_dbs.origination_status
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = .3, random_state =1)
LR = LogisticRegression(penalty='l2')
LR.fit(X_train, y_train)
B = LR.coef_
beta = [b for b in LR.coef_[0]]
beta.append(LR.intercept_[0])
coefs = [np.exp(x) for x in B]
print coefs, 'coefficient list'
B0 = LR.intercept_[0]
print np.exp(B0), "intercept"
scores = cross_val_score(LR, X, y, cv = 3, scoring='roc_auc')
print scores
print np.mean(scores)

#random forest
from sklearn.ensemble import ExtraTreesClassifier as ETC
RF = RF(n_estimators = 100, random_state = 1)
RF.fit(X_train, y_train)

predicted_probs = RF.predict_proba(X_test)
predicted_probs = ["%f" % x[1] for x in predicted_probs]
print RF.score(X_test, y_test)

forest = ETC(n_estimators = 100, random_state = 1, compute_importances = True, )
forest.fit(X_train, y_train)
importances = forest.feature_importances_
std = np.std([tree.feature_importances_ for tree in forest.estimators_], axis = 0)
indices = np.argsort(importances)[::-1]
print "feature importances:"
print importances

pl.figure()
pl.title("feature importances")
pl.bar(xrange(9), importances[indices], color = "b", yerr=std[indices], align='center')
pl.xticks(xrange(9), indices)
pl.xlim([-1,10])
pl.show()
''''

#decision tree model
dec_tree = tree.DecisionTreeClassifier()
dec_tree = dec_tree.fit(X_train, y_train)
dec_tree.predict(y_test)
from sklearn.externals.six import StringIO
import pydot
dot_data = StringIO()
tree.export_graphviz(dec_tree, out_file=dot_data)
graph = pydot.graph_from_dot_data(dot_data.getvalue())
graph.write_pdf("lar.pdf")
'''
'''

#initialize lists of minority and non-minority approval rates for graphing
#baseline graph
min_approvals = [mil_2009.minority_approval_rate, mil_2010.minority_approval_rate, mil_2011.minority_approval_rate, mil_2012.minority_approval_rate, mil_2013.minority_approval_rate]
nonmin_approvals = [mil_2009.nonminority_approval_rate, mil_2010.nonminority_approval_rate, mil_2011.nonminority_approval_rate, mil_2012.nonminority_approval_rate, mil_2013.nonminority_approval_rate]
years = [2009, 2010, 2011, 2012, 2013]
years2 = ['2009', ' ', '2010', ' ', '2011', ' ', '2012', ' ', '2013']
axes = figure().add_subplot(111)
a = axes.get_xticks().tolist()
a = years2
axes.set_xticklabels(years2)
plt.plot(years, min_approvals, marker = 'o', color = 'r', label = 'minority approval rate')
plt.plot(years, nonmin_approvals, label='non-minority approval rate')
plt.ylabel('approval rate')
plt.title('Approval Rates by Minority Status')
plt.legend()
plt.ylim((0,100))
plt.show()



years = [2009, 2010, 2011, 2012, 2013] #x axis for graphs
years2 = ['2009', ' ', '2010', ' ', '2011', ' ', '2012', ' ', '2013'] #use spaces between numbers to fix tick labels on graphs
print "\nnon-minority approval rates\n", "*"*20
print non_min_approvals_high, "high"
print non_min_approvals_upper, "upper"
print non_min_approvals_mid, "mid"
print non_min_approvals_low, "low"
#non-minority approval rate


axes = figure().add_subplot(111)
axes.set_xticklabels(years2)
plt.plot(years, non_min_approvals_low, marker = 'o', color = 'b', label= 'low minority')
plt.plot(years, non_min_approvals_mid, marker = 'o', color = 'r', label = 'middle minority')
plt.plot(years, non_min_approvals_upper, marker = 'o', color = 'k', label = 'upper minority')
plt.plot(years, non_min_approvals_high, marker = 'o', color = 'g', label = 'high minority')
plt.title('Non-minority approval rates')
plt.ylabel('percent')
plt.ylim((0,100))
plt.legend(bbox_to_anchor=[1,0], loc='center')
plt.show()

#% of originations to minorities
axes = figure().add_subplot(111)
axes.set_xticklabels(years2)
plt.plot(years, min_orig_pct_low, marker = 'o', color = 'b', label= 'low minority')
plt.plot(years, min_orig_pct_mid, marker = 'o', color = 'r', label = 'middle minority')
plt.plot(years, min_orig_pct_upper, marker = 'o', color = 'k', label = 'upper minority')
plt.plot(years, min_orig_pct_high, marker = 'o', color = 'g', label = 'high minority')
plt.title('Percent of originations to minorities')
plt.ylabel('percent')
plt.legend(bbox_to_anchor=[1,0], loc='center')
plt.ylim((0,100))
plt.show()

#%of applications by minorities
axes = figure().add_subplot(111)
axes.set_xticklabels(years2)
plt.plot(years, min_app_pct_low, marker = 'o', color = 'b', label= 'low minority')
plt.plot(years, min_app_pct_mid, marker = 'o', color = 'r', label = 'middle minority')
plt.plot(years, min_app_pct_upper, marker = 'o', color = 'k', label = 'upper minority')
plt.plot(years, min_app_pct_high, marker = 'o', color = 'g', label = 'high minority')
plt.title('Percent of applications by minorities')
plt.ylabel('percent')
plt.ylim((0,100))
plt.legend(bbox_to_anchor=[1,0], loc='center')
plt.show()

#minority application count by tract category
axes = figure().add_subplot(111)
a = years2
axes.set_xticklabels(a)
plt.plot(years, app_count_low, marker = 'o', color = 'b', label= 'low minority')
plt.plot(years, app_count_mid, marker = 'o', color = 'r', label = 'middle minority')
plt.plot(years, app_count_upper, marker = 'o', color = 'k', label = 'upper minority')
plt.plot(years, app_count_high, marker = 'o', color = 'g', label = 'high minority')
plt.title('Minority application counts by tract category')
plt.ylabel('count')
plt.legend(bbox_to_anchor=[1,0], loc='center')
plt.show()

#minority origination count by tract category
axes = figure().add_subplot(111)
a = years2
axes.set_xticklabels(a)
plt.plot(years, orig_count_low, marker = 'o', color = 'b', label= 'low minority')
plt.plot(years, orig_count_mid, marker = 'o', color = 'r', label = 'middle minority')
plt.plot(years, orig_count_upper, marker = 'o', color = 'k', label = 'upper minority')
plt.plot(years, orig_count_high, marker = 'o', color = 'g', label = 'high minority')
plt.title('Minority origination counts by tract category')
plt.ylabel('count')
plt.legend(bbox_to_anchor=[1,0], loc='center')
plt.show()

#minority approval rate
axes = figure().add_subplot(111)
a = years2
axes.set_xticklabels(a)
plt.plot(years, minority_approvals_low, marker = 'o', color = 'b', label= 'low minority')
plt.plot(years, minority_approvals_mid, marker = 'o', color = 'r', label = 'middle minority')
plt.plot(years, minority_approvals_upper, marker = 'o', color = 'k', label = 'upper minority')
plt.plot(years, minority_approvals_high, marker = 'o', color = 'g', label = 'high minority')
plt.title('Minority approval rate by tract category')
plt.ylabel('percent')
plt.legend(bbox_to_anchor=[1,0], loc='center')
plt.show()
'''

'''
loans in MSA by tract
owner occupied
1-4 family homes
conventional mortgages
home purchase loans
first lien loans

Analysis:
application count by tract
	minority/non-minority
origination count by tract
	minority/non-minority

compare % of applications originated by tract
	minority/non-minority
compare origination percent (chance?) to minority population percent
	are originations different for minority/non-minority status?
compare minority application % to minority population percent
	are mortgage applications the same by minority status?
use a logit model to predict origination or denial using
	income, location, loan amount race
		determine if minority status was significant in origination decision
use linear regression to check on pricing by minority/non-minority status

minority status percentage by applications (and originations? are these recorded separately?)


'''