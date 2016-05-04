# -*- coding: utf-8 -*-
"""
Created on Tue Apr 12 11:19:24 2016

@author: stephane

Combining Lending Club data files into a single file
"""

#%%
import numpy as np
import pandas as pd
#%%
""" 
file LoanStats3a.csv

Complete loan data for 2007-2011
1st step - read in a sample of the data
1st file contains oldest data, and appears to have 2 sections

top section:
1st line is misc text
2nd line is header row
39788 is last row of table

bottom section:
lines 39789-39791 are blank/text
line 39792 starts row data (same headers as top)
line 42540 last row of bottom section

files LoanStats3b.csv, LoanStats3c.csv, LoanStats3d.csv

Loan data for 2012-2016 Q1
all files have:
1st line misc text
2nd line header row
bottom 2 lines misc text

"""
path = 'data/lc/'
url = path + 'LoanStats3a.csv'
df1 = pd.read_csv(url,skiprows=[0, 39788,39789,39790, 42540, 42541, 42542, 42543])
print df1.shape
print df1.id.value_counts().shape
df2 = pd.read_csv('data/lc/LoanStats3b.csv',skiprows=1,skipfooter=2)
print df2.shape
print df2.id.value_counts().shape
df3 = pd.read_csv('data/lc/LoanStats3c.csv',skiprows=1,skipfooter=2)
print df3.shape
print df3.id.value_counts().shape
df4 = pd.read_csv('data/lc/LoanStats3d.csv',skiprows=1,skipfooter=2)
print df4.shape
print df4.id.value_counts().shape
#%%
# Check that all the columns are the same across all 4 files
checkcols=pd.DataFrame([df1.columns,df2.columns, df3.columns, df4.columns])
a = [checkcols[x].value_counts().values[0] for x in checkcols]
if (len(set(a)) == 1) & (set(a).pop() == 4):
    print "success"
#%%
df = pd.concat([df1, df2, df3, df4])
df.rename(columns={'id': 'lc_id'},inplace=True)
print df.shape
#%% Just save it as a new file
path = 'data/processed/LoanStats-combined.csv'
df.to_csv(path,index=False)
