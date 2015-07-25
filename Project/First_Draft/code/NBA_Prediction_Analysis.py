# -*- coding: utf-8 -*-
"""
Created on Wed Jul 18 12:10:44 2015

@author: Nick
"""

from sklearn import metrics
from sklearn import datasets
from sklearn.cluster import KMeans
from sklearn.datasets.samples_generator import make_blobs, make_moons
from sklearn.metrics.pairwise import euclidean_distances
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from sklearn.linear_model import LinearRegression
from sklearn.linear_model import LogisticRegression
from sklearn.cross_validation import train_test_split
import statsmodels.formula.api as smf

import nltk
nltk.download('all')