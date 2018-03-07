# 05 March 2018 Miroslav Gasparek
# Python bootcamp, lesson 32: Practice with Pandas

# Import modules
import numpy as np
import pandas as pd

import matplotlib.pyplot as plt
import seaborn as sns
rc={'lines.linewidth': 2, 'axes.labelsize': 18, 'axes.titlesize': 18}
sns.set(rc=rc)

# Practice 1
# Load in the frog tongue adhesion data set.
df = pd.read_csv('data/frog_tongue_adhesion.csv', comment='#')

# Extract the impact time of all impacts that had an adhesive strength of
# magnitude greater than 2000 Pa
impact_time = df.loc[np.abs(df['adhesive strength (Pa)'])>2000 , ['impact time (ms)']]
# Extract the impact force and adhesive force for all of Frog II's strikes
ImAdForce = df.loc[df['ID']=='II', ['impact force (mN)', 'adhesive force (mN)']]
# Extract the adhesive force and the time the frog pulls on the target for
# juvenile frogs (Frogs III and IV)
data_juv = df.loc[df['ID'].isin(['III','IV']), ['adhesive force (mN)', 'time frog pulls on target (ms)']]

# Practice 2
# groupby() splits up DataFrame based on some criterion

# 1. Extract Frog I's impact forces and compute the mean
f1_if = df.loc[df['ID']=='I', ['impact force (mN)']]
f1_if_mean = np.mean(f1_if)
# 2. Do the same for the other three frogs
f2_if = df.loc[df['ID']=='II', ['impact force (mN)']]
f2_if_mean = np.mean(f2_if)
f3_if = df.loc[df['ID']=='III', ['impact force (mN)']]
f3_if_mean = np.mean(f3_if)
f4_if = df.loc[df['ID']=='IV', ['impact force (mN)']]
f4_if_mean = np.mean(f4_if)

# 3. Write a for loop for this
# Initiate empty array
mean_array = np.empty(len(df.ID.unique()))
# For loop
for i in range(len(df.ID.unique())):
    mean_array[i] = np.mean(df.loc[df['ID']==df.ID.unique()[i], ['impact force (mN)']])
# We did not get DataFrame out of this, just an numpy array
# We only want ID's and impact forces, so slice those out
df_impf = df.loc[:, ['ID', 'impact force (mN)']]
# Make a GroupBy object
grouped = df_impf.groupby('ID')
# Apply the np.mean function to the grouped object
df_mean_impf = grouped.apply(np.mean)
# Pull the mean impact force of interest
impf_mean_frog3 = df_mean_impf.loc['III', :]

# Apply multiple functions to a GroupBy object using the agg() method
multi_grouped = grouped.agg([np.mean, np.median])

# a) Compute standard deviation of the impact forces for each frog
grouped_std = grouped.apply(np.std)

# b) Write a function
def coeff_of_var(data):
    """ Computes the coefficient of variation of a data set."""
    return np.std(data)/np.abs(np.mean(data))

# Make GroupBy object with two columns of interest in DataFrame
grouped = df[['ID', 'impact force (mN)','adhesive force (mN)']].groupby('ID')
# Apply the coeff_of_var function
cov_data = grouped.apply(coeff_of_var)

# Make a GroupBy object with columns of interest grouped by ID
grouped1 = df[['ID','impact force (mN)', 'adhesive force (mN)']].groupby('ID')
# Apply the functions
cov_data_final = grouped1.agg([np.mean, np.median, np.std, coeff_of_var])

# We need to specify two things to select a column
cov_data_if_mean = cov_data_final.loc[:, ('impact force (mN)', 'mean')]
# If we just want the mean impact force and mean adhesive force
cov_data_if_af_mean = cov_data_final.loc[:, (('impact force (mN)', 'adhesive force (mN)'), 'mean')]

# Make the DataFrame tidy
# Make the index (frog ID) real part of DataFrame
cov_data_final['ID'] = cov_data_final.index
# Melt the DataFrame to make it tidy
final = pd.melt(cov_data_final, var_name=['quantity', 'statistic'], id_vars='ID')
