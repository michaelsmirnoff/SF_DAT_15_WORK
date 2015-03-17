# -*- coding: utf-8 -*-
"""
Created on Sun Feb 15 23:23:16 2015

@author: jonbryan90
"""
import pandas as pd
import numpy as np

'''Load Lanthier data (644 records)'''
path ='C:\Users\jonbryan90\Desktop\DS_MASTER_DATA.csv'
Master_df = pd.read_csv(path)

'''Load Drugs_PS_df (5,823,558 records)'''
path_2 ='C:\Users\jonbryan90\Desktop\DRUGS_PS_MASTER'
Drug_PS_df = pd.read_csv(path_2, low_memory =False)

'''Load Outcome_df (5,159,924 records)'''
path_3 ='C:\Users\jonbryan90\Desktop\OUTCOME_MASTER2'
Outcome_df = pd.read_csv(path_3, low_memory=False)

'''Load Demo_df (5,791,481 records)'''
path_3 ='C:\Users\jonbryan90\Desktop\DEMO_MASTER2'
Demo_df = pd.read_csv(path_3, low_memory=False)

'''
Drop Master_df extra columns 18-90(extra rows from Excel), rows 645-659(extra rows from Excel), 
and rename columns w/ spaces to have underscores
'''
Master_df = Master_df.drop(Master_df.columns[range(18,91)], axis=1)
Master_df = Master_df.drop(Master_df.index[645:660])
Master_df = Master_df.rename(columns={'Approval Year': 'Approval_Year',
                                      'Trade Name': 'Trade_Name',
                                      'Active Ingredient(s)': 'Active_Ing',
                                      'Innovation Category': 'Innovation_Cat',
                                      'Top 25 Company': 'Top_25'})
                                      
'''
Add 'Trade Name' Firmagon to [Trade Name][557]
Add Nucynta to [Trade Name][571]
Change Eprex/Procrit to Exprex
Change Semprex-D to Semprex
Change Spiriva Handihaler to Spiriva
Change Levulan Kerastick to Levulan
Change Terazol 7 to Terazol
Change Alferon N Injection to Alferon
Change Mefloquine Hydrochloride to Mefloquine
Remove duplicate Trovan
'''
Master_df['Trade_Name'][557] = 'Firmagon'
Master_df['Trade_Name'][571] = 'Nucynta'
Master_df['Trade_Name'][495] = 'Spiriva'
Master_df['Trade_Name'][194] = 'Eprex'
Master_df['Trade_Name'][165] = 'Semprex'
Master_df['Trade_Name'][334] = 'Levulan'
Master_df['Trade_Name'][16] = 'Terazol'
Master_df['Trade_Name'][50] = 'Alferon'
Master_df['Trade_Name'][52] = 'Mefloquine'
Master_df = Master_df.drop(Master_df.index[298])

'''
Captializes the text in the Innovation_Cat column because the
original values had different cases and created more than 3 distinct categories
i.e. ADDTIION TO CLASS, ADVANCE IN CLASS, and FIRST IN CLASS
'''
Master_df['Innovation_Cat'] = Master_df['Innovation_Cat'].str.upper()

'''Populate Num_Adv_Event Column'''
Master_df['Num_Adv_Event'] = 0
for index, row in Master_df.iterrows():
       string = row['Trade_Name']
       Master_df['Num_Adv_Event'][index] = Drug_PS_df['DRUGNAME'].str.contains(string, case=False).sum()
       print string + ' ' + str(Master_df['Num_Adv_Event'][index])

'''Populate Norm_Adv_Event Column'''
Master_df['Norm_Adv_Event'] = (Master_df['Num_Adv_Event'] - Master_df['Num_Adv_Event'].min()) / (Master_df['Num_Adv_Event'].max() - Master_df['Num_Adv_Event'].min())

'''
Creates dictionary 'trade_and isr' with 'Trade_Name' as key and 
values as list of associated ISRs from Drug_PS_df
('ISR' is key used for Outcome_df)

This is because the Outcome_df does not contain the 'Trade_Name' but only the ISRs
associated with each adverse event report
'''
bool_isr = pd.Series()
isr = []
trade_and_isr = {}
for index, row in Master_df.iterrows(): #retrieves each index and row from Master_df (Lanthier data, 645 records)
    string = row['Trade_Name'] #extracts the string from 'Trade_Name'
    bool_isr = Drug_PS_df['DRUGNAME'].str.contains(string, case=False) #creates a boolean series (bool_isr) of each entries from Drug_PS_Df['DRUGNAME'] that contains the 'Trade_Name'
    for index_2, item in bool_isr.iteritems(): #iterates through the boolean series bool_isr
        if item == True: #finds all of the True entries (i.e. if the 'Trade_Name' was in Drug_PS_df['DRUGNAME'])
            isr.append(Drug_PS_df['ISR'][index_2]) #appends each ISR from Drug_PS_df that had a True value from bool_isr
    trade_and_isr[string] = isr #adds the 'Trade_Name' as key and the full list of 'ISR's as the value to the 'trade_and_isr' dictionary
    isr = [] #resets the 'isr' list to null
    print str(len(trade_and_isr[string])) #prints the length so I know the length of the ISR list for each key matches the Num_Adv_Event column

