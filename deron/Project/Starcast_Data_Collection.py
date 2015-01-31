# -*- coding: utf-8 -*-
"""
Created on Sat Jan 24 23:24:09 2015

@author: deronhogans
"""

#NEXT STEPS
#Gather collection endpoints for Startup Sample for the following data:
    #Funds Raised
    # of Employees
    # of Press
#Read captured info into Dataframe
#Build valuation model (ex. #ofEmployee/FundsRaised > .5 = More Future funding?)


import requests
import json
import time 

user_key = "2805358bf877c1b680623630187748a5"

# Get Funds Raised
def get_fundsraised(permalink):
    xparams = {"user_key" : user_key}
    FR_request = requests.get('https://api.crunchbase.com/v/2/organization/%s' % permalink, params=xparams)
    data= json.loads(FR_request.text)
    data= json.loads(FR_request.text)
    for item in data['data']['properties']:
        if item == 'total_funding_usd':
            return data['data']['properties'][item]

TheLeague_FR = get_fundsraised('the-league')
Lizhi_FR = get_fundsraised('lizhi')
CodeHS_FR = get_fundsraised("codehs")
Corp360_FR = get_fundsraised("corporate360")
Shocase_FR = get_fundsraised("shocase")

# Get # of Employees

def get_num_employees(permalink):
    xparams = {"user_key" : user_key}
    Employee_request = requests.get('https://api.crunchbase.com/v/2/organization/%s' % permalink, params=xparams)
    data= json.loads(Employee_request.text)
    for item in data['data']['properties']:
        if item == 'number_of_employees':
            return data['data']['properties'][item]

TheLeague_Num_Employees = get_num_employees('the-league')
Lizhi_Num_Employees = get_num_employees('lizhi')
CodeHS_Num_Employees = get_num_employees('codehs')
Corp360_Num_Employees = get_num_employees('corporate360')
Shocase_Num_Employees = get_num_employees('shocase')

# Get # of Press with Angellist API

