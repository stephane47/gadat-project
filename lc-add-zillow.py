# -*- coding: utf-8 -*-
"""
Created on Wed May 18 13:15:44 2016

@author: stephane
"""

#%%
import numpy as np
import pandas as pd
''' 
Let's read the zillow data now
'''
zil=pd.read_csv('data/zillow/Zip_MedianRentalPrice_AllHomes.csv')
#%%
"""
need to compress the zipcodes, lc zipcode data is just first 3 digits
   first, just trim all but the first 3
"""
zil.shape
zil['zip3'] = zil.RegionName.apply(lambda z: str(z)[0:3])
print 'before compressing, zil shape'
print zil.shape
print "{} unique zip3s".format(zil.zip3.unique().shape[0])
print "{} total though".format(zil.zip3.value_counts().sum())

#%% This will combine all zips into the zip3, and reset the index to be the zip3
zilc = zil[zil.columns[6:]].groupby(by='zip3').mean()

print "dropped some columns, strings? " + str(set(zil.columns)-set(zilc.columns))

print zilc.shape
# get rid of 2 unnecessary columns
zilc = zilc.T
zilc['moin']=range(0,zilc.shape[0])
print zilc[zilc.columns[0:5]].head(2)
print zilc[zilc.columns[0:5]].tail(2)

#print zilc[list(zilc.columns[1:3]) + list(zilc.columns[-15:-1])].shape
# okay now zilc has cols for each zip3, indexed by zip3
zilc['moin']=range(0,zilc.shape[0])

#%%
#ztest = zil[list(zil.columns[1:3]) + list(zil.columns[-15:-1]) + ['zip3'] ]
#
#ztest2 = ztest.groupby(by='zip3').mean().T
#ztest2.shape


#%%
# finally do some linreg!?
from sklearn.linear_model import LinearRegression

# i want to makea list of coefs & intercepts for each zip3 (column)
interclist =  []
coeflist = []
for ci in zilc.columns[0:-1]:   
    linreg = LinearRegression()
    linreg.fit(
        zilc[['moin',ci]].dropna().moin.reshape(-1,1),
        zilc[['moin',ci]].dropna()[ci].reshape(-1,1))
    interclist.append(float(linreg.intercept_))
    coeflist.append(float(linreg.coef_))
    
#    linreg.fit(
#        zilc[['moin','103']].dropna().moin.reshape(-1,1),
#        zilc[['moin','103']].dropna()['103'].reshape(-1,1))

#print linreg.coef_ , linreg.intercept_

#%%
#plot the mofos?
import matplotlib.pyplot as plt
for findex, ci in enumerate(zilc.columns[0:-1]): # 119 is crazy
#    ci = zilc.columns[findex]
    if True:
        shortx = zilc[['moin',ci]].dropna().moin.reshape(-1,1)
        shorty = zilc[['moin',ci]].dropna()[ci].reshape(-1,1)
        plt.plot(shortx,shorty,'-b',
                [shortx[0][0], shortx[-1][0]],
            [ coeflist[findex]*shortx[0][0] + interclist[findex],
             coeflist[findex] *shortx[-1][0] + interclist[findex]],'-r')
plt.title('sample fits')
plt.xticks(zilc.moin[::8],zilc.index[::8], rotation='vertical')

#%%
for findex, ci in enumerate(zilc.columns[0:-1]): # 119 is crazy
#    ci = zilc.columns[findex]
    if (findex != 14) & (findex%25 == 0):
        shortx = zilc[['moin',ci]].dropna().moin.reshape(-1,1)
        shorty = zilc[['moin',ci]].dropna()[ci].reshape(-1,1)
        plt.plot(shortx,shorty,'-b',
                [shortx[0][0], shortx[-1][0]],
            [ coeflist[findex]*shortx[0][0] + interclist[findex],
             coeflist[findex] *shortx[-1][0] + interclist[findex]],'-r')
plt.title('sample fits')
plt.xticks(zilc.moin[::8],zilc.index[::8], rotation='vertical')

#%%
for findex, ci in enumerate(zilc.columns[0:-1]): # 119 is crazy
#    ci = zilc.columns[findex]
    if (findex != 14) & (findex%20 == 0) & (zilc[ci].max()<2000):
        shortx = zilc[['moin',ci]].dropna().moin.reshape(-1,1)
        shorty = zilc[['moin',ci]].dropna()[ci].reshape(-1,1)
        plt.plot(shortx,shorty,'-b',
                [shortx[0][0], shortx[-1][0]],
            [ coeflist[findex]*shortx[0][0] + interclist[findex],
             coeflist[findex] *shortx[-1][0] + interclist[findex]],'-r')
plt.title('sample fits')
plt.xticks(zilc.moin[::8],zilc.index[::8], rotation='vertical')

#%% now, create the list to add to the lc df
# df just needs 2 new columns, and the values are the coef & intercept
path = 'data/processed/LoanStats-combined.csv'
df = pd.read_csv(path)
print df.shape
#%%

#minidf = df[['zip_code']]
df['lc_zip3'] = df.zip_code.apply(lambda z: str(z)[0:3])
#df['zlens'] = df.lc_zip3.apply(len)
#print df.zlens.unique() # verifies that all 3 digits
zipdict_coef = dict(zip(zilc.columns[0:-1],coeflist))
zipdict_interc = dict(zip(zilc.columns[0:-1],interclist))
df['zil_coef'] = df.lc_zip3.apply(
    lambda z:  zipdict_coef[z] if z in zipdict_coef else float('Nan'))
df['zil_interc'] = df.lc_zip3.apply(
    lambda z:  zipdict_interc[z] if z in zipdict_interc else float('Nan'))
#%%
# now save again, we finally have the zipcode data in there
path = 'data/processed/LoanStats-combined-z.csv'
df.to_csv(path,index=False)
    
#%%