# -*- coding: utf-8 -*-
"""
Created on Tue Apr 12 11:19:24 2016

@author: stephane
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

#%%
print df.shape
print "unique ids: {}".format(pd.value_counts(df.lc_id).shape)
print "unique member_ids: {}".format(pd.value_counts(df.member_id).shape)
#%%
print df[0:1]
print df.iloc[-1]

#%%
#%% Just save it as a new file
path = 'data/processed/LoanStats-combined.csv'
df.to_csv(path,index=False)




#%% beginning of split file... read in df to start
df = pd.read_csv(path)
# does loan_amnt always equal funded_amnt?
adiff=df.loan_amnt - df.funded_amnt
print pd.value_counts(adiff).shape
pd.value_counts(adiff).head()
#%%
''' 
Let's read the zillow data now
'''
zil=pd.read_csv('data/zillow/Zip_MedianRentalPrice_AllHomes.csv')
#%%
zil.shape
#need to compress the zipcodes, lc zipcode data is just first 3 digits
# first, just trim all but the first 3
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
    if (findex != 14) & (findex%25 == 0):
        shortx = zilc[['moin',ci]].dropna().moin.reshape(-1,1)
        shorty = zilc[['moin',ci]].dropna()[ci].reshape(-1,1)
        plt.plot(shortx,shorty,'-b',
                [shortx[0][0], shortx[-1][0]],
            [ coeflist[findex]*shortx[0][0] + interclist[findex],
             coeflist[findex] *shortx[-1][0] + interclist[findex]],'-r')
plt.title('sample fits')
plt.xticks(zilc.moin[::8],zilc.index[::8], rotation='vertical')
#plt.plot(shortx,shorty,'-b',
#        [shortx[0][0], shortx[-1][0]],
#    [ linreg.coef_[0][0]*shortx[0][0] + linreg.intercept_[0],
#     linreg.coef_[0][0] *shortx[-1][0] + linreg.intercept_[0]],'-r')
#%% now, create the list to add to the lc df
# df just needs 2 new columns, and the values are the coef & intercept

#minidf = df[['zip_code']]
df['lc_zip3'] = df.zip_code.apply(lambda z: str(z)[0:3])
df['zlens'] = df.lc_zip3.apply(len)
print df.zlens.unique() # verifies that all 3 digits
zipdict_coef = dict(zip(zilc.columns[0:-1],coeflist))
zipdict_interc = dict(zip(zilc.columns[0:-1],interclist))
df['zil_coef'] = df.lc_zip3.apply(
    lambda z:  zipdict_coef[z] if z in zipdict_coef else float('Nan'))
df['zil_interc'] = df.lc_zip3.apply(
    lambda z:  zipdict_interc[z] if z in zipdict_interc else float('Nan'))
#%%
# now save again, we finally have the zipcode data in there
    
    
#%%

# Here are all the columns, in this file at least:
'''
dfc=df.columns
print list(dfc)
['id', 'member_id', 'loan_amnt', 'funded_amnt', 'funded_amnt_inv',
 'term', 'int_rate', 'installment', 'grade', 'sub_grade',
 'emp_title', 'emp_length', 'home_ownership', 'annual_inc', 
 'verification_status', 'issue_d', 
 'loan_status', 
 'pymnt_plan', 'url', 'desc', 'purpose', 'title',
 'zip_code', 'addr_state', 'dti', 'delinq_2yrs', 'earliest_cr_line',
 'inq_last_6mths', 'mths_since_last_delinq', 'mths_since_last_record', 
 'open_acc', 'pub_rec', 'revol_bal', 'revol_util', 'total_acc',
 'initial_list_status', 'out_prncp', 'out_prncp_inv', 
 'total_pymnt', 'total_pymnt_inv', 'total_rec_prncp', 'total_rec_int', 'total_rec_late_fee',
 'recoveries', 'collection_recovery_fee', 'last_pymnt_d', 'last_pymnt_amnt', 'next_pymnt_d', 
 'last_credit_pull_d', 'collections_12_mths_ex_med', 'mths_since_last_major_derog', 
 'policy_code', 'application_type', 'annual_inc_joint', 'dti_joint', 
 'verification_status_joint',
 'acc_now_delinq', 'tot_coll_amt', 'tot_cur_bal',
 'open_acc_6m', 'open_il_6m', 'open_il_12m', 'open_il_24m', 'mths_since_rcnt_il', 
 'total_bal_il', 'il_util', 'open_rv_12m', 'open_rv_24m', 'max_bal_bc', 'all_util',
 'total_rev_hi_lim', 'inq_fi', 'total_cu_tl', 'inq_last_12m', 'acc_open_past_24mths', 
 'avg_cur_bal', 'bc_open_to_buy', 'bc_util', 
 'chargeoff_within_12_mths', 'delinq_amnt', 'mo_sin_old_il_acct', 'mo_sin_old_rev_tl_op', 
 'mo_sin_rcnt_rev_tl_op', 'mo_sin_rcnt_tl', 'mort_acc', 'mths_since_recent_bc',
 'mths_since_recent_bc_dlq', 'mths_since_recent_inq', 'mths_since_recent_revol_delinq', 
 'num_accts_ever_120_pd', 'num_actv_bc_tl', 'num_actv_rev_tl',
 'num_bc_sats', 'num_bc_tl', 'num_il_tl', 'num_op_rev_tl', 'num_rev_accts', 
 'num_rev_tl_bal_gt_0', 'num_sats', 'num_tl_120dpd_2m', 'num_tl_30dpd',
 'num_tl_90g_dpd_24m', 'num_tl_op_past_12m', 'pct_tl_nvr_dlq', 
 'percent_bc_gt_75', 'pub_rec_bankruptcies', 'tax_liens', 
 'tot_hi_cred_lim', 'total_bal_ex_mort', 'total_bc_limit', 'total_il_high_credit_limit'
 ]
'''
#%%
colset1 = \
['id', 'member_id', 'loan_amnt', 'funded_amnt', 'funded_amnt_inv',
 'term', 'int_rate', 'installment', 'grade', 'sub_grade',
'loan_status', 
 'out_prncp', 'out_prncp_inv',
 'total_pymnt', 'total_pymnt_inv', 'total_rec_prncp', 'total_rec_int', 'total_rec_late_fee',
 
 ]
featurecolset = \
 [
'emp_length',  'annual_inc', 'dti',
]
#%% automatically try to pull out categoricals
a = [ df[x].unique().shape[0] for x in df] # count unique values
categorical_cols = \
[
'term', 'grade', 'home_ownership', 'verification_status', 
'loan_status', 'pymnt_plan', 'initial_list_status', 
'policy_code', 'application_type', 
'verification_status_joint', 'acc_now_delinq',
 'num_tl_120dpd_2m', 'num_tl_30dpd'
 ]


df=df[colset1]
print df.shape
print pd.value_counts(df.loan_status)
print pd.value_counts(df.grade)
#%%
df2=df[(df.loan_status == 'Fully Paid') | (df.loan_status == 'Charged Off') | 
    (df.loan_status == 'Current')  ].copy()
df2['loan_status_num'] = df2.loan_status.map(
    {'Charged Off':0, 'Fully Paid':1, 'Current':1})
df2['grade_num'] = df2.grade.map({'A':0, 'B':1, 'C':2, 'D':3, 'E':4, 'F':5, 'G':6})
df2.sort_values(by='grade_num',inplace=True)
grouped=df2.groupby('grade')
probs=grouped.loan_status_num.sum()/grouped.loan_status_num.count()
gradenames=sorted(df.grade.unique())
gradenums = np.arange(0,7)
print probs
#%%
# fit a logistic regression model and store the class predictions
from sklearn.linear_model import LogisticRegression
logreg = LogisticRegression()
feature_cols = ['grade_num']
X = df2[feature_cols]
y = df2.loan_status_num
logreg.fit(X, y)
df2['loan_status_pred_num'] = logreg.predict(X)

#%%
import matplotlib.pyplot as plt
#%%
plt.scatter(df2.grade_num,df2.loan_status_num,label='loan status')
plt.plot(df2.grade_num,df2.loan_status_pred_num,color='red')
plt.setp(plt.gca(), xticklabels=gradenames, xticks = gradenums)
plt.setp(plt.gca(), yticklabels=np.arange(0,1.2,.2), yticks = np.arange(0,1.2,.2))
#, yticks=(4, 8, 12), yticklabels=[], xticks=(0, 10, 20))
#%%
df2['loan_status_pred_prob']=logreg.predict_proba(X)[:,1]
plt.scatter(df2.grade_num,df2.loan_status_num)
plt.plot(df2.grade_num,df2.loan_status_pred_prob,color='red')
plt.plot(probs)

#%%
#okay so I've been using their predictions to predict the prob of default,
# but it turns out their predictions are pretty accurate
#%%
#plt.bar([x-.4 for x in range(0,7)],df2.groupby('grade').loan_status_num.sum())
grouped=df2.groupby('grade')

fig,ax = plt.subplots()
width=.4
xlocs=np.arange(0,7)
ax.bar(xlocs-width,grouped.loan_status_num.sum(),width,color='k')
ax.set_xticks(xlocs)
ax.set_xticklabels(sorted(df.grade.unique()))

ax.bar(
    xlocs,grouped.loan_status_num.apply(lambda item: (item == 0).sum()),width,
    color='r')
#ax.bar([x-.4 for x in range(0,7)],df2.groupby('grade').loan_status_num.sum())
#%%
from sklearn.cross_validation import train_test_split
from sklearn import metrics
X_train, X_test, y_train, y_test = train_test_split(X, y,random_state=22)
logreg2 = LogisticRegression()
logreg2.fit(X_train,y_train)
y_pred_class = logreg2.predict(X_test)
print metrics.accuracy_score(y_test, y_pred_class)
print metrics.accuracy_score(y_test,[1]*len(y_test))

#%%

