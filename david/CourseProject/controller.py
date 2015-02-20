#used to control the geo_aggregator and other classes and functions for analysis
#import libraries
import json
import psycopg2
from DAT4_library import queries
#from geo_aggregator_2013 import geo_aggregator
from DAT4_library import connect_DB
from DAT4_library import parse_inputs
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pylab import *
from years_of_milwaukee import call_2009
from years_of_milwaukee import call_2010
from years_of_milwaukee import call_2011
from years_of_milwaukee import call_2012
from years_of_milwaukee import call_2013
from years_of_milwaukee import call_tracts_2013 as tracts_2013
from years_of_milwaukee import call_tracts_2012 as tracts_2012
from years_of_milwaukee import call_tracts_2011 as tracts_2011
from years_of_milwaukee import call_tracts_2010 as tracts_2010
from years_of_milwaukee import call_tracts_2009 as tracts_2009
#instantiate classes
#geo = geo_aggregator() #disabled geo_aggregator as it has been used and is not needed
query = queries()
connect = connect_DB()
parse = parse_inputs()

#instantiate year classes for baseline
mil_2009 = call_2009()
mil_2010 = call_2010()
mil_2011 = call_2011()
mil_2012 = call_2012()
mil_2013 = call_2013()

#instantiate tract classes for tract groups
tract_2013 = tracts_2013()
tract_2012 = tracts_2012()
tract_2011 = tracts_2011()
tract_2010 = tracts_2010()
tract_2009 = tracts_2009()

tract_2013.descriptors_2013()
tract_2012.descriptors_2012()
tract_2011.descriptors_2011()
tract_2010.descriptors_2010()
tract_2009.descriptors_2009()
#open credentials to access database
#cur = connect.connect()
print "\n"
#get counts for loops: applications and originations for 2009-2013
'''data have been filtered as follows
	loan type: conventional only, code 1
	property type: 1-4 family only, code 1
	loan purpose: purchase only, code 1
	occupancy status: owner occupied only, code 1
	lien status: first liens only, code 1
	action type: originations includes only originated loans, applications includes codes 1-4
	these filters were used to standardize the underwriting criteria for the logistic model
	standardizing type also allows comparison on pricing as collateral type, loan type, loan purpose, and occupancy status all affect pricing
'''

'''
No filter lending activity in MSA 33340
2009: applications 124,999, originations 65,761, approval percent = 52.61%
2010: applications 106,160, originations 57,089, approval percent = 53.78%
2011: applications 84128, originations 45,671, approval percent = 54.29%
2012: applications 106,200, originations 64,241, approval percent = 60.49%
2013: applications 81,802, originations 48,194, approval percent = 58.92%

Filtered lending activity in MSA 33340
2009: applications 9288, originations 7380, approval percent = 79.46%
	minority: applications 1389, originations, approval percent = 67.67%
	non-minority: applications , originations, approval percent = 81.53%
2010: appplications , originations, approval percent =
2011: applicaitons , originations , approval percent =
2012: applications , originations , approval percent =
2013: applications , originations , approval percent =
'''
'''
mil_2009.descriptors_2009()
print "\n"
mil_2010.descriptors_2010()
print "\n"
mil_2011.descriptors_2011()
print "\n"
mil_2012.descriptors_2012()
print "\n"
mil_2013.descriptors_2013()

#initialize lists of minority and non-minority approval rates for graphing
#baseline graph
min_approvals = [0, mil_2009.minority_approval_rate, mil_2010.minority_approval_rate, mil_2011.minority_approval_rate, mil_2012.minority_approval_rate, mil_2013.minority_approval_rate]
nonmin_approvals = [0, mil_2009.nonminority_approval_rate, mil_2010.nonminority_approval_rate, mil_2011.nonminority_approval_rate, mil_2012.nonminority_approval_rate, mil_2013.nonminority_approval_rate]
years = [2009, 2010, 2011, 2012, 2013]
years2 = ['0', '2009', '2010', '2011', '2012', '2013']
#plt.plot(x, y, label)
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
'''
#change this to # of applications by minorities
#label bins!
#minority application count by tract category
app_count_low = [tract_2009.min_app_count_low, tract_2010.min_app_count_low, tract_2011.min_app_count_low, tract_2012.min_app_count_low, tract_2013.min_app_count_low]
app_count_mid = [tract_2009.min_app_count_middle, tract_2010.min_app_count_middle, tract_2011.min_app_count_middle, tract_2012.min_app_count_middle, tract_2013.min_app_count_middle]
app_count_upper =[tract_2009.min_app_count_upper, tract_2010.min_app_count_upper, tract_2011.min_app_count_upper, tract_2012.min_app_count_upper, tract_2013.min_app_count_upper]
app_count_high = [tract_2009.min_app_count_high, tract_2010.min_app_count_high, tract_2011.min_app_count_high, tract_2012.min_app_count_high, tract_2013.min_app_count_high]
years = [2009, 2010, 2011, 2012, 2013]
years2 = ['2009',' ', '2010',' ', '2011',' ', '2012',' ', '2013']
axes = figure().add_subplot(111)
a = years2
axes.set_xticklabels(a)
plt.plot(years, app_count_low, marker = 'o', color = 'b', label= 'low minority')
plt.plot(years, app_count_mid, marker = 'o', color = 'r', label = 'middle minority')
plt.plot(years, app_count_upper, marker = 'o', color = 'k', label = 'upper minority')
plt.plot(years, app_count_high, marker = 'o', color = 'g', label = 'high minority')
plt.title('Minority application counts by tract category')
plt.ylabel('count')
plt.legend()
plt.show()

