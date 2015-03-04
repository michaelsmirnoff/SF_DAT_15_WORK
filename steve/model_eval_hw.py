# -*- coding: utf-8 -*-
"""
Created on Sun Feb  1 13:08:53 2015

@author: stephenrromanoff
"""

''' 
Model Evaluation Homework

Stephen Romanoff
'''

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

glassdata = pd.read_table('http://archive.ics.uci.edu/ml/machine-learning-databases/glass/glass.data', header=None, sep='|', names=u_cols, index_col='user_id', dtype={'zip_code':str})


