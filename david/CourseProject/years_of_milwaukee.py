import psycopg2
from DAT4_library import queries
from DAT4_library import connect_DB
from DAT4_library import parse_inputs
import pandas as pd
class year_calls(object):

	def __init__(self):
		pass

class call_2009(year_calls):
	def __init__(self):
		self.query = queries()
		self.parse = parse_inputs()
		self.connect = connect_DB()
		self.minority_approval_rate = 0
		self.nonminority_approval_rate = 0
		self.HMDA_cols = ['statecode', 'countycode', 'censustractnumber', 'applicantrace1', 'applicantrace2', 'applicantrace3', 'applicantrace4', 'applicantrace5',
					'coapplicantrace1', 'coapplicantrace2', 'coapplicantrace3', 'coapplicantrace4', 'coapplicantrace5', 'applicantethnicity', 'coapplicantethnicity',
					'applicantincome', 'ratespread', 'lienstatus', 'hoepastatus', 'purchasertype', 'loanamount', 'asofdate', 'hud_median_family_income',
					'minority_population_pct', 'tract_to_msa_md_income']
	def descriptors_2009(self):
		cur = self.connect.connect()
		print "Begin 2009 descriptors\n", "*"*30
		#print "\nMSA baseline application and origination counts\n", "*"*20
		SQL = self.query.count_originations_2009()
		cur.execute(SQL)
		orig_count_2009 = cur.fetchone()[0]
		#print orig_count_2009, "origination count"

		SQL = self.query.count_applications_2009()
		cur.execute(SQL)
		app_count_2009 = cur.fetchone()[0]
		#print app_count_2009, "application count" #applications include originations, because they were applications too!
		#print round((orig_count_2009/float(app_count_2009))*100,2), "approval percent"


		#get data for data frame
		SQL = self.query.originations2009()
		cur.execute(SQL)
		orig_2009 = pd.DataFrame(cur.fetchall(), columns = self.HMDA_cols)

		#add minority status for 2009 originations dataframe
		orig_2009['minority_status'] = 0 #initialize series in dataframe
		minority_status = [] #create a list to store minority flags
		for row in orig_2009.iterrows():
			self.parse.parse(row) #parse database rows to determine minority status
			minority_status.append(self.parse.inputs['minority status']) #append minority flag
		orig_2009['minority_status'] = minority_status #input minority flags into the dataframe

		SQL = self.query.applications2009() #set the query text
		cur.execute(SQL) #query the database for application rows
		app_2009 = pd.DataFrame(cur.fetchall(), columns = self.HMDA_cols) #store the query results as a dataframe

		#minority status of 1 is minority 0 is non-minority
		#adding minority status to the 2009 applications dataframe
		app_2009['minority_status'] = 0 #initialize series in dataframe
		minority_status = [] #initialize a list to hold the minority status flags
		for row in app_2009.iterrows():
			self.parse.parse(row) #parse the app_2009 data to determine minority status
			minority_status.append(self.parse.inputs['minority status']) #create a list of minority status flags
		app_2009['minority_status'] = minority_status #add minority status list data to the dataframe

		#determine minority and non-minority approval rates for the MSA
		base_percent_orig =  round((orig_count_2009/float(app_count_2009)*100),2)
		#percent of originations that are to minorities
		percent_originations_to_minorities = round((orig_2009.minority_status.value_counts()[1]/float(orig_count_2009)*100),2)
		#percent of applications by minorities
		minority_application_percent = round((app_2009.minority_status.value_counts()[1]/float(app_count_2009)*100),2)
		#percent of minority applications approved
		self.minority_approval_rate= round((orig_2009.minority_status.value_counts()[1]/float(app_2009.minority_status.value_counts()[1])*100),2)
		self.nonminority_approval_rate  = round((orig_2009.minority_status.value_counts()[0]/float(app_2009.minority_status.value_counts()[0])*100),2)

		#format for commas and percents
		print "In Milwaukee during 2009 there were %s total applications, %s total originations, giving a %s orignation rate" %(app_count_2009, orig_count_2009, base_percent_orig)
		print "Minorities submitted %s applications, received %s originations giving an origination rate of %s" %(app_2009.minority_status.value_counts()[1], orig_2009.minority_status.value_counts()[1], self.minority_approval_rate)
		print "Minorities accounted for %s percent of applications, %s percent of originations, and represent 53.4 percent of the MSAs population" %(minority_application_percent, percent_originations_to_minorities)
		print "Non-minority origination rate was %s percent" % (self.nonminority_approval_rate)
		#print total originations, minority originations, minority origination percent
		#print total approvals, minority approvals, % of approvals that are minority
		#print % applications minority, % approvals minority, % minoritypopulation
		#print total approval rate, minority approval rate, non-minority approval rate



class call_2010(year_calls):
	def __init__(self):
		self.query = queries()
		self.parse = parse_inputs()
		self.connect = connect_DB()
		self.minority_approval_rate = 0
		self.nonminority_approval_rate = 0
		self.HMDA_cols = ['statecode', 'countycode', 'censustractnumber', 'applicantrace1', 'applicantrace2', 'applicantrace3', 'applicantrace4', 'applicantrace5',
					'coapplicantrace1', 'coapplicantrace2', 'coapplicantrace3', 'coapplicantrace4', 'coapplicantrace5', 'applicantethnicity', 'coapplicantethnicity',
					'applicantincome', 'ratespread', 'lienstatus', 'hoepastatus', 'purchasertype', 'loanamount', 'asofdate', 'hud_median_family_income',
					'minority_population_pct', 'tract_to_msa_md_income']
	def descriptors_2010(self):
		cur = self.connect.connect()
		print "Begin 2010 descriptors\n", "*"*30
		#print "\nMSA baseline application and origination counts\n", "*"*20
		SQL = self.query.count_originations_2010()
		cur.execute(SQL)
		orig_count_2010 = cur.fetchone()[0]
		#print orig_count_2010, "origination count"

		SQL = self.query.count_applications_2010()
		cur.execute(SQL)
		app_count_2010 = cur.fetchone()[0]
		#print app_count_2010, "application count" #applications include originations, because they were applications too!
		#print round((orig_count_2010/float(app_count_2010))*100,2), "approval percent"


		#get data for data frame
		SQL = self.query.originations2010()
		cur.execute(SQL)
		orig_2010 = pd.DataFrame(cur.fetchall(), columns = self.HMDA_cols)

		#add minority status for 2010 originations dataframe
		orig_2010['minority_status'] = 0 #initialize series in dataframe
		minority_status = [] #create a list to store minority flags
		for row in orig_2010.iterrows():
			self.parse.parse(row) #parse database rows to determine minority status
			minority_status.append(self.parse.inputs['minority status']) #append minority flag
		orig_2010['minority_status'] = minority_status #input minority flags into the dataframe

		SQL = self.query.applications2010() #set the query text
		cur.execute(SQL) #query the database for application rows
		app_2010 = pd.DataFrame(cur.fetchall(), columns = self.HMDA_cols) #store the query results as a dataframe

		#minority status of 1 is minority 0 is non-minority
		#adding minority status to the 2010 applications dataframe
		app_2010['minority_status'] = 0 #initialize series in dataframe
		minority_status = [] #initialize a list to hold the minority status flags
		for row in app_2010.iterrows():
			self.parse.parse(row) #parse the app_2010 data to determine minority status
			minority_status.append(self.parse.inputs['minority status']) #create a list of minority status flags
		app_2010['minority_status'] = minority_status #add minority status list data to the dataframe

		#determine minority and non-minority approval rates for the MSA
		base_percent_orig =  round((orig_count_2010/float(app_count_2010)*100),2)
		#percent of originations that are to minorities
		percent_originations_to_minorities = round((orig_2010.minority_status.value_counts()[1]/float(orig_count_2010)*100),2)
		#percent of applications by minorities
		minority_application_percent = round((app_2010.minority_status.value_counts()[1]/float(app_count_2010)*100),2)
		#percent of minority applications approved
		self.minority_approval_rate = round((orig_2010.minority_status.value_counts()[1]/float(app_2010.minority_status.value_counts()[1])*100),2)
		self.nonminority_approval_rate  = round((orig_2010.minority_status.value_counts()[0]/float(app_2010.minority_status.value_counts()[0])*100),2)

		#format for commas and percents
		print "In Milwaukee during 2010 there were %s total applications, %s total originations, giving a %s orignation rate" %(app_count_2010, orig_count_2010, base_percent_orig)
		print "Minorities submitted %s applications, received %s originations giving an origination rate of %s" %(app_2010.minority_status.value_counts()[1], orig_2010.minority_status.value_counts()[1], self.minority_approval_rate)
		print "Minorities accounted for %s percent of applications, %s percent of originations, and represent 53.4 percent of the MSAs population" %(minority_application_percent, percent_originations_to_minorities)
		print "Non-minority origination rate was %s percent" % (self.nonminority_approval_rate)
		#print total originations, minority originations, minority origination percent
		#print total approvals, minority approvals, % of approvals that are minority
		#print % applications minority, % approvals minority, % minoritypopulation
		#print total approval rate, minority approval rate, non-minority approval rate