#minority origination count by tract category
orig_count_low = [tract_2009.min_orig_count_low, tract_2010.min_orig_count_low, tract_2011.min_orig_count_low, tract_2012.min_orig_count_low, tract_2013.min_orig_count_low]
orig_count_mid = [tract_2009.min_orig_count_middle, tract_2010.min_orig_count_middle, tract_2011.min_orig_count_middle, tract_2012.min_orig_count_middle, tract_2013.min_orig_count_middle]
orig_count_upper =[tract_2009.min_orig_count_upper, tract_2010.min_orig_count_upper, tract_2011.min_orig_count_upper, tract_2012.min_orig_count_upper, tract_2013.min_orig_count_upper]
orig_count_high = [tract_2009.min_orig_count_high, tract_2010.min_orig_count_high, tract_2011.min_orig_count_high, tract_2012.min_orig_count_high, tract_2013.min_orig_count_high]
axes = figure().add_subplot(111)
a = years2
axes.set_xticklabels(a)
plt.plot(years, orig_count_low, marker = 'o', color = 'b', label= 'low minority')
plt.plot(years, orig_count_mid, marker = 'o', color = 'r', label = 'middle minority')
plt.plot(years, orig_count_upper, marker = 'o', color = 'k', label = 'upper minority')
plt.plot(years, orig_count_high, marker = 'o', color = 'g', label = 'high minority')
plt.title('Minority origination counts by tract category')
plt.ylabel('count')
plt.legend()
plt.show()

#minority approval rate
minority_approvals_low = [round((orig_count_low[i] / float(app_count_low[i])*100),2) for i in range(0,len(app_count_low))]
minority_approvals_mid = [round((orig_count_mid[i] / float(app_count_mid[i])*100),2) for i in range(0,len(app_count_mid))]
minority_approvals_upper = [round((orig_count_upper[i] / float(app_count_upper[i])*100),2) for i in range(0,len(app_count_upper))]
minority_approvals_high = [round((orig_count_high[i] / float(app_count_high[i])*100),2) for i in range(0,len(app_count_high))]
orig_count_low = [tract_2009.min_orig_count_low, tract_2010.min_orig_count_low, tract_2011.min_orig_count_low, tract_2012.min_orig_count_low, tract_2013.min_orig_count_low]
orig_count_mid = [tract_2009.min_orig_count_middle, tract_2010.min_orig_count_middle, tract_2011.min_orig_count_middle, tract_2012.min_orig_count_middle, tract_2013.min_orig_count_middle]
orig_count_upper =[tract_2009.min_orig_count_upper, tract_2010.min_orig_count_upper, tract_2011.min_orig_count_upper, tract_2012.min_orig_count_upper, tract_2013.min_orig_count_upper]
orig_count_high = [tract_2009.min_orig_count_high, tract_2010.min_orig_count_high, tract_2011.min_orig_count_high, tract_2012.min_orig_count_high, tract_2013.min_orig_count_high]
axes = figure().add_subplot(111)
a = years2
axes.set_xticklabels(a)
plt.plot(years, minority_approvals_low, marker = 'o', color = 'b', label= 'low minority')
plt.plot(years, minority_approvals_mid, marker = 'o', color = 'r', label = 'middle minority')
plt.plot(years, minority_approvals_upper, marker = 'o', color = 'k', label = 'upper minority')
plt.plot(years, minority_approvals_high, marker = 'o', color = 'g', label = 'high minority')
plt.title('Minority approval rate by tract category')
plt.ylabel('percent')
plt.legend()
plt.show()

#non minority approval rate

'''
#select MSA and build geo dictionary
#this was run for each year 2009-2013
MSA = ['33340'] #select MSA for Milwaukee
filename = 'MSA_33340_2013' #name the output file
cred_list = credentials.split(',') #split credential string
geo.main(cred_list, MSA) #assemble the JSON object
geo.write_geo_dict(filename) #write the tracts as a JSON object

#list of file paths on github.com for data retrieval
#https://github.com/Kibrael/DAT4-students/blob/master/david/CourseProject/milwaukee2009.csv
#https://github.com/Kibrael/DAT4-students/blob/master/david/CourseProject/milwaukee2010.csv
#https://github.com/Kibrael/DAT4-students/blob/master/david/CourseProject/milwaukee2011.csv
#https://github.com/Kibrael/DAT4-students/blob/master/david/CourseProject/milwaukee2012.csv
#https://github.com/Kibrael/DAT4-students/blob/master/david/CourseProject/milwaukee2013.csv
'''



	#code plan
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