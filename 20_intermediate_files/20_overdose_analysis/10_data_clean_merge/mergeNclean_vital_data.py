#!/usr/bin/env python
# coding: utf-8

# In[322]:


import pandas as pd
import numpy as np
from plotnine import *


# 1. merging 10 US vital data sets and cleaning

# In[323]:


df1 = pd.read_csv("Underlying Cause of Death, 2006.txt",  delimiter="\t")
df2 = pd.read_csv("Underlying Cause of Death, 2007.txt",  delimiter="\t")
df3 = pd.read_csv("Underlying Cause of Death, 2008.txt",  delimiter="\t")
df4 = pd.read_csv("Underlying Cause of Death, 2009.txt",  delimiter="\t")
df5 = pd.read_csv("Underlying Cause of Death, 2010.txt",  delimiter="\t")
df6 = pd.read_csv("Underlying Cause of Death, 2011.txt",  delimiter="\t")
df7 = pd.read_csv("Underlying Cause of Death, 2012.txt",  delimiter="\t")
df8 = pd.read_csv("Underlying Cause of Death, 2013.txt",  delimiter="\t")
df9 = pd.read_csv("Underlying Cause of Death, 2014.txt",  delimiter="\t")
df10 = pd.read_csv("Underlying Cause of Death, 2015.txt",  delimiter="\t")


# In[324]:


# merging 10 data sets

df=[df1,df2,df3, df4, df5, df6, df7, df8, df9, df10]
df_new=pd.concat(df)


# In[325]:


df_new.head()


# In[326]:


#split state and county name

temp=df_new['County'].str.split(",",expand=True)
df_new['County']=temp[0]
df_new['State']=temp[1]


# In[327]:


# check 'Drug/Alcohol Induced Cause'
df_new['Drug/Alcohol Induced Cause'].unique()


# In[328]:


#select 'Drug poisonings (overdose) Unintentional (X40-X44)', 'Drug poisonings (overdose) Undetermined (Y10-Y14)', 'Drug poisonings (overdose) Suicide (X60-X64)'
df_death=df_new.loc[df_new['Drug/Alcohol Induced Cause'].isin(['Drug poisonings (overdose) Unintentional (X40-X44)', 'Drug poisonings (overdose) Undetermined (Y10-Y14)', 'Drug poisonings (overdose) Suicide (X60-X64)'])]


# In[329]:


#reorder col names
columnsTitles = ['Notes', 'State', 'County', 'County Code', 'Year', 'Year Code',
       'Drug/Alcohol Induced Cause', 'Drug/Alcohol Induced Cause Code',
       'Deaths']

df_death = df_death.reindex(columns=columnsTitles).copy()


# In[330]:


#drop useless cols

df_death=df_death.drop(["Notes", "Year Code", "Drug/Alcohol Induced Cause Code"],axis=1 )


# In[331]:


# remove white space in state name
df_death['State']=df_death['State'].str.replace(" ","")


# In[332]:


df_death.head()


# In[333]:


#cleaning missing value in 'Deaths'
df_death['State']=df_death['State'].astype(str)
df_death['County']=df_death['County'].astype(str)
df_death['Deaths']=df_death['Deaths'].astype(str)
df_death= df_death[~df_death['Deaths'].str.contains("Missing")]


# In[334]:


#change data type

df_death['County Code']=df_death['County Code'].astype(int)
df_death['Year']=df_death['Year'].astype(int)
df_death['Deaths']=pd.to_numeric(df_death['Deaths'], downcast='integer')


# In[335]:


df_death.head()
