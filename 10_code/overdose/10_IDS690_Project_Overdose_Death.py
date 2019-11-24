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


# 2. population data cleaning

# In[336]:


df2= pd.read_excel("PopulationReport.xlsx")


# In[337]:


df2.head()


# In[338]:


df2.rename(columns = {'County Name':'County'}, inplace = True)
df2['State']=df2['State'].astype(str)
df2['County']=df2['County'].astype(str)
df2['pop2010']=df2['pop2010'].astype(int)


# 3. Final data set

# In[339]:


#merging df_death and df2 to get final data set

df_final=pd.merge(df_death, df2, how='inner', on=['State', 'County'])


# In[340]:


df_final.head()


# In[343]:


#Death rate Calculation by county

df_final['Death Rate']=df_final['Deaths']/df_final['pop2010']


# In[344]:


#df_final[(df_final['State']=='AK') & (df_final['Year']==2009)]


# In[345]:


# new table with Total Death group by State and Year
df_death_tot=df_final.groupby(["State","Year"]).Deaths.sum().reset_index()


# In[346]:


# new table with Total Population group by State and Year
df_pop_tot=df_final.groupby(["State","Year"]).pop2010.sum().reset_index()


# In[347]:


# merging two new tables
df_final_2=pd.merge(df_death_tot, df_pop_tot, how='inner', on=['State', 'Year'])


# In[348]:


df_final_2.head()


# In[349]:


# add Death Rate by State
df_final_2['Death Rate']=df_final_2['Deaths']/df_final_2['pop2010']


# In[350]:


df_final_2.head()


# In[ ]:





# In[351]:


# select FL and four adjacent States
df_sel1=df_final_2[(df_final_2['State']=='FL') | (df_final_2['State']=='SC') | (df_final_2['State']=='AL') |(df_final_2['State']=='GA') | (df_final_2['State']=='NC') ]


# In[352]:


df_sel1.head()


# In[353]:


fig=(ggplot(aes(x='Year', y='Death Rate', group = 'State', color = 'State') , data = df_sel1) + geom_smooth()  + geom_vline(xintercept=2010, linetype = "dotted") + xlim(2008, 2014))
fig


# In[354]:


# select WA and four adjacent States
df_sel2=df_final_2[(df_final_2['State']=='WA') | (df_final_2['State']=='ID') | (df_final_2['State']=='CA') |(df_final_2['State']=='MT') | (df_final_2['State']=='NV') ]


# In[355]:


fig=(ggplot(aes(x='Year', y='Death Rate', group = 'State', color = 'State') , data = df_sel2) + geom_smooth()  + geom_vline(xintercept=2011, linetype = "dotted") + xlim(2009, 2015))
fig


# In[357]:


# select TX and four adjacent States
df_sel3=df_final_2[(df_final_2['State']=='TX') | (df_final_2['State']=='LA') | (df_final_2['State']=='OK') |(df_final_2['State']=='NM') | (df_final_2['State']=='AK') ]


# In[358]:


fig=(ggplot(aes(x='Year', y='Death Rate', group = 'State', color = 'State') , data = df_sel3) + geom_smooth()  + geom_vline(xintercept=2007, linetype = "dotted") + xlim(2006, 2011))
fig


# In[ ]:





# In[320]:


#test=df_final.groupby("County")
#test.get_group("Baldwin County")


# In[ ]:




