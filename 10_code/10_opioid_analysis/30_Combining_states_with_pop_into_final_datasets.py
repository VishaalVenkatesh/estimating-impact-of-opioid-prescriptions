import pandas as pd
import numpy as np
from plotnine import *

states =  ["AL", "AK",  "AR", "CA", "CO", "CT", "DC", "DE", "FL", "GA", 
           "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD", 
           "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ", 
           "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC", 
           "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"]

#Population Data
pop_data = pd.read_csv("/Users/abhirajvinnakota/Desktop/estimating-impact-of-opioid-prescription-regulations-team-6/20_intermediate_files/30_pop_data_analysis/pop_counties_20062012.csv", usecols = ['BUYER_STATE','BUYER_COUNTY','year','population']) #reading the data
pop_data = pop_data[pop_data['year'] == 2010][['BUYER_COUNTY','BUYER_STATE','population']] #filtered for 2010
pop_data = pop_data.rename({"BUYER_STATE":"STATE","BUYER_COUNTY":"COUNTY"}, axis=1) #renaming columns


## For Florida
# 1> Appending the datasets for individual states
final_df = pd.DataFrame(columns=('STATE','COUNTY','Year','opioids')) #creating empty dataframe with the required columns

for state in states: #iterating over the states
    df1 = pd.read_pickle('/Users/abhirajvinnakota/Desktop/estimating-impact-of-opioid-prescription-regulations-team-6/20_intermediate_files/10_opioids_analysis/20_state_level_data_from_20/florida/'+str(state)+'.pkl') #reading the file
    final_df = final_df.append(df1,sort = True) #appending to the empty dataframe (not empty after the first iteration)

# 2> Creating column for pre_post
final_df.loc[final_df['Year'].astype('str').astype('int') >= 2010, 'pre_post'] = 'post'
final_df.loc[final_df['Year'].astype('str').astype('int') < 2010, 'pre_post'] = 'pre'

# 3> Creating column for policy state
final_df.loc[(final_df['STATE'] == 'FL'), 'policy_state'] = 1
final_df.loc[(final_df['STATE'] != 'FL'), 'policy_state'] = 0

# 4> Dropping other policy change states from the analysis (namely, Texas and Washington)
final_df = final_df[~((final_df['STATE'] == 'WA') | (final_df['STATE'] == 'TX'))]

# 5> Final Dataset
final_data = final_df.merge(pop_data, on =['COUNTY','STATE'])#merging both the datasets
final_data['opioids_per_capita'] = np.divide(final_data['opioids'],final_data['population']) #calculating opioids per capita per year
final_data = final_data.drop(['opioids','population'],axis= 1 ) #droping unnessary columns
pd.to_pickle(final_data,'/Users/abhirajvinnakota/Desktop/estimating-impact-of-opioid-prescription-regulations-team-6/20_intermediate_files/10_opioids_analysis/30_final_data_sets_from_30/1.final_dataset_florida.pkl') #writing the final file to disk


df_florida = pd.read_pickle('/Users/abhirajvinnakota/Desktop/estimating-impact-of-opioid-prescription-regulations-team-6/20_intermediate_files/10_opioids_analysis/30_final_data_sets_from_30/1.final_dataset_florida.pkl')
df_florida.shape

df_florida.head()









# For Texas
#  1> Appending the datasets for individual states
final_df = pd.DataFrame(columns=('STATE','COUNTY','Year','Month','opioids')) #creating empty dataframe with the required columns

for state in states: #iterating over the states
    df1 = pd.read_pickle('/Users/abhirajvinnakota/Desktop/estimating-impact-of-opioid-prescription-regulations-team-6/20_intermediate_files/10_opioids_analysis/20_state_level_data_from_20/texas_wash/'+str(state)+'.pkl') #reading the file
    final_df = final_df.append(df1,sort = True) #appending to the empty dataframe (not empty after the first iteration)
    
