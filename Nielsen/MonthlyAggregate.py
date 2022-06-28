# -*- coding: utf-8 -*-
"""
Created on Mon Jun 13 09:44:06 2022

@author: Luke Morris

Monthly Nielsen Aggregate
This file combines the necessary Nielsen data pulls with the master classification file to produce our monthly syndicated resources.

Monthly Nielsen Files:

- Mass, DECA CONSUS Retail Trade Areas
- Total xAOC, Food, Drug
- Drug, Dollar, Club Retail Trade Areas,
- Food Retail Trade Areas N-Z
- Food Retail Trade Areas A-E
- Syndicated Food Markets 1.0
- Syndicated Food Markets 2.0
- Total Nielsen Market
- Food Retail Trade Areas F-M
- Lowes Retail Trade Area
Combine the above with the Master Classification file, Trade Area Mapping, and Walmart Departments
"""

import pandas as pd
import numpy as np
from MNF.py import upcCoder

# Rows are 0 indexed, start at 4

mass = pd.read_excel('LATEST_DATA\\Mass_DECA_CONSUS_Retail_Trade_Areas.xlsx', 
                     sheet_name = 'Report1', header=4)
totalxAOC = pd.read_excel('LATEST_DATA\\Total_xAOC_Food_Drug.xlsx', 
                          sheet_name = 'Report1', header=4)
drug = pd.read_excel('LATEST_DATA\\Drug_Dollar_Club_Retail_Trade_Areas.xlsx', 
                     sheet_name = 'Report1', header=4)
foodAE = pd.read_excel('LATEST_DATA\\Food_Retail_Trade_Areas_A-E.xlsx', 
                       sheet_name = 'Report1', header=4)
foodFM = pd.read_excel('LATEST_DATA\\Food_Retail_Trade_Areas_F-M.xlsx', 
                       sheet_name = 'Report1', header=4)
foodNZ = pd.read_excel('LATEST_DATA\\Food_Retail_Trade_Areas_N-Z.xlsx', 
                       sheet_name = 'Report1', header=4)
sync1 = pd.read_excel('LATEST_DATA\\Syndicated_Food_Markets_1.0.xlsx', 
                      sheet_name = 'Report1', header=4)
sync2 = pd.read_excel('LATEST_DATA\\Syndicated_Food_Markets_2.0.xlsx', 
                      sheet_name = 'Report1', header=4)
totalN = pd.read_excel('LATEST_DATA\\Total_Nielsen_Market.xlsx', 
                       sheet_name = 'Report1', header=4)
lowes = pd.read_excel('LATEST_DATA\\Lowes_Retail_Trade_Area.xlsx', 
                      sheet_name = 'Report1', header=4)

mclass = pd.read_excel('H&G_AOD_Master_Item_Classification_File.xlsx')

# Update columns 

cols = ['Trade Area', 'UPC', 'SHORT PRODUCT DESCRIPTION', 'Current Scan Periods', '$', '$ YA',
       'Units', 'Units YA', '%ACV', '%ACV YA', '$ / TDP', '$ / TDP YA',
       'Disp w/o Feat $', 'Disp w/o Feat $ YA', 'Feat w/o Disp $',
       'Feat w/o Disp $ YA', 'Price Decr $', 'Price Decr $ YA',
       'Feat & Disp $', 'Feat & Disp $ YA']

synclist = [mass, totalxAOC, drug, foodAE, foodFM, foodNZ, sync1, sync2, totalN, lowes]

for i in synclist:
    i.columns = cols

# Loop creates new dataframe to append, otherwise appends next iteration

p = 1
#df = synclist[0]

for i in synclist:
    if p == 1:
        #pass
        df = i
        p = p + 1
    else:
        df = df.append(i)
        p = p + 1
        
# Fill NAs which will be in value columns

df.fillna(0, inplace=True)

# Drop duplicates in Master Class to avoid errors

mclass = mclass.drop_duplicates(subset=['UPC'])

# Merge to final dataset on UPC

working_df = df.merge(mclass, how='left', on='UPC')

"""
Merge with Market Characteristic Mapping and Walmart List
"""

mark_char = pd.read_csv('Market_Characteristics.csv')
wmt = pd.read_excel('WMT Master Dept Classifications AOD.xlsx', sheet_name='Walmart')

working_df = mark_char.merge(working_df, how='right', on='Trade Area')

walmart = working_df[working_df['Trade Area'] == 'Walmart Total US TA']

walmart = walmart.merge(wmt, how='left', on='UPC')

# Drop Walmart rows and then append the new Walmart

# Set a blank column then delete Walmart rows
working_df['WMT Dept'] = ''
working_df = working_df[working_df['Trade Area'] != 'Walmart Total US TA']

# Append Walmart rows
finaldf = working_df.append(walmart)


"""
Add Leading 0's for UPC
"""
"""
def upcCoder(upc_list):


    Parameters
    ----------
    df : TYPE, optional
        DESCRIPTION. The default is df.

    Returns
    -------
    df : TYPE
        DESCRIPTION.


    upc_list = upc_list.astype(str)
    UPC12 = []

    for upc in upc_list:
        UPC12.append(upc.zfill(12))
    
    return UPC12
"""

finaldf['UPC'] = upcCoder(finaldf['UPC'])

"""
Previous code
finaldf['UPC'] = finaldf['UPC'].astype(str)
UPC0 = finaldf['UPC']
UPC12 = []

for upc in UPC0:
    UPC12.append(upc.zfill(12))

finaldf['UPC'] = UPC12
"""

"""
Drop Duplicates just in case and then export.
This step might not be needed. Trying to evaluate.
Final Export
"""
finaldf.drop_duplicates(subset=['Trade Area', 'UPC', 'SHORT PRODUCT DESCRIPTION', 
                                'Current Scan Periods',], inplace = True)

finaldf.to_excel('NEW_NIELSEN.xlsx', index=False)