# -*- coding: utf-8 -*-
"""
Created on Mon Feb 23 00:49:21 2015

@author: jonbryan90
"""

'''Load Drug_df 1.40 GBs'''
path_2 ='C:\Users\jonbryan90\Desktop\DRUGS_MASTER2'
Drug_df = pd.read_csv(path_2)

'''Makes a Dataframe w/ only records with ROLE_COD = Primary Suspect Drug'''
Drug_PS_df = pd.DataFrame()
Drug_PS_df = Drug_df[Drug_df.ROLE_COD == 'PS']

'''Creates DRUGS_PS_MASTER .csv'''
Drug_PS_df.to_csv('C:\Users\jonbryan90\Desktop\DRUGS_PS_MASTER')