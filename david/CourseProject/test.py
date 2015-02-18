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
#instantiate classes
#geo = geo_aggregator() #disabled geo_aggregator as it has been used and is not needed
query = queries()
connect = connect_DB()
parse = parse_inputs()

#mil_2009 = call_2009()
#mil_2010 = call_2010()
#mil_2011 = call_2011()
#mil_2012 = call_2012()
mil_2013 = call_2013()

class year_calls(object):
	pass

class call_tracts_2013(year_calls):
	def __init__(self):
		self.query = queries() #query object has query texts for all database interactions as different functions
		self.parse = parse_inputs() #parses the LAR row into selected components and stores them in a dictionary
		self.connect = connect_DB() #sets a database connection and passes a cursor back
		self.orig_by_tract_minority_category = [] #sorted alphabetically: high, low, middle, upper
		self.app_by_tract_minority_category = [] #sorted alphabetically: high, low, middle, upper
		self.tract_orig_rates = [] #holds an alphabetically sorted list of origination rates for tract categorized by minority population
		#order of tract_orig_rates list: high, low, middle, upper
		self.nonminority_approval_rate = 0 #establishes a variable to hold rates for graphing
		self.HMDA_cols = ['statecode', 'countycode', 'censustractnumber', 'applicantrace1', 'applicantrace2', 'applicantrace3', 'applicantrace4', 'applicantrace5',
					'coapplicantrace1', 'coapplicantrace2', 'coapplicantrace3', 'coapplicantrace4', 'coapplicantrace5', 'applicantethnicity', 'coapplicantethnicity',
					'applicantincome', 'ratespread', 'lienstatus', 'hoepastatus', 'purchasertype', 'loanamount', 'asofdate', 'hud_median_family_income',
					'minority_population_pct', 'tract_to_msa_md_income']
	def descriptors_2013(self):
		cur = self.connect.connect()
		print "Begin 2013 descriptors\n", "*"*30
		#print "\nMSA baseline application and origination counts\n", "*"*20
		SQL = self.query.count_originations_2013() #set qeury text to pull the count of originations
		cur.execute(SQL) #execute the query
		orig_count_2013 = cur.fetchone()[0] #pull the tuple from the cursor
		#print orig_count_2013, "origination count"

		SQL = self.query.count_applications_2013() #set query text to pull the count of applications
		cur.execute(SQL) #execute the query
		app_count_2013 = cur.fetchone()[0] #set the tuple from the cursor
		#print app_count_2013, "application count" #applications include originations, because they were applications too!
		#print round((orig_count_2013/float(app_count_2013))*100,2), "approval percent"


		#get data for data frame
		SQL = self.query.originations2013() #set query text
		cur.execute(SQL) #execute query against the database
		orig_2013 = pd.DataFrame(cur.fetchall(), columns = self.HMDA_cols) #set the database pull as a dataframe

		#add minority status for 2013 originations dataframe
		orig_2013['minority_status'] = 0 #initialize series in dataframe
		orig_2013['minority_tract_category'] = 0
		tract_cat = [] #create a list to store tract minority percent categories
		minority_status = [] #create a list to store minority flags
		for row in orig_2013.iterrows():
			self.parse.parse(row) #parse database rows to determine minority status
			minority_status.append(self.parse.inputs['minority status']) #append minority flag
			tract_cat.append(self.parse.inputs['minority_tract_category']) #fill the list with flags
		orig_2013['minority_status'] = minority_status #input minority flags into the dataframe
		orig_2013['minority_tract_category'] = tract_cat

		SQL = self.query.applications2013() #set the query text
		cur.execute(SQL) #query the database for application rows
		app_2013 = pd.DataFrame(cur.fetchall(), columns = self.HMDA_cols) #store the query results as a dataframe

		#minority status of 1 is minority 0 is non-minority
		#adding minority status to the 2013 applications dataframe
		app_2013['minority_status'] = 0 #initialize series in dataframe
		app_2013['minority_tract_category'] = 0
		tract_cat = [] #initialize a list to hold the minority tract percent category (low, middle, upper, high)
		minority_status = [] #initialize a list to hold the minority status flags
		for row in app_2013.iterrows():
			self.parse.parse(row) #parse the app_2013 data to determine minority status
			minority_status.append(self.parse.inputs['minority status']) #create a list of minority status flags
			tract_cat.append(self.parse.inputs['minority_tract_category'])
		app_2013['minority_status'] = minority_status #add minority status list data to the dataframe
		app_2013['minority_tract_category'] = tract_cat
		#print app_2013.groupby('minority_tract_category').head(40)
		#print app_2013[['minority_tract_category', 'minority_population_pct']]

		#need counts of tracts in each minority percent category - get from sql with a distinct query?
		print "\napplication count by minority tract category\n", "*"*20
		print app_2013.groupby('minority_tract_category').minority_tract_category.count() #print the count of applications by tract category

		print "\norigination count by minority tract category\n", "*"*20
		print orig_2013.groupby('minority_tract_category').minority_tract_category.count() #print the count of originations by tract category

		for tract in orig_2013.groupby('minority_tract_category').minority_tract_category.count():
			self.orig_by_tract_minority_category.append(tract) #fills the count of originations by tract category
		for tract in app_2013.groupby('minority_tract_category').minority_tract_category.count():
			self.app_by_tract_minority_category.append(tract) #fills the count of applicaitons by tract category


		for i in range(0,4):
			self.tract_orig_rates.append(round((self.orig_by_tract_minority_category[i]/float(self.app_by_tract_minority_category[i])*100),2))

		print "\norigination rates by tract category\n", "*"*20
		print "low:", self.tract_orig_rates[1]
		print "middle:", self.tract_orig_rates[2]
		print "upper:", self.tract_orig_rates[3]
		print "high:", self.tract_orig_rates[0]
		#store minority application counts in the class object for use in graphing
		self.min_app_count_low = app_2013[(app_2013.minority_status == 1) & (app_2013.minority_tract_category == 'low')]['minority_status'].count()
		self.min_app_count_middle = app_2013[(app_2013.minority_status == 1) & (app_2013.minority_tract_category == 'middle')]['minority_status'].count()
		self.min_app_count_upper = app_2013[(app_2013.minority_status == 1) & (app_2013.minority_tract_category == 'upper')]['minority_status'].count()
		self.min_app_count_high = app_2013[(app_2013.minority_status == 1) & (app_2013.minority_tract_category == 'high')]['minority_status'].count()
		#store minority origination counts in the class object for use in graphing
		self.min_orig_count_low = orig_2013[(orig_2013.minority_status ==1)& (orig_2013.minority_tract_category == 'low')]['minority_status'].count()
		self.min_orig_count_middle = orig_2013[(orig_2013.minority_status ==1)& (orig_2013.minority_tract_category == 'middle')]['minority_status'].count()
		self.min_orig_count_upper = orig_2013[(orig_2013.minority_status ==1)& (orig_2013.minority_tract_category == 'upper')]['minority_status'].count()
		self.min_orig_count_high= orig_2013[(orig_2013.minority_status ==1)& (orig_2013.minority_tract_category == 'high')]['minority_status'].count()
		#store total applications by tract type for use in graphing
		self.total_app_count_low = app_2013[app_2013.minority_tract_category == 'low']['minority_status'].count()
		self.total_app_count_middle = app_2013[app_2013.minority_tract_category == 'middle']['minority_status'].count()
		self.total_app_count_upper = app_2013[app_2013.minority_tract_category == 'upper']['minority_status'].count()
		self.total_app_count_high = app_2013[app_2013.minority_tract_category == 'high']['minority_status'].count()
		#store total originations by tract type fo use in graphing
		self.total_orig_count_low = orig_2013[orig_2013.minority_tract_category == 'low']['minority_status'].count()
		self.total_orig_count_middle = orig_2013[orig_2013.minority_tract_category == 'middle']['minority_status'].count()
		self.total_orig_count_upper = orig_2013[orig_2013.minority_tract_category == 'upper']['minority_status'].count()
		self.total_orig_count_high= orig_2013[orig_2013.minority_tract_category == 'high']['minority_status'].count()

		#percent of applications submitted by minorities
		print "\npercent of applications by minorities in tract category\n", "*"*20
		print "low:", round((self.min_app_count_low / float(self.total_app_count_low)*100),2)
		print "middle:", round((self.min_app_count_middle / float(self.total_app_count_middle)*100),2)
		print "upper:", round((self.min_app_count_upper / float(self.total_app_count_upper)*100),2)
		print "high:", round((self.min_app_count_high / float(self.total_app_count_high)*100),2)
		#percent of originations to minority status borrowers
		print "\npercent of originations to minorities by tract category\n", "*"*20
		print "low:", round((self.min_orig_count_low / float(self.total_orig_count_low)*100),2)
		print "middle:", round((self.min_orig_count_middle/ float(self.total_orig_count_middle)*100),2)
		print "upper:", round((self.min_orig_count_upper / float(self.total_orig_count_upper)*100),2)
		print "high:", round((self.min_orig_count_high / float(self.total_orig_count_high)*100),2)
		#approval rate on minority applications
		print "\napproval rate on minority loans by tract category\n", "*"*20
		print "low:", round((self.min_orig_count_low / float(self.min_app_count_low)*100),2)
		print "middle:", round((self.min_orig_count_middle / float(self.min_app_count_middle)*100),2)
		print "upper:", round((self.min_orig_count_upper / float(self.min_app_count_upper)*100),2)
		print "high:", round((self.min_orig_count_high / float(self.min_app_count_high)*100),2)


		'''
		#determine minority and non-minority approval rates for the MSA
		base_percent_orig =  round((orig_count_2013/float(app_count_2013)*100),2)
		#percent of originations that are to minorities
		percent_originations_to_minorities = round((orig_2013.minority_status.value_counts()[1]/float(orig_count_2013)*100),2)
		#percent of applications by minorities
		minority_application_percent = round((app_2013.minority_status.value_counts()[1]/float(app_count_2013)*100),2)
		#percent of minority applications approved
		self.minority_approval_rate = round((orig_2013.minority_status.value_counts()[1]/float(app_2013.minority_status.value_counts()[1])*100),2)
		#approval rate for non-minority status loans
		self.nonminority_approval_rate  = round((orig_2013.minority_status.value_counts()[0]/float(app_2013.minority_status.value_counts()[0])*100),2)

		#format for commas and percents
		#http://quickfacts.census.gov/qfd/states/55/55079.html for % minority in 2013
		print "In Milwaukee during 2013 there were %s total applications, %s total originations, giving a %s orignation rate" %(app_count_2013, orig_count_2013, base_percent_orig)
		print "Minorities submitted %s applications, received %s originations giving an origination rate of %s" %(app_2013.minority_status.value_counts()[1], orig_2013.minority_status.value_counts()[1], self.minority_approval_rate)
		print "Minorities accounted for %s percent of applications, %s percent of originations, and represent 53.4 percent of the MSAs population" %(minority_application_percent, percent_originations_to_minorities)
		print "Non-minority origination rate was %s percent" % (self.nonminority_approval_rate)
		#print total originations, minority originations, minority origination percent
		#print total approvals, minority approvals, % of approvals that are minority
		#print % applications minority, % approvals minority, % minoritypopulation
		#print total approval rate, minority approval rate, non-minority approval rate
		'''
tracts_2013 = call_tracts_2013()

tracts_2013.descriptors_2013()