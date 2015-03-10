#used to control the geo_aggregator and other classes and functions for analysis
#import libraries
import json
import psycopg2
import psycopg2.extras
from DAT4_library import queries
#from geo_aggregator_2013 import geo_aggregator
from DAT4_library import connect_DB
from DAT4_library import parse_inputs
import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
import matplotlib.pyplot as plt
from sklearn.cross_validation import train_test_split
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


'''
#get dataframe for union of all databases
cur = connect.connect()
SQL = query.all_years_union()
cur.execute(SQL)
all_dbs = pd.DataFrame(cur.fetchall(), columns = tract_2009.HMDA_cols) #how do i reference HMDA cols from an object?
#change year variables to HMDA variables
all_dbs['minority_status'] = 0 #initialize series in dataframe
all_dbs['minority_tract_category'] = 0
tract_cat = [] #create a list to store tract minority percent categories
minority_status = [] #create a list to store minority flags
for row in all_dbs.iterrows():
	parse.parse(row) #parse database rows to determine minority status
	minority_status.append(parse.inputs['minority status']) #append minority flag
	tract_cat.append(parse.inputs['minority_tract_category']) #fill the list with flags
all_dbs['minority_status'] = minority_status #input minority flags into the dataframe
all_dbs['minority_tract_category'] = tract_cat

#print all_dbs.head()
'''
#get descriptive data from tract categories
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

