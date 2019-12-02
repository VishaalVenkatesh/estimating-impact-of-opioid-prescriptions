
import pandas as pd
import numpy as np

states =  ["AL", "AK",  "AR", "CA", "CO", "CT", "DC", "DE", "FL", "GA", 
           "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD", 
           "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ", 
           "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC", 
           "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"]

#Dataset prep for Florida
for state in states:  
    df = pd.read_pickle("/Users/abhirajvinnakota/Desktop/Project/new_data/abhiraj_data/"+ state + ".pkl") #reading state level data for opioids
    df["TRANSACTION_DATE"] = pd.to_datetime(df["TRANSACTION_DATE"], format = "%m%d%Y") #converting to datetime format
    df["Year"] = df["TRANSACTION_DATE"].dt.year #extracting year
    df['opioids'] = df['CALC_BASE_WT_IN_GM'] * df['MME_Conversion_Factor']
    df = df.reset_index() #reseting indicies
    df = df.drop(['CALC_BASE_WT_IN_GM','TRANSACTION_DATE','DRUG_NAME','MME_Conversion_Factor','index'], axis = 1) #dropping columns 
    df = df.rename({"BUYER_STATE":"STATE","BUYER_COUNTY":"COUNTY"}, axis=1) #renaming columns 
    df = df.groupby(['STATE','COUNTY','Year'],as_index=False).sum() #summing opioids at a yearly level
    pd.to_pickle(df,'/Users/abhirajvinnakota/Desktop/estimating-impact-of-opioid-prescription-regulations-team-6/20_intermediate_files/10_opioids_analysis/20_state_level_data_from_20/florida/'+state+'.pkl' ) #writing to disk



#Dataset prep for Texas & Washington
for state in states:  
    df = pd.read_pickle("/Users/abhirajvinnakota/Desktop/Project/new_data/abhiraj_data/"+ state + ".pkl") #reading state level data for opioids
    df["TRANSACTION_DATE"] = pd.to_datetime(df["TRANSACTION_DATE"], format = "%m%d%Y") #converting to datetime format
    df["Year"] = df["TRANSACTION_DATE"].dt.year #extracting year
    df["Month"] = df["TRANSACTION_DATE"].dt.month #extracting month
    df['opioids'] = df['CALC_BASE_WT_IN_GM'] * df['MME_Conversion_Factor']
    df = df.reset_index() #reseting indicies
    df = df.drop(['CALC_BASE_WT_IN_GM','TRANSACTION_DATE','DRUG_NAME','MME_Conversion_Factor','index'], axis = 1) #dropping columns 
    df = df.rename({"BUYER_STATE":"STATE","BUYER_COUNTY":"COUNTY"}, axis=1) #renaming columns 
    df = df.groupby(['STATE','COUNTY','Year','Month'],as_index=False).sum() #summing opioids at a yearly level
    df.head()
    pd.to_pickle(df,'/Users/abhirajvinnakota/Desktop/estimating-impact-of-opioid-prescription-regulations-team-6/20_intermediate_files/10_opioids_analysis/20_state_level_data_from_20/texas_wash/'+state+'.pkl' ) #writing to disk


