# 03 March 2018 Miroslav Gasparek
# Python bootcamp, lesson 30: Introduction to Pandas

# Import modules
import numpy as np
import pandas as pd

import matplotlib.pyplot as plt
import seaborn as sns
rc={'lines.linewidth': 2, 'axes.labelsize': 18, 'axes.titlesize': 18}
sns.set(rc=rc)

# Read in data files with pandas
df_high = pd.read_csv('data/xa_high_food.csv', comment='#')
df_low = pd.read_csv('data/xa_low_food.csv', comment='#')

# Read in data files with pandas with no orw headings.
df_high = pd.read_csv('data/xa_high_food.csv', comment='#', header=None)
df_low = pd.read_csv('data/xa_low_food.csv', comment='#', header=None)
# A Pandas Series is basically a one-dimensional DataFrame
# Pandas Series can be thought of as generalized NumPy array.

# Dictionary of top men's World Cup scorers and how many goals they scored
wc_dict = { 'Klose': 16,
            'Ronaldo': 15,
            'Muller': 14,
            'Fontaine': 13,
            'Pele': 12,
            'Kocsis': 11,
            'Klinsmann': 11}
# Create a Series from the Dictionary
s_goals = pd.Series(wc_dict)

# Make another Dictionary
nation_dict = { 'Klose': 'Germany',
                'Ronaldo': 'Brazil',
                'Muller': 'Germany',
                'Fontaine': 'France',
                'Pele': 'Brazil',
                'Kocsis': 'Hungary',
                'Klinsmann': 'Germany'}
# Series with nations
s_nation = pd.Series(nation_dict)

# Combine Series into a DataFrame, whose keys are the column headers
# and values are the series we are building into a DataFrame.

# Combine into a DataFrame
df_wc = pd.DataFrame({'nation': s_nation, 'goals': s_goals})

# We can index by columns
print(df_wc['goals'])
# We can access data of a single particular person, like slice indexing
print(df_wc.loc['Fontaine', :])

# Look only at German players, for instance, using similar Boolean indexing
german_nat = df_wc.loc[df_wc['nation']=='Germany', :]

# Combine the cross-sectional area data into a DataFrame
# These series are not Series, so we use pd.concat()
# Change column headings
df_low.columns = ['low']
df_high.columns = ['high']

# Concatenate DataFrames
df = pd.concat((df_low, df_high), axis=1)

# Outputting a new CSV file
# kwarg index='False' to avoid explicit writing of the indices to the file
# Write out DataFrame
df.to_csv('xa_combined.csv', index=False)

# Load DataFrame
df_reloaded = pd.read_csv('xa_combined.csv')

## Tidy DataFrames follow these rules:
# 1. Each variable is a column.
# 2. Each observation is a row.
# 3. Each type of observation has its own separate DataFrame.

# Tidy up the DataFrame
df = pd.melt(df, var_name='food density', value_name='cross-sectional area (sq micron)').dropna()
