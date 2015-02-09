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

#instantiate classes
#geo = geo_aggregator() #disabled geo_aggregator as it has been used and is not needed
query = queries()
connect = connect_DB()
parse = parse_inputs()
#open credentials to access database
cur = connect.connect()

#get counts for loops: applications and originations for 2009-2013
SQL = query.count_originations_2009()
cur.execute(SQL)
orig_count_2009 = cur.fetchone()[0]
print orig_count_2009
SQL = query.count_applications_2009()
cur.execute(SQL)
app_count_2009 = cur.fetchone()[0]
print app_count_2009

#set header list for data frames
HMDA_cols = ['statecode', 'countycode', 'censustractnumber', 'applicantrace1', 'applicantrace2', 'applicantrace3', 'applicantrace4', 'applicantrace5',
            'coapplicantrace1', 'coapplicantrace2', 'coapplicantrace3', 'coapplicantrace4', 'coapplicantrace5', 'applicantethnicity', 'coapplicantethnicity',
            'applicantincome', 'ratespread', 'lienstatus', 'hoepastatus', 'purchasertype', 'loanamount', 'asofdate', 'hud_median_family_income',
            'minority_population_pct', 'tract_to_msa_md_income']

#get data for data frame
SQL = query.originations2009()
cur.execute(SQL)
orig_2009 = pd.DataFrame(cur.fetchall(), columns = HMDA_cols)
#print orig_2009.head()

SQL = query.applications2009()
cur.execute(SQL)
app_2009 = pd.DataFrame(cur.fetchall(), columns = HMDA_cols)
#print app_2009[0][0]
#app_2009['boomba'] = range(0,1908)
for row in app_2009.iterrows():
    parse.parse(row)
    #print row[1][8:13]
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