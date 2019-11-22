# Where did we get our raw data from?

The following are the sources for all the raw data we have used in this analysis. 

## 1.	Dataset on Reporting to the US Drug Enforcement Agency (DEA):

https://www.washingtonpost.com/national/2019/07/18/how-download-use-dea-pain-pills-database/?arc404=true

•	We will use the Washington Post version of the dataset. This dataset includes data on only two opioids – Hydrocodone & Oxycodone. These opioids however account for more than 75% of opioids prescribed. 
•	The COUNTY and STATE columns in the goal dataset would be gotten from the BUYER_COUNTY and BUYER_STATE columns. 
•	The MONTH and YEAR can be obtained from TRANSACTION_DATE. Month level analysis will only be done for Washington and Texas due to lack of sufficient data post policy change. For Florida, a yearly analysis will be done.  
•	The OPIOD PER CAPITA can be calculated by dividing the total volume of opioid bought inside of a county divided by the population of the county. To calculate the total volume of opioid bought in a county, we multiply the “CALC_BASE_WT_IN_GM” with the “MME_Conversion_Factor” and sum up the value at county level.
•	PERIOD: This column will be calculated based on pre and the post periods. 0 for pre and 1 for post. 
•	POLICY STATE: This will tell us if the state has and opioid policy enforced. This will be based on the “BUYER_STATE” column in the data. 

## 2.	Population Data from the US Census – POPULATION:

https://data.ers.usda.gov/reports.aspx?ID=17827&AspxAutoDetectCookieSupport=1

•	This data frame comprises of population data as collected by the US census at a county level. 
•	The population for the year 2010 will be the most relevant to this analysis as it is the closest to the years under consideration. 
•	We choose to use the population for 2010 for all the years under consideration as using rate of change of population assumes a linear rate of increase and may not be ideal for all the counties. Moreover, we do not have the rate of change of population for the years prior to 2010. This makes using 2010 population data throughout more reasonable. 
