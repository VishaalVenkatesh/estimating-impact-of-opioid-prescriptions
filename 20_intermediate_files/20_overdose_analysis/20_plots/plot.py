#!/usr/bin/env python
# coding: utf-8

# In[322]:


import pandas as pd
import numpy as np
from plotnine import *




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
