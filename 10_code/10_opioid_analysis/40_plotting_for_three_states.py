import numpy as np
import pandas as pd
from plotnine import *


## Florida
df = pd.read_pickle("/Users/abhirajvinnakota/Desktop/estimating-impact-of-opioid-prescription-regulations-team-6/20_intermediate_files/10_opioids_analysis/30_final_data_sets_from_30/1.final_dataset_florida.pkl")
df['Year']=df['Year'].astype(str).astype(int)
df['policy_state'] = df['policy_state'].astype('category')


# pre-post
fig =(ggplot(df[df['policy_state'] == 1], aes(x='Year',y ='opioids_per_capita', color = 'policy_state'))
      + geom_point(df[df['policy_state'] == 1],color = 'grey', alpha = 0.2)
      + geom_smooth(df[(df['policy_state'] == 1) & (np.equal(df['pre_post'], 'pre'))], method = 'lm', se = True)
      + geom_smooth(df[(df['policy_state'] == 1) & (np.equal(df['pre_post'], 'post'))], method = 'lm', se = True)
      + geom_vline(xintercept= 2010, linetype = 'dotted')
      + labs( x = 'Year', y = 'Opioid Shipments per Capita', title ='Pre-Post Analysis - Florida (Policy Change Jan 1st 2010)', color = 'Policy State')
      + guides(fill = False, color = False, linetype = False, shape = False))
fig


#diff-in-diff
fig =(ggplot(df, aes(x='Year',y ='opioids_per_capita', color = 'policy_state'))
      + geom_point(df[df['policy_state'] == 1],color = 'grey', alpha = 0.2)
      + geom_smooth(df[(df['policy_state'] == 1) & (np.equal(df['pre_post'], 'pre'))], method = 'lm',  se = True)
      + geom_smooth(df[(df['policy_state'] == 1) & (np.equal(df['pre_post'], 'post'))], method = 'lm',  se = True)
      + geom_smooth(df[(df['policy_state'] == 0) & (np.equal(df['pre_post'], 'pre'))], method = 'lm',  se = True)
      + geom_smooth(df[(df['policy_state'] == 0) & (np.equal(df['pre_post'], 'post'))], method = 'lm',  se = True)
      + geom_vline(xintercept= 2010, linetype = "dotted")
      + labs( x = 'Year', y = 'Opioid Shipments per Capita', title ='Diff-in-Diff Analysis - Florida (Policy Change Jan 1st 2010)'))
fig




## Texas
df_texas = pd.read_pickle("/Users/abhirajvinnakota/Desktop/estimating-impact-of-opioid-prescription-regulations-team-6/20_intermediate_files/10_opioids_analysis/30_final_data_sets_from_30/1.final_dataset_texas.pkl")
df_texas['Year_axis'] = df_texas['Year_axis'].astype(str).astype(float)
df_texas['Year'] = df_texas['Year'].astype(str).astype(int)
df_texas['policy_state'] = df_texas['policy_state'].astype('category')



#pre-post
fig =(ggplot(df_texas[df_texas['policy_state'] == 1], aes(x='Year_axis',y ='opioids_per_capita', color = 'policy_state'))
      + geom_smooth(df_texas[(df_texas['policy_state'] == 1) & (np.equal(df_texas['pre_post'], 'pre'))], method = 'lm')
      + geom_smooth(df_texas[(df_texas['policy_state'] == 1) & (np.equal(df_texas['pre_post'], 'post'))], method = 'lm')
      + geom_vline(xintercept = 2007, linetype = "dotted")
      + labs(x = 'Year', y = 'Opioid Shipments per Capita', title ='Pre-Post Analysis - Texas (Policy Change Jan 1st 2007)')
      + guides(fill = False, color = False, linetype = False, shape = False))
fig



#yearly-trend
fig =(ggplot(df_texas, aes(x='Year_axis',y ='opioids_per_capita', color = 'policy_state'))
      + geom_smooth(df_texas[(df_texas['policy_state'] == 1) & (df_texas['Year'] == 2006)], method = 'loess')
      + geom_smooth(df_texas[(df_texas['policy_state'] == 1) & (np.equal(df_texas['Year'], 2007))], method = 'loess')
      + geom_smooth(df_texas[(df_texas['policy_state'] == 1) & (np.equal(df_texas['Year'], 2008))], method = 'loess')
      + geom_smooth(df_texas[(df_texas['policy_state'] == 1) & (np.equal(df_texas['Year'], 2009))], method = 'loess')
      + geom_smooth(df_texas[(df_texas['policy_state'] == 1) & (np.equal(df_texas['Year'], 2010))], method = 'loess')
      + geom_smooth(df_texas[(df_texas['policy_state'] == 1) & (np.equal(df_texas['Year'], 2011))], method = 'loess')
      + geom_smooth(df_texas[(df_texas['policy_state'] == 1) & (np.equal(df_texas['Year'], 2012))], method = 'loess')
      + geom_vline(xintercept= 2007, linetype = "dotted")
      + labs(x = 'Year', y = 'Opioid Shipments per Capita', title ='Yearly Trends - Texas (Policy Change Jan 1st 2007)')
      + guides(fill = False, color = False, linetype = False, shape = False))
fig



# Pre-post vs Policy_state matrix
df2 = df_texas.groupby(['pre_post','policy_state'],as_index=False)['opioids_per_capita'].mean()
df2.pivot(index='pre_post', columns='policy_state', values='opioids_per_capita')



## Washington
df_wash = pd.read_pickle("/Users/abhirajvinnakota/Desktop/estimating-impact-of-opioid-prescription-regulations-team-6/20_intermediate_files/10_opioids_analysis/30_final_data_sets_from_30/1.final_dataset_washington.pkl")
df_wash['Year_axis'] = df_wash['Year_axis'].astype(str).astype(float)
df_wash['Year'] = df_wash['Year'].astype(str).astype(int)
df_wash['policy_state'] = df_wash['policy_state'].astype('category')


# Pre-post vs Policy_state matrix
df2 = df_wash.groupby(['pre_post','policy_state'],as_index=False)['opioids_per_capita'].mean()
df2.pivot(index='pre_post', columns='policy_state', values='opioids_per_capita')

