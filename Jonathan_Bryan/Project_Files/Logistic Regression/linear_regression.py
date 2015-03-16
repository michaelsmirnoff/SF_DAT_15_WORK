# -*- coding: utf-8 -*-
"""
Created on Wed Jan 21 18:30:20 2015

@author: jonbryan90
"""

#imports
import pandas as pd
import matplotlib.pyplot as plt

#read data into DataFrame
data = pd.read_csv('http://www.bcf.usc.edu/~gareth/ISL/Advertising.csv', index_col=0)
data.head()

#print the shape of the DataFrame
data.shape