class call_2011(year_calls):
	def __init__(self):
		self.query = queries()
		self.parse = parse_inputs()
		self.connect = connect_DB()
		self.minority_approval_rate = 0
		self.nonminority_approval_rate = 0
		self.HMDA_cols = ['statecode', 'countycode', 'censustractnumber', 'applicantrace1', 'applicantrace2', 'applicantrace3', 'applicantrace4', 'applicantrace5',
					'coapplicantrace1', 'coapplicantrace2', 'coapplicantrace3', 'coapplicantrace4', 'coapplicantrace5', 'applicantethnicity', 'coapplicantethnicity',
					'applicantincome', 'ratespread', 'lienstatus', 'hoepastatus', 'purchasertype', 'loanamount', 'asofdate', 'hud_median_family_income',
					'minority_population_pct', 'tract_to_msa_md_income']
	def descriptors_2011(self):
		cur = self.connect.connect()
		print "Begin 2011 descriptors\n", "*"*30
		#print "\nMSA baseline application and origination counts\n", "*"*20
		SQL = self.query.count_originations_2011()
		cur.execute(SQL)
		orig_count_2011 = cur.fetchone()[0]
		#print orig_count_2011, "origination count"

		SQL = self.query.count_applications_2011()
		cur.execute(SQL)
		app_count_2011 = cur.fetchone()[0]
		#print app_count_2011, "application count" #applications include originations, because they were applications too!
		#print round((orig_count_2011/float(app_count_2011))*100,2), "approval percent"


		#get data for data frame
		SQL = self.query.originations2011()
		cur.execute(SQL)
		orig_2011 = pd.DataFrame(cur.fetchall(), columns = self.HMDA_cols)

		#add minority status for 2011 originations dataframe
		orig_2011['minority_status'] = 0 #initialize series in dataframe
		minority_status = [] #create a list to store minority flags
		for row in orig_2011.iterrows():
			self.parse.parse(row) #parse database rows to determine minority status
			minority_status.append(self.parse.inputs['minority status']) #append minority flag
		orig_2011['minority_status'] = minority_status #input minority flags into the dataframe

		SQL = self.query.applications2011() #set the query text
		cur.execute(SQL) #query the database for application rows
		app_2011 = pd.DataFrame(cur.fetchall(), columns = self.HMDA_cols) #store the query results as a dataframe

		#minority status of 1 is minority 0 is non-minority
		#adding minority status to the 2011 applications dataframe
		app_2011['minority_status'] = 0 #initialize series in dataframe
		minority_status = [] #initialize a list to hold the minority status flags
		for row in app_2011.iterrows():
			self.parse.parse(row) #parse the app_2011 data to determine minority status
			minority_status.append(self.parse.inputs['minority status']) #create a list of minority status flags
		app_2011['minority_status'] = minority_status #add minority status list data to the dataframe

		#determine minority and non-minority approval rates for the MSA
		base_percent_orig =  round((orig_count_2011/float(app_count_2011)*100),2)
		#percent of originations that are to minorities
		percent_originations_to_minorities = round((orig_2011.minority_status.value_counts()[1]/float(orig_count_2011)*100),2)
		#percent of applications by minorities
		minority_application_percent = round((app_2011.minority_status.value_counts()[1]/float(app_count_2011)*100),2)
		#percent of minority applications approved
		self.minority_approval_rate = round((orig_2011.minority_status.value_counts()[1]/float(app_2011.minority_status.value_counts()[1])*100),2)
		self.nonminority_approval_rate  = round((orig_2011.minority_status.value_counts()[0]/float(app_2011.minority_status.value_counts()[0])*100),2)

		#format for commas and percents
		print "In Milwaukee during 2011 there were %s total applications, %s total originations, giving a %s orignation rate" %(app_count_2011, orig_count_2011, base_percent_orig)
		print "Minorities submitted %s applications, received %s originations giving an origination rate of %s" %(app_2011.minority_status.value_counts()[1], orig_2011.minority_status.value_counts()[1], self.minority_approval_rate)
		print "Minorities accounted for %s percent of applications, %s percent of originations, and represent 53.4 percent of the MSAs population" %(minority_application_percent, percent_originations_to_minorities)
		print "Non-minority origination rate was %s percent" % (self.nonminority_approval_rate)
		#print total originations, minority originations, minority origination percent
		#print total approvals, minority approvals, % of approvals that are minority
		#print % applications minority, % approvals minority, % minoritypopulation
		#print total approval rate, minority approval rate, non-minority approval rate

class call_2012(year_calls):
	def __init__(self):
		self.query = queries()
		self.parse = parse_inputs()
		self.connect = connect_DB()
		self.minority_approval_rate = 0
		self.nonminority_approval_rate = 0
		self.HMDA_cols = ['statecode', 'countycode', 'censustractnumber', 'applicantrace1', 'applicantrace2', 'applicantrace3', 'applicantrace4', 'applicantrace5',
					'coapplicantrace1', 'coapplicantrace2', 'coapplicantrace3', 'coapplicantrace4', 'coapplicantrace5', 'applicantethnicity', 'coapplicantethnicity',
					'applicantincome', 'ratespread', 'lienstatus', 'hoepastatus', 'purchasertype', 'loanamount', 'asofdate', 'hud_median_family_income',
					'minority_population_pct', 'tract_to_msa_md_income']
	def descriptors_2012(self):
		cur = self.connect.connect()
		print "Begin 2012 descriptors\n", "*"*30
		#print "\nMSA baseline application and origination counts\n", "*"*20
		SQL = self.query.count_originations_2012()
		cur.execute(SQL)
		orig_count_2012 = cur.fetchone()[0]
		#print orig_count_2012, "origination count"

		SQL = self.query.count_applications_2012()
		cur.execute(SQL)
		app_count_2012 = cur.fetchone()[0]
		#print app_count_2012, "application count" #applications include originations, because they were applications too!
		#print round((orig_count_2012/float(app_count_2012))*100,2), "approval percent"


		#get data for data frame
		SQL = self.query.originations2012()
		cur.execute(SQL)
		orig_2012 = pd.DataFrame(cur.fetchall(), columns = self.HMDA_cols)

		#add minority status for 2012 originations dataframe
		orig_2012['minority_status'] = 0 #initialize series in dataframe
		minority_status = [] #create a list to store minority flags
		for row in orig_2012.iterrows():
			self.parse.parse(row) #parse database rows to determine minority status
			minority_status.append(self.parse.inputs['minority status']) #append minority flag
		orig_2012['minority_status'] = minority_status #input minority flags into the dataframe

		SQL = self.query.applications2012() #set the query text
		cur.execute(SQL) #query the database for application rows
		app_2012 = pd.DataFrame(cur.fetchall(), columns = self.HMDA_cols) #store the query results as a dataframe

		#minority status of 1 is minority 0 is non-minority
		#adding minority status to the 2012 applications dataframe
		app_2012['minority_status'] = 0 #initialize series in dataframe
		minority_status = [] #initialize a list to hold the minority status flags
		for row in app_2012.iterrows():
			self.parse.parse(row) #parse the app_2012 data to determine minority status
			minority_status.append(self.parse.inputs['minority status']) #create a list of minority status flags
		app_2012['minority_status'] = minority_status #add minority status list data to the dataframe

		#determine minority and non-minority approval rates for the MSA
		base_percent_orig =  round((orig_count_2012/float(app_count_2012)*100),2)
		#percent of originations that are to minorities
		percent_originations_to_minorities = round((orig_2012.minority_status.value_counts()[1]/float(orig_count_2012)*100),2)
		#percent of applications by minorities
		minority_application_percent = round((app_2012.minority_status.value_counts()[1]/float(app_count_2012)*100),2)
		#percent of minority applications approved
		self.minority_approval_rate = round((orig_2012.minority_status.value_counts()[1]/float(app_2012.minority_status.value_counts()[1])*100),2)
		self.nonminority_approval_rate  = round((orig_2012.minority_status.value_counts()[0]/float(app_2012.minority_status.value_counts()[0])*100),2)

		#format for commas and percents
		print "In Milwaukee during 2012 there were %s total applications, %s total originations, giving a %s orignation rate" %(app_count_2012, orig_count_2012, base_percent_orig)
		print "Minorities submitted %s applications, received %s originations giving an origination rate of %s" %(app_2012.minority_status.value_counts()[1], orig_2012.minority_status.value_counts()[1], self.minority_approval_rate)
		print "Minorities accounted for %s percent of applications, %s percent of originations, and represent 53.4 percent of the MSAs population" %(minority_application_percent, percent_originations_to_minorities)
		print "Non-minority origination rate was %s percent" % (self.nonminority_approval_rate)
		#print total originations, minority originations, minority origination percent
		#print total approvals, minority approvals, % of approvals that are minority
		#print % applications minority, % approvals minority, % minoritypopulation
		#print total approval rate, minority approval rate, non-minority approval rate

