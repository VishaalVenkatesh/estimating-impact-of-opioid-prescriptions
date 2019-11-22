#!/usr/bin/env python
# coding: utf-8

# In[322]:


import pandas as pd
import numpy as np
from plotnine import *




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
