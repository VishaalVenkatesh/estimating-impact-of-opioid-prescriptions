
import pandas as pd
import numpy as np


states =  ["AL", "AK",  "AR", "CA", "CO", "CT", "DC", "DE", "FL", "GA", 
           "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD", 
           "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ", 
           "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC", 
           "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"]

#Population Data
pop_data = pd.read_csv("/Users/abhirajvinnakota/Desktop/Project/processed_data/pop_counties_20062012.csv", usecols = ['BUYER_STATE','BUYER_COUNTY','year','population']) #reading the data
pop_data = pop_data[pop_data['year'] == 2010][['BUYER_COUNTY','BUYER_STATE','population']] #filtered for 2010
pop_data = pop_data.rename({"BUYER_STATE":"STATE","BUYER_COUNTY":"COUNTY"}, axis=1) #renaming columns


#Dataset prep for Florida
for state in states:
    df = pd.read_pickle("/Users/abhirajvinnakota/Desktop/Project/"+str(state)+".pkl") #reading state level data for opioids
    df["TRANSACTION_DATE"] = df["TRANSACTION_DATE"].astype('str').str.zfill(8) #Pre-fixed 0 for the strings with 7 digits
    df["TRANSACTION_DATE"] = pd.to_datetime(df["TRANSACTION_DATE"], format = "%m%d%Y") #converting to datetime format
    df["Year"] = df["TRANSACTION_DATE"].dt.to_period('Y') #extracting year
    df = df[(df["Year"] >= 2008) & (df["Year"] <= 2012)] #filtered for the required years
    df['CALC_BASE_WT_IN_GM'] = df['CALC_BASE_WT_IN_GM'].astype('float') #changing dtype from string to float
    df['opioids'] = np.multiply(df['CALC_BASE_WT_IN_GM'],df['MME_Conversion_Factor']) #opioids calculation
    df = df.reset_index() #reseting indicies
    df = df.drop(['CALC_BASE_WT_IN_GM','TRANSACTION_DATE','DRUG_NAME','MME_Conversion_Factor','index'], axis = 1) #dropping columns 
    df = df.rename({"BUYER_STATE":"STATE","BUYER_COUNTY":"COUNTY"}, axis=1) #renaming columns 
    df['opioids_sum'] = df.groupby(['STATE','COUNTY','Year'])['opioids'].transform(sum) #summing opioids at a yearly level
    df = df.drop(['opioids'], axis = 1) #dropping the opioids column
    df.drop_duplicates(inplace=True) #dropping duplicate value to get to the final data set
    pd.to_pickle(df,'/Users/abhirajvinnakota/Desktop/Project/processed_data/florida/'+str(state)+'.pkl' ) #writing to disk


#appending the datasets for individual states
final_df = pd.DataFrame(columns=('STATE','COUNTY','Year','opioids_sum')) #creating empty dataframe with the required columns


for state in states: #iterating over the states
    df1 = pd.read_pickle("/Users/abhirajvinnakota/Desktop/Project/processed_data/florida/"+str(state)+".pkl") #reading the file
    final_df = final_df.append(df1,sort = True) #appending to the empty dataframe (not empty after the first iteration)



#creating column for pre_post
final_df.loc[final_df['Year'].astype('str').astype('int') > 2010, 'pre_post'] = 'post'
final_df.loc[final_df['Year'].astype('str').astype('int') == 2010, 'pre_post'] = 'exact'
final_df.loc[final_df['Year'].astype('str').astype('int') < 2010, 'pre_post'] = 'pre'


#creating column for policy state
final_df.loc[(final_df['STATE'] == 'FL'), 'policy_state'] = 1
final_df.loc[(final_df['STATE'] != 'FL'), 'policy_state'] = 0


#dropping other policy change states from the analysis (namely, Texas and Washington)
final_df = final_df[~((final_df['STATE'] == 'WA') | (final_df['STATE'] == 'TX'))]