#  2> Creating column for pre_post
final_df.loc[final_df['Year'].astype('str').astype('int') < 2007, 'pre_post'] = 'pre'
final_df.loc[final_df['Year'].astype('str').astype('int') >= 2007, 'pre_post'] = 'post'

# 2.5> Creating a column for plotting 
final_df['Year_axis'] = final_df['Year'] + (final_df['Month']/12)

#  3> Creating column for policy state
final_df.loc[(final_df['STATE'] == 'TX'), 'policy_state'] = 1
final_df.loc[(final_df['STATE'] != 'TX'), 'policy_state'] = 0

#  4> Dropping other policy change states from the analysis (namely, Florida and Washington)
final_df = final_df[~((final_df['STATE'] == 'WA') | (final_df['STATE'] == 'FL'))]

#  5> Final Dataset
final_data = final_df.merge(pop_data, on =['COUNTY','STATE']) #merging both the datasets
final_data['opioids_per_capita'] = np.divide(final_data['opioids'],final_data['population']) #calculating opioids per capita per year
final_data = final_data.drop(['opioids','population'],axis= 1 ) #droping unnessary columns
pd.to_pickle(final_data,'/Users/abhirajvinnakota/Desktop/estimating-impact-of-opioid-prescription-regulations-team-6/20_intermediate_files/10_opioids_analysis/30_final_data_sets_from_30/1.final_dataset_texas.pkl') #writing the final file to disk

df_texas = pd.read_pickle('/Users/abhirajvinnakota/Desktop/estimating-impact-of-opioid-prescription-regulations-team-6/20_intermediate_files/10_opioids_analysis/30_final_data_sets_from_30/1.final_dataset_texas.pkl') #read the final file to disk
df_texas.shape
df_texas.head()





# For Washington
#  1> appending the datasets for individual states
final_df = pd.DataFrame(columns=('STATE','COUNTY','Year','Month','opioids')) #creating empty dataframe with the required columns

for state in states: #iterating over the states
    df1 = pd.read_pickle('/Users/abhirajvinnakota/Desktop/estimating-impact-of-opioid-prescription-regulations-team-6/20_intermediate_files/10_opioids_analysis/20_state_level_data_from_20/texas_wash/'+str(state)+'.pkl') #reading the file
    final_df = final_df.append(df1,sort = True) #appending to the empty dataframe (not empty after the first iteration)
    
#  2> creating column for pre_post
final_df.loc[final_df['Year'].astype('str').astype('int') < 2011, 'pre_post'] = 'pre'
final_df.loc[final_df['Year'].astype('str').astype('int') >= 2011, 'pre_post'] = 'post'

# 2.5> Creating a column for plotting 
final_df['Year_axis'] = final_df['Year'] + (final_df['Month']/12)

#  3> creating column for policy state
final_df.loc[(final_df['STATE'] == 'WA'), 'policy_state'] = 1
final_df.loc[(final_df['STATE'] != 'WA'), 'policy_state'] = 0

#  4> dropping other policy change states from the analysis (namely, Florida and Texas)
final_df = final_df[~((final_df['STATE'] == 'TX') | (final_df['STATE'] == 'FL'))]

#  5> Final Dataset
final_data = final_df.merge(pop_data, on =['COUNTY','STATE']) #merging both the datasets
final_data['opioids_per_capita'] = np.divide(final_data['opioids'],final_data['population']) #calculating opioids per capita per year
final_data = final_data.drop(['opioids','population'],axis= 1 ) #droping unnessary columns
pd.to_pickle(final_data,'/Users/abhirajvinnakota/Desktop/estimating-impact-of-opioid-prescription-regulations-team-6/20_intermediate_files/10_opioids_analysis/30_final_data_sets_from_30/1.final_dataset_washington.pkl') #writing the final file to disk

df_wash = pd.read_pickle('/Users/abhirajvinnakota/Desktop/estimating-impact-of-opioid-prescription-regulations-team-6/20_intermediate_files/10_opioids_analysis/30_final_data_sets_from_30/1.final_dataset_washington.pkl') #read the final file to disk
df_wash.shape

df_wash.head()