class call_2013(year_calls):
	def __init__(self):
		self.query = queries()
		self.parse = parse_inputs()
		self.connect = connect_DB()
		self.minority_approval_rate = 0
		self.nonminority_approval_rate = 0
		self.HMDA_cols = ['statecode', 'countycode', 'censustractnumber', 'applicantrace1', 'applicantrace2', 'applicantrace3', 'applicantrace4', 'applicantrace5',
					'coapplicantrace1', 'coapplicantrace2', 'coapplicantrace3', 'coapplicantrace4', 'coapplicantrace5', 'applicantethnicity', 'coapplicantethnicity',
					'applicantincome', 'ratespread', 'lienstatus', 'hoepastatus', 'purchasertype', 'loanamount', 'asofdate', 'hud_median_family_income',
					'minority_population_pct', 'tract_to_msa_md_income']
	def descriptors_2013(self):
		cur = self.connect.connect()
		print "Begin 2013 descriptors\n", "*"*30
		#print "\nMSA baseline application and origination counts\n", "*"*20
		SQL = self.query.count_originations_2013()
		cur.execute(SQL)
		orig_count_2013 = cur.fetchone()[0]
		#print orig_count_2013, "origination count"

		SQL = self.query.count_applications_2013()
		cur.execute(SQL)
		app_count_2013 = cur.fetchone()[0]
		#print app_count_2013, "application count" #applications include originations, because they were applications too!
		#print round((orig_count_2013/float(app_count_2013))*100,2), "approval percent"


		#get data for data frame
		SQL = self.query.originations2013()
		cur.execute(SQL)
		orig_2013 = pd.DataFrame(cur.fetchall(), columns = self.HMDA_cols)

		#add minority status for 2013 originations dataframe
		orig_2013['minority_status'] = 0 #initialize series in dataframe
		minority_status = [] #create a list to store minority flags
		for row in orig_2013.iterrows():
			self.parse.parse(row) #parse database rows to determine minority status
			minority_status.append(self.parse.inputs['minority status']) #append minority flag
		orig_2013['minority_status'] = minority_status #input minority flags into the dataframe

		SQL = self.query.applications2013() #set the query text
		cur.execute(SQL) #query the database for application rows
		app_2013 = pd.DataFrame(cur.fetchall(), columns = self.HMDA_cols) #store the query results as a dataframe

		#minority status of 1 is minority 0 is non-minority
		#adding minority status to the 2013 applications dataframe
		app_2013['minority_status'] = 0 #initialize series in dataframe
		minority_status = [] #initialize a list to hold the minority status flags
		for row in app_2013.iterrows():
			self.parse.parse(row) #parse the app_2013 data to determine minority status
			minority_status.append(self.parse.inputs['minority status']) #create a list of minority status flags
		app_2013['minority_status'] = minority_status #add minority status list data to the dataframe

		#determine minority and non-minority approval rates for the MSA
		base_percent_orig =  round((orig_count_2013/float(app_count_2013)*100),2)
		#percent of originations that are to minorities
		percent_originations_to_minorities = round((orig_2013.minority_status.value_counts()[1]/float(orig_count_2013)*100),2)
		#percent of applications by minorities
		minority_application_percent = round((app_2013.minority_status.value_counts()[1]/float(app_count_2013)*100),2)
		#percent of minority applications approved
		self.minority_approval_rate = round((orig_2013.minority_status.value_counts()[1]/float(app_2013.minority_status.value_counts()[1])*100),2)
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