#Final Dataset
final_data = final_df.merge(pop_data, on =['COUNTY','STATE']) #merging both the datasets
final_data['opioids per capita'] = np.divide(final_data['opioids_sum'],final_data['population']) #calculating opioids per capita per year
final_data = final_data.drop(['opioids_sum','population'],axis= 1 ) #droping unnessary columns
pd.to_pickle(final_data,'/Users/abhirajvinnakota/Desktop/Project/processed_data/florida/1.final_dataset.pkl') #writing the final file to disk


#Dataset prep for Texas
for state in states:
    df = pd.read_pickle("/Users/abhirajvinnakota/Desktop/Project/"+str(state)+".pkl") #reading state level data for opioids
    df["TRANSACTION_DATE"] = df["TRANSACTION_DATE"].astype('str').str.zfill(8) #Pre-fixed 0 for the strings with 7 digits
    df["TRANSACTION_DATE"] = pd.to_datetime(df["TRANSACTION_DATE"], format = "%m%d%Y") #converting to datetime format
    df["Year"] = df["TRANSACTION_DATE"].dt.to_period('Y') #extracting year
    df["Month"] = df["TRANSACTION_DATE"].dt.to_period('M') #extracting month
    df = df[(df["Year"] >= 2006) & (df["Year"] <= 2008)] #filtered for the required years
    df['CALC_BASE_WT_IN_GM'] = df['CALC_BASE_WT_IN_GM'].astype('float') #changing dtype from string to float
    df['opioids'] = np.multiply(df['CALC_BASE_WT_IN_GM'],df['MME_Conversion_Factor']) #opioids calculation
    df = df.reset_index() #reseting indicies
    df = df.drop(['CALC_BASE_WT_IN_GM','TRANSACTION_DATE','DRUG_NAME','MME_Conversion_Factor','index'], axis = 1) #dropping columns 
    df = df.rename({"BUYER_STATE":"STATE","BUYER_COUNTY":"COUNTY"}, axis=1) #renaming columns 
    df['opioids_sum'] = df.groupby(['STATE','COUNTY','Year','Month'])['opioids'].transform(sum) #summing opioids at a yearly level
    df = df.drop(['opioids'], axis = 1) #dropping the opioids column
    df.drop_duplicates(inplace=True) #dropping duplicate value to get to the final data set
    pd.to_pickle(df,'/Users/abhirajvinnakota/Desktop/Project/processed_data/texas/'+str(state)+'.pkl' ) #writing to disk


#appending the datasets for individual states
final_df = pd.DataFrame(columns=('STATE','COUNTY','Year','Month','opioids_sum')) #creating empty dataframe with the required columns

for state in states: #iterating over the states
    df1 = pd.read_pickle("/Users/abhirajvinnakota/Desktop/Project/processed_data/texas/"+str(state)+".pkl") #reading the file
    final_df = final_df.append(df1,sort = True) #appending to the empty dataframe (not empty after the first iteration)

#creating column for pre_post
final_df.loc[final_df['Year'].astype('str').astype('int') == 2006, 'pre_post'] = 'pre'
final_df.loc[final_df['Year'].astype('str').astype('int') == 2007, 'pre_post'] = 'exact'
final_df.loc[final_df['Year'].astype('str').astype('int') == 2008, 'pre_post'] = 'post'


#creating column for policy state
final_df.loc[(final_df['STATE'] == 'TX'), 'policy_state'] = 1
final_df.loc[(final_df['STATE'] != 'TX'), 'policy_state'] = 0


#dropping other policy change states from the analysis (namely, Florida and Washington)
final_df = final_df[~((final_df['STATE'] == 'WA') | (final_df['STATE'] == 'FL'))]


#Final Dataset
final_data = final_df.merge(pop_data, on =['COUNTY','STATE']) #merging both the datasets
final_data['opioids per capita'] = np.divide(final_data['opioids_sum'],final_data['population']) #calculating opioids per capita per year
final_data = final_data.drop(['opioids_sum','population'],axis= 1 ) #droping unnessary columns
pd.to_pickle(final_data,'/Users/abhirajvinnakota/Desktop/Project/processed_data/texas/1.final_dataset.pkl') #writing the final file to disk


