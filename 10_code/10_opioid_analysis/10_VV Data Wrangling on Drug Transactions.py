#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
from dask import dataframe as dd


# In[2]:


#I read the data. When rerunning it, include DRUG_NAME in the col names. I excluded it by mistake. 
#\t because the file is a tab-separated-file.
df_cols = pd.read_csv('D://Data//arcos_all.tsv//arcos_all.tsv', delimiter='\t', usecols=['BUYER_STATE','BUYER_COUNTY','TRANSACTION_DATE','CALC_BASE_WT_IN_GM','MME_Conversion_Factor','DRUG_NAME'], encoding='utf-8')


# In[3]:


#Let's now strip the original dataframe to just contain Oxycodone and Hydrocodone.
chunksize = 100000
chunksize1 = 0
chunksize2 = 100000
l = []#Empty list to get indices of rows where drug is Oxycodone or Hydrocodone
for i in range (df_cols.shape[0]%chunksize):
    df = df_cols.iloc[chunksize1:chunksize2]
    l.append(df.index[(df['DRUG_NAME']=='OXYCODONE') | (df['DRUG_NAME']=='HYDROCODONE')])
    chunksize1 = chunksize1 + 100000
    chunksize2 = chunksize2 + 100000
    
#index_drugs = df_cols.index[(df_cols['DRUG_NAME']=='OXYCODONE') | (df_cols['DRUG_NAME']=='HYDROCODONE')]

#c[c['DRUG_NAME']=='OXYCODONE']
#df_cols_drug_f = df_cols[(df_cols['DRUG_NAME']=='OXYCODONE') | (df_cols['DRUG_NAME']=='HYDROCODONE')]
#df_cols.to_pickle('D://Data//arcos_all.tsv//initialise.pkl')


# In[4]:


#How many rows do we have now?
s = 0
for i in range (len(l)):
    s = s + len(l[i])
    
s
#About 133 M. This is 75% or original dataframe. This matches with the prompt.


# In[7]:


#Let's now subset for a specific state.

def sub_state_index(state):
    
    chunksize = 100000
    chunksize1 = 0
    chunksize2 = 100000
    m = []#Empty list to get indices of rows of a particular state
    df_cols_state = pd.DataFrame()
    for i in range (df_cols.shape[0]%chunksize):
        df_1 = df_cols.iloc[chunksize1:chunksize2]
        m.append(df_1.index[((df_1['BUYER_STATE']==state) & ((df_1['DRUG_NAME']=='OXYCODONE') | (df_1['DRUG_NAME']=='HYDROCODONE')))])
        chunksize1 = chunksize1 + 100000
        chunksize2 = chunksize2 + 100000
    return (m)


# In[8]:


#Using the index function (sub_state_index), we can get a list of dataframes containing the rows for that particular state.
#We then need to pf.concat the list to get a single dataframe for that state.
def sub_state(state_index):
    chunksize = 100000
    chunksize1 = 0
    chunksize2 = 100000
    n = []#Empty list to store rows...
    for i in range (len(state_index)):
        df_2 = df_cols.iloc[chunksize1:chunksize2]
        n.append(df_2[df_2.index.isin(state_index[i])])
        chunksize1 = chunksize1 + 100000
        chunksize2 = chunksize2 + 100000
    return(n)


# In[ ]:


#I test if my functions are working for the state of Florida
#Creating a list of indices for the state of Florida
fl_index = sub_state_index('FL') 


# In[ ]:


#Creating a list of dataframes for the state of Florida
fl_state = sub_state(fl_index)


# In[ ]:


#Single dataframe for all of florida. We need the above 3 different steps to minimise computational time
df_fl = pd.concat(fl_state)
#All the functions are working!


# In[40]:


#In the next step I will create a separate dataframe for each state. All the dataframes will be pickled for ease of access next time.
#Also AZ seems to crash the thing.
states =  ["AL", "AK",  "AR", "CA", "CO", "CT", "DC", "DE", "FL", "GA", 
          "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD", 
          "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ", 
          "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC", 
          "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"]

for state in states:
         pd.to_pickle((pd.concat(sub_state(sub_state_index(state)))),'D://Data//arcos_all.tsv//'+str(state)+'.pkl' )
        
    





