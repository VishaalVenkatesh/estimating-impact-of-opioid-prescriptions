#!/usr/bin/env python
# coding: utf-8

# In[322]:


import pandas as pd
import numpy as np
from plotnine import *




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