#Dataset prep for Washington
for state in states:
    df = pd.read_pickle("/Users/abhirajvinnakota/Desktop/Project/"+str(state)+".pkl") #reading state level data for opioids
    df["TRANSACTION_DATE"] = df["TRANSACTION_DATE"].astype('str').str.zfill(8) #Pre-fixed 0 for the strings with 7 digits
    df["TRANSACTION_DATE"] = pd.to_datetime(df["TRANSACTION_DATE"], format = "%m%d%Y") #converting to datetime format
    df["Year"] = df["TRANSACTION_DATE"].dt.to_period('Y') #extracting year
    df["Month"] = df["TRANSACTION_DATE"].dt.to_period('M') #extracting month
    df = df[(df["Year"] >= 2010) & (df["Year"] <= 2012)] #filtered for the required years
    df['CALC_BASE_WT_IN_GM'] = df['CALC_BASE_WT_IN_GM'].astype('float') #changing dtype from string to float
    df['opioids'] = np.multiply(df['CALC_BASE_WT_IN_GM'],df['MME_Conversion_Factor']) #opioids calculation
    df = df.reset_index() #reseting indicies
    df = df.drop(['CALC_BASE_WT_IN_GM','TRANSACTION_DATE','DRUG_NAME','MME_Conversion_Factor','index'], axis = 1) #dropping columns 
    df = df.rename({"BUYER_STATE":"STATE","BUYER_COUNTY":"COUNTY"}, axis=1) #renaming columns 
    df['opioids_sum'] = df.groupby(['STATE','COUNTY','Year','Month'])['opioids'].transform(sum) #summing opioids at a yearly level
    df = df.drop(['opioids'], axis = 1) #dropping the opioids column
    df.drop_duplicates(inplace=True) #dropping duplicate value to get to the final data set
    pd.to_pickle(df,'/Users/abhirajvinnakota/Desktop/Project/processed_data/washington/'+str(state)+'.pkl' ) #writing to disk


#appending the datasets for individual states
final_df = pd.DataFrame(columns=('STATE','COUNTY','Year','Month','opioids_sum')) #creating empty dataframe with the required columns

for state in states: #iterating over the states
    df1 = pd.read_pickle("/Users/abhirajvinnakota/Desktop/Project/processed_data/washington/"+str(state)+".pkl") #reading the file
    final_df = final_df.append(df1,sort = True) #appending to the empty dataframe (not empty after the first iteration)

#creating column for pre_post
final_df.loc[final_df['Year'].astype('str').astype('int') == 2010, 'pre_post'] = 'pre'
final_df.loc[final_df['Year'].astype('str').astype('int') == 2011, 'pre_post'] = 'exact'
final_df.loc[final_df['Year'].astype('str').astype('int') == 2012, 'pre_post'] = 'post'


#creating column for policy state
final_df.loc[(final_df['STATE'] == 'WA'), 'policy_state'] = 1
final_df.loc[(final_df['STATE'] != 'WA'), 'policy_state'] = 0


#dropping other policy change states from the analysis (namely, Florida and Texas)
final_df = final_df[~((final_df['STATE'] == 'TX') | (final_df['STATE'] == 'FL'))]


#Final Dataset
final_data = final_df.merge(pop_data, on =['COUNTY','STATE']) #merging both the datasets
final_data['opioids per capita'] = np.divide(final_data['opioids_sum'],final_data['population']) #calculating opioids per capita per year
final_data = final_data.drop(['opioids_sum','population'],axis= 1 ) #droping unnessary columns
pd.to_pickle(final_data,'/Users/abhirajvinnakota/Desktop/Project/processed_data/texas/1.final_dataset.pkl') #writing the final file to disk

