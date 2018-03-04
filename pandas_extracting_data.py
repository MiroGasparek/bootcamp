# 03 March 2018 Miroslav Gasparek
# Python bootcamp, lesson 31: Extracting data of interest)

# Import modules
import numpy as np
import pandas as pd

import matplotlib.pyplot as plt
import seaborn as sns
rc={'lines.linewidth': 2, 'axes.labelsize': 18, 'axes.titlesize': 18}
sns.set(rc=rc)

# Load the frog data
df = pd.read_csv('data/frog_tongue_adhesion.csv', comment='#')

# Selecting data
# Slice out big forces (impact force above one Newton)
df_big_force = df[df['impact force (mN)'] > 1000]
# Select a single experiment
exp42 = df.loc[42,:]
# Select multiple columns
cols = df.loc[:, ['impact force (mN)', 'adhesive force (mN)']]
# Boolean indexing using loc, selecting Frog I's impact force and adhesive force
frog1cols = df.loc[df['ID']=='I', ['impact force (mN)', 'adhesive force (mN)']]

# Finding correlations
# Check if impact force and adhesive strength might be correlated
fig1 = plt.figure(1)
plt.plot(df['impact force (mN)'], df['adhesive force (mN)'], marker='.',
        linestyle='none')
plt.xlabel('impact force (mN)')
plt.ylabel('adhesive force (mN)')
fig1.show()

# Make a quick plot with axis already labelled
df.plot(x='total contact area (mm2)', y='adhesive force (mN)', kind='scatter')
plt.show()

# Compute the Pearson correlation between all pairs of data
# with the corr() method of DataFrame
correlations = df.corr()
print(correlations)

# Shortcut names
# Rename the impact force column
df = df.rename(columns={'impact force (mN)': 'impf'})