'''Populate Num_Other Column '''
new_Outcome_df = pd.DataFrame() 
isr_OT = {}
for key in trade_and_isr:
    print key
    if trade_and_isr[key] == []:
        print key + ' has no ISRs'
    else:
        new_Outcome_df = Outcome_df.drop(['YEAR', 'QTR'] , axis=1)
        new_Outcome_df = new_Outcome_df.drop([new_Outcome_df.columns[0]], axis=1)
        ISR_list = trade_and_isr[key]
        ISR_list = map(int, ISR_list)
        isr_OT['ISR'] = ISR_list
        isr_OT['OUTC_COD'] = ['OT']
        key_index = int(Master_df[Master_df.Trade_Name == key].index)
        Master_df.loc[key_index,'Num_Other'] = new_Outcome_df.isin(isr_OT).all(1).sum()
        print key + ' ' + str(Master_df.loc[key_index,'Num_Other'])
    

'''Populate Num_Life_Threat Column '''
new_Outcome_df = pd.DataFrame() 
isr_OT = {}
for key in trade_and_isr:
    print key
    if trade_and_isr[key] == []:
        print key + ' has no ISRs'
    else:
        new_Outcome_df = Outcome_df.drop(['YEAR', 'QTR'] , axis=1)
        new_Outcome_df = new_Outcome_df.drop([new_Outcome_df.columns[0]], axis=1)
        ISR_list = trade_and_isr[key]
        ISR_list = map(int, ISR_list)
        isr_OT['ISR'] = ISR_list
        isr_OT['OUTC_COD'] = ['LT']
        key_index = int(Master_df[Master_df.Trade_Name == key].index)
        Master_df.loc[key_index,'Num_Life_Threat'] = new_Outcome_df.isin(isr_OT).all(1).sum()
        print key + ' ' + str(Master_df.loc[key_index,'Num_Life_Threat'])
        
'''Populate Num_Hosp Column '''
new_Outcome_df = pd.DataFrame() 
isr_OT = {}
for key in trade_and_isr:
    print key
    if trade_and_isr[key] == []:
        print key + ' has no ISRs'
    else:
        new_Outcome_df = Outcome_df.drop(['YEAR', 'QTR'] , axis=1)
        new_Outcome_df = new_Outcome_df.drop([new_Outcome_df.columns[0]], axis=1)
        ISR_list = trade_and_isr[key]
        ISR_list = map(int, ISR_list)
        isr_OT['ISR'] = ISR_list
        isr_OT['OUTC_COD'] = ['HO']
        key_index = int(Master_df[Master_df.Trade_Name == key].index)
        Master_df.loc[key_index,'Num_Hosp'] = new_Outcome_df.isin(isr_OT).all(1).sum()
        print key + ' ' + str(Master_df.loc[key_index,'Num_Hosp'])
        
'''Populate Num_Congen_Anom Column '''
new_Outcome_df = pd.DataFrame() 
isr_OT = {}
for key in trade_and_isr:
    print key
    if trade_and_isr[key] == []:
        print key + ' has no ISRs'
    else:
        new_Outcome_df = Outcome_df.drop(['YEAR', 'QTR'] , axis=1)
        new_Outcome_df = new_Outcome_df.drop([new_Outcome_df.columns[0]], axis=1)
        ISR_list = trade_and_isr[key]
        ISR_list = map(int, ISR_list)
        isr_OT['ISR'] = ISR_list
        isr_OT['OUTC_COD'] = ['CA']
        key_index = int(Master_df[Master_df.Trade_Name == key].index)
        Master_df.loc[key_index,'Num_Congen_Anom'] = new_Outcome_df.isin(isr_OT).all(1).sum()
        print key + ' ' + str(Master_df.loc[key_index,'Num_Congen_Anom'])   

'''Populate Num_Disable Column '''
new_Outcome_df = pd.DataFrame() 
isr_OT = {}
for key in trade_and_isr:
    print key
    if trade_and_isr[key] == []:
        print key + ' has no ISRs'
    else:
        new_Outcome_df = Outcome_df.drop(['YEAR', 'QTR'] , axis=1)
        new_Outcome_df = new_Outcome_df.drop([new_Outcome_df.columns[0]], axis=1)
        ISR_list = trade_and_isr[key]
        ISR_list = map(int, ISR_list)
        isr_OT['ISR'] = ISR_list
        isr_OT['OUTC_COD'] = ['DS']
        key_index = int(Master_df[Master_df.Trade_Name == key].index)
        Master_df.loc[key_index,'Num_Disable'] = new_Outcome_df.isin(isr_OT).all(1).sum()
        print key + ' ' + str(Master_df.loc[key_index,'Num_Disable'])   
   
'''Populate Num_Deaths Column '''
new_Outcome_df = pd.DataFrame() 
isr_OT = {}
for key in trade_and_isr:
    print key
    if trade_and_isr[key] == []:
        print key + ' has no ISRs'
    else:
        new_Outcome_df = Outcome_df.drop(['YEAR', 'QTR'] , axis=1)
        new_Outcome_df = new_Outcome_df.drop([new_Outcome_df.columns[0]], axis=1)
        ISR_list = trade_and_isr[key]
        ISR_list = map(int, ISR_list)
        isr_OT['ISR'] = ISR_list
        isr_OT['OUTC_COD'] = ['DE']
        key_index = int(Master_df[Master_df.Trade_Name == key].index)
        Master_df.loc[key_index,'Num_Deaths'] = new_Outcome_df.isin(isr_OT).all(1).sum()
        print key + ' ' + str(Master_df.loc[key_index,'Num_Deaths'])       

'''Populate Num_Male Column '''
new_Demo_df = Demo_df.drop(['I_F_COD','AGE','AGE_COD','REPORTER_COUNTRY','YEAR', 'QTR'] , axis=1)
new_Demo_df = new_Demo_df.drop([new_Demo_df.columns[0]], axis=1) 
isr_DE = {}
for key in trade_and_isr:
    print key
    if trade_and_isr[key] == []:
        print key + ' has no ISRs'
    else:
        ISR_list = trade_and_isr[key]
        ISR_list = map(int, ISR_list)
        isr_DE['ISR'] = ISR_list
        isr_DE['GNDR_COD'] = ['M']
        key_index = int(Master_df[Master_df.Trade_Name == key].index)
        Master_df.loc[key_index,'Num_Male'] = new_Demo_df.isin(isr_DE).all(1).sum()
        print key + ' ' + str(Master_df.loc[key_index,'Num_Male'])       

'''Populate Num_Female Column '''
new_Demo_df = Demo_df.drop(['I_F_COD','AGE','AGE_COD','REPORTER_COUNTRY','YEAR', 'QTR'] , axis=1)
new_Demo_df = new_Demo_df.drop([new_Demo_df.columns[0]], axis=1) 
isr_DE = {}
for key in trade_and_isr:
    print key
    if trade_and_isr[key] == []:
        print key + ' has no ISRs'
    else:
        ISR_list = trade_and_isr[key]
        ISR_list = map(int, ISR_list)
        isr_DE['ISR'] = ISR_list
        isr_DE['GNDR_COD'] = ['F']
        key_index = int(Master_df[Master_df.Trade_Name == key].index)
        Master_df.loc[key_index,'Num_Female'] = new_Demo_df.isin(isr_DE).all(1).sum()
        print key + ' ' + str(Master_df.loc[key_index,'Num_Female'])       





'''
Creates a new column that divides a drugs total number of adverse events
by the number of years the drug has been on the market
'''  
Master_df['AE_Per_Year'] = Master_df.Num_Adv_Event / (2014 - Master_df.Approval_Year)
Master_df['Num_Serious'] = Master_df.Num_Other + Master_df.Num_Life_Threat + Master_df.Num_Hosp + Master_df.Num_Congen_Anom +  Master_df.Num_Disable + Master_df.Num_Deaths


'''
Converts all words in the 'Innovation_Column to uppercase and then numeral 0,1,2
'''
Master_df.Innovation_Cat = Master_df.Innovation_Cat.str.upper()
Master_df.Innovation_Cat = Master_df.Innovation_Cat.replace(to_replace=['ADDITION TO CLASS',
                                             'ADVANCE IN CLASS',
                                             'FIRST IN CLASS'], value=[0,1,2])



'''
Converts all NaN to Zero
'''

Master_df.Num_Serious= Master_df.Num_Serious.fillna(0)
Master_df.Num_Other = Master_df.Num_Other.fillna(0)
Master_df.Num_Life_Threat = Master_df.Num_Life_Threat.fillna(0)
Master_df.Num_Hosp = Master_df.Num_Hosp.fillna(0)
Master_df.Num_Congen_Anom = Master_df.Num_Congen_Anom.fillna(0)
Master_df.Num_Disable = Master_df.Num_Disable.fillna(0)
Master_df.Num_Deaths = Master_df.Num_Deaths.fillna(0)
Master_df.Num_Male = Master_df.Num_Male.fillna(0)
Master_df.Num_Female = Master_df.Num_Female.fillna(0)




'''Saves this all to a .csv'''
    
#Master_df.to_csv('C:\Users\jonbryan90\Desktop\MASTER5_NoNA')




                