#used to control the geo_aggregator and other classes and functions for analysis

import json
import psycopg2

from geo_aggregator_2013 import geo_aggregator

geo = geo_aggregator()
with open('/Users/roellk/Desktop/Python/credentials.txt', 'r') as f:
    credentials = f.read()

MSA = ['33340']
filename = 'MSA_33340_2013'
cred_list = credentials.split(',')
geo.main(cred_list, MSA)

geo.write_geo_dict(filename)