# Data Wrangling

from enum import unique
import pandas as pd
import numpy as np

df=pd.read_csv("https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/dataset_part_1.csv")
df.head(10)

df.isnull().sum()/len(df)*100

df.dtypes # check the data types of the columns

df['LaunchSite'].value_counts(unique) # check the unique values in the Launch_Site column
df['LaunchSite'].value_counts('CCAFS SLC 40') #

df['Orbit'].value_counts(unique) # check the unique values in the Orbit column  

landing_outcomes = df['Outcome'].value_counts(unique) 

for i,outcome in enumerate(landing_outcomes.keys()):
    print(i,outcome)

bad_outcomes=set(landing_outcomes.keys()[[1,3,5,6,7]])
bad_outcomes

landing_class = df['Outcome'].apply(lambda x: 0 if x in bad_outcomes else 1)
df['Class']=landing_class
df[['Class']].head(8)



df["Class"].mean() # Check Success Rate

df.to_csv("dataset_part_2.csv", index=False) # Save the DataFrame to a CSV file
