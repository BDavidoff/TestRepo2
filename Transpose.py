#!/usr/bin/env python
# coding: utf-8

# 
# get study codes in chronilogical order using stMemname and custom sort
# transpose master list into shape where col 1 is UCodeID, and each subsequent column is the stMemnames, 
# with null values where a row with said UCodeID doesnt have that stMemname.
# 

# In[2]:


#import libraries
import pandas as pd
import numpy as np


# In[6]:


# Sample data
data = {
    'ID': [1, 1, 1, 2, 2, 3],
    'Study': ['f18', 's19', 'w18', 'w19', 'f19', 's18']
}

df = pd.DataFrame(data)


# In[7]:


# Custom sort function
def sort_study(study):
    season_order = {'w': 0, 's': 1, 'f': 2}
    season = study[0]
    year = int(study[1:])
    return (year, season_order[season])

# Sort the DataFrame
df = df.sort_values(by='Study', key=lambda x: x.map(sort_study))

# Create pivot table
pivot_df = df.pivot(index='ID', columns='Study', values='Study')
pivot_df = pivot_df.reset_index()

# Get column names
sorted_columns = ['ID'] + sorted(pivot_df.columns[1:], key=sort_study)
pivot_df = pivot_df.reindex(columns=sorted_columns)

# Fill NaN values with None
pivot_df = pivot_df.where(pd.notnull(pivot_df), None)

# Fill missing studies with -1 if they appeared in previous study years
def fill_missing_studies(row):
    for i, study in enumerate(sorted_columns[1:], start=1):
        if pd.isnull(row[study]) and i > 1 and not pd.isnull(row[sorted_columns[i-1]]):
            row[study] = -1
    return row

pivot_df = pivot_df.apply(fill_missing_studies, axis=1)

print(pivot_df)
