#!/usr/bin/env python
# coding: utf-8

# In[261]:


import pandas as pd
import numpy as np


# 1. merging 10 US vital data sets and cleaning for final data set

# In[262]:


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


# In[263]:


# merged 10 data sets

df=[df1,df2,df3, df4, df5, df6, df7, df8, df9, df10]
df_new=pd.concat(df)


# In[264]:


df_new.head()


# In[265]:


#split state and county name

temp=df_new['County'].str.split(",",expand=True)
df_new['County']=temp[0]
df_new['State']=temp[1]


# In[266]:


df_new['Drug/Alcohol Induced Cause'].unique()


# In[267]:


#select 'Drug poisonings (overdose) Unintentional (X40-X44)', 'Drug poisonings (overdose) Undetermined (Y10-Y14)', 'Drug poisonings (overdose) Suicide (X60-X64)'
df_death=df_new.loc[df_new['Drug/Alcohol Induced Cause'].isin(['Drug poisonings (overdose) Unintentional (X40-X44)', 'Drug poisonings (overdose) Undetermined (Y10-Y14)', 'Drug poisonings (overdose) Suicide (X60-X64)'])]


# In[268]:


#reorder col names
columnsTitles = ['Notes', 'State', 'County', 'County Code', 'Year', 'Year Code',
       'Drug/Alcohol Induced Cause', 'Drug/Alcohol Induced Cause Code',
       'Deaths']

df_death = df_death.reindex(columns=columnsTitles).copy()


# In[269]:


#drop useless cols

df_death=df_death.drop(["Notes", "Year Code", "Drug/Alcohol Induced Cause Code"],axis=1 )


# In[270]:


df_death.head()


# In[271]:


#cleaning missing value

df_death['Deaths']=df_death['Deaths'].astype(str)
df_death= df_death[~df_death['Deaths'].str.contains("Missing")]


# In[272]:


#change data type

df_death['County Code']=df_death['County Code'].astype(int)
df_death['Year']=df_death['Year'].astype(int)


# In[273]:


df_death['Deaths']=pd.to_numeric(df_death['Deaths'], downcast='integer')


# In[274]:


df_death.head()


# In[ ]:





# 2. population data cleaning

# In[275]:


df2= pd.read_csv("pop_counties_20062012.csv")


# In[276]:


df2.head()


# In[277]:


#split state and county name, and cleaning

temp=df2['NAME'].str.split(",",expand=True)
df2['County']=temp[0]
df2['State']=temp[1]


# In[278]:


df2 =df2.drop(["BUYER_COUNTY", "STATE", "COUNTY", "NAME", "variable", 'State', 'county_name'],axis=1 )


# In[279]:


df2.rename(columns = {'year':'Year', 'countyfips':'County Code', 'BUYER_STATE':'State' }, inplace = True)


# In[280]:


df2=df2.dropna(axis=0, how='any')


# In[ ]:





# 3. Final data set

# In[281]:


#merging df_death and df2 to get final data set

df_final=pd.merge(df_death, df2, how='inner', on=['County Code', 'Year'])


# In[282]:


df_final['population']=df_final['population'].astype(int)


# In[283]:


df_final=df_final.drop(["State_y", "County_y"],axis=1 )


# In[284]:


df_final.rename(columns = {'State_x':'State', 'County_x':'County'}, inplace = True)


# In[285]:


df_final.head()


# In[286]:


#Death rate Calculation

df_final['Death Rate']=df_final['Deaths']/df_final['population']


# In[287]:


df_final.head()


# In[ ]:





# In[ ]:




