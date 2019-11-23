#!/usr/bin/env python
# coding: utf-8

# In[81]:


import pandas as pd
import numpy as np

from patsy import dmatrices

from plotnine import *

import statsmodels.api as sm
import statsmodels.formula.api as smf

import matplotlib
import matplotlib.pyplot as plt


# 1. merging 10 US vital data sets and cleaning

# In[45]:


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


# In[46]:


# merging 10 data sets

df=[df1,df2,df3, df4, df5, df6, df7, df8, df9, df10]
df_new=pd.concat(df)


# In[47]:


df_new.head()


# In[48]:


#split state and county name

temp=df_new['County'].str.split(",",expand=True)
df_new['County']=temp[0]
df_new['State']=temp[1]


# In[49]:


# check 'Drug/Alcohol Induced Cause'
df_new['Drug/Alcohol Induced Cause'].unique()


# In[50]:


#select 'Drug poisonings (overdose) Unintentional (X40-X44)', 'Drug poisonings (overdose) Undetermined (Y10-Y14)', 'Drug poisonings (overdose) Suicide (X60-X64)'
df_death=df_new.loc[df_new['Drug/Alcohol Induced Cause'].isin(['Drug poisonings (overdose) Unintentional (X40-X44)', 'Drug poisonings (overdose) Undetermined (Y10-Y14)', 'Drug poisonings (overdose) Suicide (X60-X64)'])]


# In[51]:


#reorder col names
columnsTitles = ['Notes', 'State', 'County', 'County Code', 'Year', 'Year Code',
       'Drug/Alcohol Induced Cause', 'Drug/Alcohol Induced Cause Code',
       'Deaths']

df_death = df_death.reindex(columns=columnsTitles).copy()


# In[52]:


#drop useless cols

df_death=df_death.drop(["Notes", "Year Code", "Drug/Alcohol Induced Cause Code"],axis=1 )


# In[53]:


# remove white space in state name
df_death['State']=df_death['State'].str.replace(" ","")


# In[54]:


df_death.head()


# In[55]:


#cleaning missing value in 'Deaths'
df_death['State']=df_death['State'].astype(str)
df_death['County']=df_death['County'].astype(str)
df_death['Deaths']=df_death['Deaths'].astype(str)
df_death= df_death[~df_death['Deaths'].str.contains("Missing")]


# In[56]:


#change data type

df_death['County Code']=df_death['County Code'].astype(int)
df_death['Year']=df_death['Year'].astype(int)
df_death['Deaths']=pd.to_numeric(df_death['Deaths'], downcast='integer')


# In[57]:


df_death.head()


# 2. population data cleaning

# In[58]:


df2= pd.read_excel("PopulationReport.xlsx")


# In[59]:


df2.head()


# In[60]:


df2.rename(columns = {'County Name':'County'}, inplace = True)
df2['State']=df2['State'].astype(str)
df2['County']=df2['County'].astype(str)
df2['pop2010']=df2['pop2010'].astype(int)


# 3. Final data set

# In[61]:


#merging df_death and df2 to get final data set

df_final=pd.merge(df_death, df2, how='inner', on=['State', 'County'])


# In[ ]:





# In[62]:


#Death rate Calculation by county

df_final['Death_Rate']=df_final['Deaths']/df_final['pop2010']

df_final['Policy_State']=np.where((df_final['State']=='WA') | (df_final['State']=='FL') | (df_final['State']=='TX'),1,0)


# In[63]:


df_final.head()


# In[64]:


df_final_FL=df_final[(df_final['State']!='TX') | (df_final['State']=='WA') ]
df_final_FL['Post']=np.where(df_final_FL['Year']<2010,0,1)
df_final_FL['Year_C']=df_final_FL['Year']-2010


# In[65]:


df_final_FL


# In[66]:


df_final_TX=df_final[(df_final['State']!='FL') | (df_final['State']=='WA') ]
df_final_TX['Post']=np.where(df_final_TX['Year']<2007,0,1)
df_final_TX['Year_C']=df_final_TX['Year']-2007


# In[67]:


df_final_WA=df_final[(df_final['State']!='TX') | (df_final['State']=='FL') ]
df_final_WA['Post']=np.where(df_final_WA['Year']<2011,0,1)
df_final_WA['Year_C']=df_final_WA['Year']-2011


# In[68]:


df_FL=df_final[(df_final['State']=='FL')]


# In[90]:


fig_FL=(ggplot(aes(x='Year', y='Death_Rate', group = 'State', color = 'State') , data = df_FL) +
        geom_point() +geom_smooth(method='lm', data=df_FL[df_FL['Year']<2010], color='blue') +
        geom_smooth(method='lm', data=df_FL[df_FL['Year']>=2010], color='red') + geom_vline(xintercept=2010, linetype = "dotted") + 
        xlim(2006, 2014)+
        labs(title="Pre-Post in FL")
       )
fig_FL.save("prepost_FL.pdf")
fig_FL


# In[70]:


df_TX=df_final[(df_final['State']=='TX')]


# In[92]:


fig_TX=(ggplot(aes(x='Year', y='Death_Rate', group = 'State', color = 'State') , data = df_TX) +geom_point() +geom_smooth(method='lm', data=df_TX[df_TX['Year']<2007], color='blue') +
        geom_smooth(method='lm', data=df_TX[df_TX['Year']>=2007], color='red') + geom_vline(xintercept=2007, linetype = "dotted") + 
        xlim(2006, 2014)+
       labs(title="Pre-Post in TX")
       )
fig_TX.save("prepost_TX.pdf")
fig_TX


# In[72]:


df_WA=df_final[(df_final['State']=='WA')]


# In[94]:


fig_WA=(ggplot(aes(x='Year', y='Death_Rate', group = 'State', color = 'State') , data = df_WA) + geom_smooth(method='lm', data=df_WA[df_WA['Year']<2011], color='blue')+ 
        geom_smooth(method='lm', data=df_WA[df_WA['Year']>=2011], color='red')+
        geom_point() + geom_vline(xintercept=2011, linetype = "dotted") + xlim(2008, 2014)+
         labs(title="Pre-Post in WA"))
fig_WA.save("prepost_WA.pdf")
fig_WA


# In[96]:


fig_WA =(ggplot(df_final, aes(x='Year',y ='Death_Rate', color='Policy_State'))
      + geom_smooth(df_final[(df_final['State'] != 'FL')& (df_final['State'] !='TX') & 
                             (df_final['State'] !='WA')& (df_final['Year']<2011) ], method = 'lm')
        + geom_smooth(df_final[(df_final['State'] != 'FL')& (df_final['State'] !='TX') & 
                             (df_final['State'] !='WA')& (df_final['Year']>=2011) ], method = 'lm')
       + geom_smooth(df_final[(df_final['State'] =='WA')& (df_final['Year']<2011) ], method = 'lm')
        + geom_smooth(df_final[(df_final['State'] =='WA')& (df_final['Year']>=2011) ], method = 'lm')
      + geom_vline(xintercept= 2011, linetype = 'dotted')+
        labs(title='Difference in Differece between WA and non-policy states in US'))
fig_WA.save('DID_WA.pdf')
fig_WA


# In[97]:


fig_FL =(ggplot(df_final, aes(x='Year',y ='Death_Rate', color='Policy_State'))
      + geom_smooth(df_final[(df_final['State'] != 'FL')& (df_final['State'] !='TX') & 
                             (df_final['State'] !='WA')& (df_final['Year']<2010) ], method = 'lm')
        + geom_smooth(df_final[(df_final['State'] != 'FL')& (df_final['State'] !='TX') & 
                             (df_final['State'] !='WA')& (df_final['Year']>=2010) ], method = 'lm')
       + geom_smooth(df_final[(df_final['State'] =='FL')& (df_final['Year']<2010) ], method = 'lm')
        + geom_smooth(df_final[(df_final['State'] =='FL')& (df_final['Year']>=2010) ], method = 'lm')
      + geom_vline(xintercept= 2010, linetype = 'dotted')+
           labs(title='Difference in Differece between FL and non-policy states in US'))
fig_FL.save('DID_FL.pdf')
fig_FL


# In[98]:


fig_TX =(ggplot(df_final, aes(x='Year',y ='Death_Rate', color='Policy_State'))
      + geom_smooth(df_final[(df_final['State'] != 'FL')& (df_final['State'] !='TX') & 
                             (df_final['State'] !='WA')& (df_final['Year']<2007) ], method = 'lm')
        + geom_smooth(df_final[(df_final['State'] != 'FL')& (df_final['State'] !='TX') & 
                             (df_final['State'] !='WA')& (df_final['Year']>=2007) ], method = 'lm')
       + geom_smooth(df_final[(df_final['State'] =='TX')& (df_final['Year']<2007) ], method = 'lm')
        + geom_smooth(df_final[(df_final['State'] =='TX')& (df_final['Year']>=2007) ], method = 'lm')
      + geom_vline(xintercept= 2007, linetype = 'dotted')+
           labs(title='Difference in Differece between TX and non-policy states in US'))
fig_TX.save('DID_TX.pdf')
fig_TX


# In[84]:


fig_TX.save("DID_TX.pdf")


# In[77]:


mod1 = smf.ols('Death_Rate ~ Post + Policy_State + Year_C + Post*Year_C + Post * Policy_State + Year_C * Policy_State + Policy_State * Year_C * Post', data=df_final_FL).fit()
print(mod1.summary())


# In[79]:


mod2 = smf.ols('Death_Rate ~ Post + Policy_State + Year_C + Post*Year_C + Post * Policy_State + Year_C * Policy_State + Policy_State * Year_C * Post', data=df_final_TX).fit()
print(mod2.summary())


# In[80]:


mod3 = smf.ols('Death_Rate ~ Post + Policy_State + Year_C + Post*Year_C + Post * Policy_State + Year_C * Policy_State + Policy_State * Year_C * Post', data=df_final_WA).fit()
print(mod3.summary())


# In[ ]:





# In[ ]:





# In[ ]:




