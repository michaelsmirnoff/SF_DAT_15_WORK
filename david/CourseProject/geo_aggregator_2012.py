class geo_aggregator(object):
	def __init__(self):

		#a dictionary to hold the entire HMDA geocode structure
		#select all geocode identifiers for loans in a chosen MSA/MD
		#for all MSAs in the HMDA file
		self.geo_dictionary = {
						"MSAs":[
								]
							}

	def main(self, cred_list, MSA_list):
			#import psycopg2 to access SQL servers
			import psycopg2
			#parse the cred_list prior ot login
			dbname = cred_list[0]
			user = cred_list[1]
			host = cred_list[2]
			password = cred_list[3]
			#set a string for connection to SQL
			connect_string = "dbname=%s user=%s host=%s password =%s" %(dbname, user, host, password)

			#attempte a connection to the SQL database hosting the LAR information
			try:
				conn = psycopg2.connect(connect_string)
				print "connection successful"
			#if database connection results in an error print the following
			except:
					print "I am unable to connect to the database"

			cur = conn.cursor()

			#MSA_list is a list of all MSAs passed to the geo_aggregator

			#a list to hold states in an MSA
			state_list = []
			#a list to hold all counties in a state
			county_list = []
			#a list to hold all tracts in a county
			tract_list = []

			for msa in range(0, len(MSA_list)): #MSA_list is all unique MSAs in the LAR file
					print msa+1, "of ", len(MSA_list), "\n", "*"*15
					#append one MSA to the MSA list inside the MSAs dictionary
					self.geo_dictionary["MSAs"].append({"MSA number": MSA_list[msa]})

					#this section will have multiple nested loops
					#the first will add an MSA to the dictionary
					#the second will add all states for the MSA to the dictionary
					#the third will add all counties to the states
					#the fourth will add all tracts to the counties

					#set msa_var equal to the last MSA in the list, it must be passed to SQL as a tuple
					msa_var = (MSA_list[msa],) #set the MSA as a tuple so psycopg2 doesn't get mad
					state_list = [] #clear the state list so that no carry over happens from inner to outer loops

					#select all state codes in the MSA
					SQL = '''SELECT statecode
					FROM hmdapub2012
					WHERE msaofproperty = %s
					'''

					cur.execute(SQL, msa_var)
					#fetch the query from SQL
					state_rows = cur.fetchall()
					#print rows, "state codes for msa, ", msa_var

					#create a list of states in the MSA
					#this loop has no nested loops
					self.geo_dictionary["MSAs"][msa]["States"] = []
					#loop over all state values pulled from the LAR, add only unique values for each MSA
					for k in range(0, len(state_rows)):
							#change the row tuple to a string using temp variable
							temp = state_rows[k][0]
							#print temp
							#if the state is not in the list, add it
							if temp not in state_list:
									state_list.append(temp)

					#add each unique state code in the state_list
					for state in range(0, len(state_list)):
							#add each unique state to the list of states in the MSA dictionary
							self.geo_dictionary["MSAs"][msa]["States"].append({"State name": state_list[state]})

							#select all counties for the states in the MSA
							state_var = (state_list[state], MSA_list[msa]) #convert string to tuple for psycopg2
							county_list = []
							SQL = '''SELECT countycode
											FROM hmdapub2012
											WHERE statecode = %s and msaofproperty = %s
											'''
							cur.execute(SQL, state_var)
							#fetch the query from SQL
							county_rows = cur.fetchall() #renamed rows as county_rows to avoid issues with state loops

							self.geo_dictionary["MSAs"][msa]["States"][state]["Counties"] = []

							#this loop adds all unique counties to a list
							#this loop has no nested sub loops
							for c in range(0,len(county_rows)): #loop over each county in the list of unique counties
									temp_county = county_rows[c][0] #convert tuple to string
									if temp_county not in county_list: #if the county is not in the list of counties in the state, add it
											county_list.append(temp_county) #append the value if unique in the list

							for county in range(0,len(county_list)): #loop over the county list
									#add each unique county to its state inside the MSA
									self.geo_dictionary["MSAs"][msa]["States"][state]["Counties"].append({"County name": county_list[county]})

									#select all tracts in the county
									county_var = (county_list[county], state_list[state], MSA_list[msa]) #convert string to tuple for psycopg2
									#print county_var, "county var", "*" * 10
									tract_list = []
									SQL = '''SELECT censustractnumber
													 FROM hmdapub2012
													 where countycode = %s and statecode = %s and msaofproperty = %s
													 '''
									cur.execute(SQL, county_var)
									#fetch the query from SQL
									tract_rows = cur.fetchall()

									self.geo_dictionary["MSAs"][msa]["States"][state]["Counties"][county]["Tracts"] = []

									#this loop adds all unique tracts to a list
									#this loop has no nested sub loops
									for t in range(0, len(tract_rows)):
											temp_tract = tract_rows[t][0]
										#  print temp_tract
											if temp_tract not in tract_list:
													tract_list.append(temp_tract)
									#print tract_list, "tract list"
									for tract in range(0, len(tract_list)): #loop over all tracts in the list
											#add each unique tract to its county inside the state inside the MSA
											self.geo_dictionary["MSAs"][msa]["States"][state]["Counties"][county]["Tracts"].append({"Tract name" : tract_list[tract]})

	def write_geo_dict(self, name): #writes the JSON structure to a file
			import json
			with open(name, 'w') as outfile:
					json.dump(self.geo_dictionary, outfile, indent = 4, ensure_ascii=False)

	def print_geo_dict(self):
		print self.geo_dictionary

	def return_geo_dict(self):
		return self.geo_dictionary