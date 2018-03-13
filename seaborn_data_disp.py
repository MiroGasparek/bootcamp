# 13 March 2018 Miroslav Gasparek
# Python bootcamp, lesson 34: Seaborn and data display

# Import modules
import numpy as np
import pandas as pd

# This is how we import the module of Matplotlib we'll be using
import matplotlib.pyplot as plt

# Some pretty Seaborn settings
import seaborn as sns
rc={'lines.linewidth': 2, 'axes.labelsize': 18, 'axes.titlesize': 18}
sns.set(rc=rc)
##############################
# Close all open figures
plt.close('all')

# Load the data of the frog
df = pd.read_csv('data/frog_tongue_adhesion.csv', comment='#')
# Rename impact force column
df = df.rename(columns={'impact force (mN)': 'impf'})

# Mean impact force of frog I
np.mean(df.loc[df['ID']=='I', 'impf'])

# Calculate the means and SEMs of all four frogs
# For loop for mean and standard error of the mean
mean_impf = np.empty(4)
sem_impf  = np.empty(4)
for i, frog in enumerate(['I', 'II', 'III', 'IV']):
    mean_impf[i] = np.mean(df.loc[df['ID']==frog, 'impf'])
    n = np.sum(df['ID']=='I')
    sem_impf = np.std(df.loc[df['ID']==frog, 'impf']) / np.sqrt(n)

print(mean_impf)
print(sem_impf)

#####
# More advanced: calculate by groupby() and mean() and sem()
# gb_frog = dg.groupby('ID')
# mean_impf = gb_frog['impf'].mean()
# sem_impf = gb_frog['impf'].sem()
####

# Make a bar graph
fig1 = plt.figure(1)
plt.bar(np.arange(4), mean_impf, yerr=sem_impf, ecolor='black',
        tick_label=['I', 'II', 'III', 'IV'], align='center')
plt.ylabel('impact force (nM)')
fig1.show()

# Easier plot with Seaborn
fig2 = plt.figure(2)
sns.barplot(data=df, x='ID', y='impf')
plt.xlabel('')
plt.ylabel('impact force (mN)')
fig2.show()

###
# Message: do not make bar graphs.
###

# Bee swarm plot
fig3 = plt.figure(3)
sns.swarmplot(data=df, x='ID', y='impf')
plt.margins(0.02)
plt.xlabel('')
plt.ylabel('impact force (mN)')
fig3.show()

# Bee swarm plot with the date of measurement
fig4 = plt.figure(4)
ax = sns.swarmplot(data=df, x = 'ID', y = 'impf', hue='date')
ax.legend_.remove() # ???
plt.margins(0.02)
plt.xlabel('')
plt.ylabel('impact force (mN)')
fig4.show()

# When too many data points for bee swarm plot, use box plot
fig5 = plt.figure(5)
sns.boxplot(data=df, x='ID', y='impf')
plt.margins(0.02)
plt.xlabel('frog ID')
plt.ylabel('impact force (mN)')
fig5.show()