Filtered lending activity in MSA 33340 by tract category of minority pct population
2010--
High: app count: 179, orig count 103, approve rate: 57.54%, pct apps by min: 72.63, pct orig to min: 73.79
Upper: app count 435, orig count 309, approve rate: 71.03%, pct apps by min: 65.98, pct orig to min: 65.98
Middle: app count 219, orig count 155, approve rate: 70.78%, pct apps by min: 49.77, pct orig to min:
Low: app count: 7524, orig count 5991, approve rate: 79.63%, pct apps by min: 9.46
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
min_approvals = [mil_2009.minority_approval_rate, mil_2010.minority_approval_rate, mil_2011.minority_approval_rate, mil_2012.minority_approval_rate, mil_2013.minority_approval_rate]
nonmin_approvals = [mil_2009.nonminority_approval_rate, mil_2010.nonminority_approval_rate, mil_2011.nonminority_approval_rate, mil_2012.nonminority_approval_rate, mil_2013.nonminority_approval_rate]
years = [2009, 2010, 2011, 2012, 2013]
years2 = [2009', ' ', '2010', ' ', '2011', ' ', '2012', ' ', '2013']
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
#set total applications by year to lists
total_app_low = [tract_2009.total_app_count_low, tract_2010.total_app_count_low, tract_2011.total_app_count_low, tract_2012.total_app_count_low, tract_2013.total_app_count_low]
total_app_mid = [tract_2009.total_app_count_middle, tract_2010.total_app_count_middle, tract_2011.total_app_count_middle, tract_2012.total_app_count_middle, tract_2013.total_app_count_middle]
total_app_upper = [tract_2009.total_app_count_upper, tract_2010.total_app_count_upper, tract_2011.total_app_count_upper, tract_2012.total_app_count_upper, tract_2013.total_app_count_upper]
total_app_high = [tract_2009.total_app_count_high, tract_2010.total_app_count_high, tract_2011.total_app_count_high, tract_2012.total_app_count_high, tract_2013.total_app_count_high]
#set total originations by year to lists
total_orig_low = [tract_2009.total_orig_count_low, tract_2010.total_orig_count_low, tract_2011.total_orig_count_low, tract_2012.total_orig_count_low, tract_2013.total_orig_count_low]
total_orig_mid = [tract_2009.total_orig_count_middle, tract_2010.total_orig_count_middle, tract_2011.total_orig_count_middle, tract_2012.total_orig_count_middle, tract_2013.total_orig_count_middle]
total_orig_upper = [tract_2009.total_orig_count_upper, tract_2010.total_orig_count_upper, tract_2011.total_orig_count_upper, tract_2012.total_orig_count_upper, tract_2013.total_orig_count_upper]
total_orig_high = [tract_2009.total_orig_count_high, tract_2010.total_orig_count_high, tract_2011.total_orig_count_high, tract_2012.total_orig_count_high, tract_2013.total_orig_count_high]

#set minority origination counts by year to lists
orig_count_low = [tract_2009.min_orig_count_low, tract_2010.min_orig_count_low, tract_2011.min_orig_count_low, tract_2012.min_orig_count_low, tract_2013.min_orig_count_low]
orig_count_mid = [tract_2009.min_orig_count_middle, tract_2010.min_orig_count_middle, tract_2011.min_orig_count_middle, tract_2012.min_orig_count_middle, tract_2013.min_orig_count_middle]
orig_count_upper =[tract_2009.min_orig_count_upper, tract_2010.min_orig_count_upper, tract_2011.min_orig_count_upper, tract_2012.min_orig_count_upper, tract_2013.min_orig_count_upper]
orig_count_high = [tract_2009.min_orig_count_high, tract_2010.min_orig_count_high, tract_2011.min_orig_count_high, tract_2012.min_orig_count_high, tract_2013.min_orig_count_high]
#set minority application counts by year to lists
app_count_low = [tract_2009.min_app_count_low, tract_2010.min_app_count_low, tract_2011.min_app_count_low, tract_2012.min_app_count_low, tract_2013.min_app_count_low]
app_count_mid = [tract_2009.min_app_count_middle, tract_2010.min_app_count_middle, tract_2011.min_app_count_middle, tract_2012.min_app_count_middle, tract_2013.min_app_count_middle]
app_count_upper =[tract_2009.min_app_count_upper, tract_2010.min_app_count_upper, tract_2011.min_app_count_upper, tract_2012.min_app_count_upper, tract_2013.min_app_count_upper]
app_count_high = [tract_2009.min_app_count_high, tract_2010.min_app_count_high, tract_2011.min_app_count_high, tract_2012.min_app_count_high, tract_2013.min_app_count_high]
#calculate the application count for non-minorities
non_app_count_low = [total_app_low[i] - app_count_low[i] for i in range(0, len(app_count_low))]
non_app_count_mid = [total_app_mid[i] - app_count_mid[i] for i in range(0, len(app_count_mid))]
non_app_count_upper = [total_app_upper[i] - app_count_upper[i] for i in range(0, len(app_count_upper))]
non_app_count_high = [total_app_high[i] - app_count_high[i] for i in range(0, len(app_count_high))]
#calculate the origination count for non-minorities
non_orig_count_low = [total_orig_low[i] - orig_count_low[i] for i in range(0, len(orig_count_low))]
non_orig_count_mid = [total_orig_mid[i] - orig_count_mid[i] for i in range(0, len(orig_count_mid))]
non_orig_count_upper = [total_orig_upper[i] - orig_count_upper[i] for i in range(0, len(orig_count_upper))]
non_orig_count_high = [total_orig_high[i] - orig_count_high[i] for i in range(0, len(orig_count_high))]
#calculate non-minority approval rate for each tract category and add to a list
non_min_approvals_low = [round((non_orig_count_low[i] / float(non_app_count_low[i])*100),2) for i in range(0,len(non_app_count_low))]
non_min_approvals_mid = [round((non_orig_count_mid[i] / float(non_app_count_mid[i])*100),2) for i in range(0,len(non_app_count_mid))]
non_min_approvals_upper = [round((non_orig_count_upper[i] / float(non_app_count_upper[i])*100),2) for i in range(0,len(non_app_count_upper))]
non_min_approvals_high = [round((non_orig_count_high[i] / float(non_app_count_high[i])*100),2) for i in range(0,len(non_app_count_high))]
#calculate minority approval rate for each tract category and add to a list
minority_approvals_low = [round((orig_count_low[i] / float(app_count_low[i])*100),2) for i in range(0,len(app_count_low))]
minority_approvals_mid = [round((orig_count_mid[i] / float(app_count_mid[i])*100),2) for i in range(0,len(app_count_mid))]
minority_approvals_upper = [round((orig_count_upper[i] / float(app_count_upper[i])*100),2) for i in range(0,len(app_count_upper))]
minority_approvals_high = [round((orig_count_high[i] / float(app_count_high[i])*100),2) for i in range(0,len(app_count_high))]
#calculate percent of originations that were to minorities
min_orig_pct_low = [round((orig_count_low[i] / float(total_orig_low[i])*100),2) for i in range(0,len(total_orig_low))]
min_orig_pct_mid = [round((orig_count_mid[i] / float(total_orig_mid[i])*100),2) for i in range(0,len(total_orig_mid))]
min_orig_pct_upper = [round((orig_count_upper[i] / float(total_orig_upper[i])*100),2) for i in range(0,len(total_orig_upper))]
min_orig_pct_high = [round((orig_count_high[i] / float(total_orig_high[i])*100),2) for i in range(0,len(total_orig_high))]
#calculate percent of applications that were by minorities
min_app_pct_low = [round((app_count_low[i] / float(total_app_low[i])*100),2) for i in range(0,len(total_app_low))]
min_app_pct_mid = [round((app_count_mid[i] / float(total_app_mid[i])*100),2) for i in range(0,len(total_app_mid))]
min_app_pct_upper = [round((app_count_upper[i] / float(total_app_upper[i])*100),2) for i in range(0,len(total_app_upper))]
min_app_pct_high = [round((app_count_high[i] / float(total_app_high[i])*100),2) for i in range(0,len(total_app_high))]

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
plt.ylim((0,100))
plt.legend(bbox_to_anchor=[1,0], loc='center')
plt.show()


'''
#select MSA and build geo dictionary
#this was run for each year 2009-2013
MSA = ['33340'] #select MSA for Milwaukee
filename = 'MSA_33340_2013' #name the output file
cred_list = credentials.split(',') #split credential string
geo.main(cred_list, MSA) #assemble the JSON object
geo.write_geo_dict(filename) #write the tracts as a JSON object
'''
#list of file paths on github.com for data retrieval
#https://github.com/Kibrael/DAT4-students/blob/master/david/CourseProject/milwaukee2009.csv
#https://github.com/Kibrael/DAT4-students/blob/master/david/CourseProject/milwaukee2010.csv
#https://github.com/Kibrael/DAT4-students/blob/master/david/CourseProject/milwaukee2011.csv
#https://github.com/Kibrael/DAT4-students/blob/master/david/CourseProject/milwaukee2012.csv
#https://github.com/Kibrael/DAT4-students/blob/master/david/CourseProject/milwaukee2013.csv




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