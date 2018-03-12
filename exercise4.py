# 12 March 2018 Miroslav Gasparek
# Python bootcamp, exercise 4: Practice with Pandas

# Import modules
import glob
import re

import numpy as np
import pandas as pd
import numba

# This is how we import the module of Matplotlib we'll be using
import matplotlib.pyplot as plt

# Some pretty Seaborn settings
import seaborn as sns
rc={'lines.linewidth': 2, 'axes.labelsize': 18, 'axes.titlesize': 18}
sns.set(rc=rc)

# Close figures
plt.close('all')
# 
# # Exercise 4.1
# # a) Get list of CSV files
# csv_list = glob.glob('data/grant*.csv')
# # Initialize list of DataFrames
# df_list = []
# # Load in each sequentially.
# for csv_file in csv_list:
#     # Read in DataFrame
#     df = pd.read_csv(csv_file, comment='#')
#     # Place in list
#     df_list.append(df)
# 
# # b) Initialize years
# years = []
# for csv_file in csv_list:
#     years.append(int(csv_file[-8:-4]))
# 
# # Rename 'yearband' to 'year'
# df_list[0] = df_list[0].rename(columns={'yearband': 'year'})
# # No worries about Y2K
# df_list[0]['year'] += 1900
# 
# for i, df in enumerate(df_list):
#     df_list[i]['year'] = np.ones(len(df), dtype=int)*years[i]
# 
# # Change the names of each column for each DataFrame
# # Select a DataFrame
# df = df_list[3]
# # See which column had 'len' in it and extract it
# df.columns[df.columns.str.contains('len')]
# 
# # Define a renaming function
# def rename_cols(df):
#     """ Rename columns so that all DataFrames have same column headings."""
#     # Sniff out the key names from names that are close
#     band_key = df.columns[df.columns.str.contains('and')][0]
#     species_key = df.columns[df.columns.str.contains('ecies')][0]
#     length_key = df.columns[df.columns.str.contains('len')][0]
#     depth_key = df.columns[df.columns.str.contains('dep')][0]
#     year_key = df.columns[df.columns.str.contains('year')][0]
#     
#     # Rename the columns using renaming dictionary
#     return df.rename(columns={  band_key: 'band',
#                                 species_key: 'species',
#                                 depth_key: 'beak depth (mm)',
#                                 length_key: 'beak length (mm)',
#                                 year_key: 'year'})
#                                 
# # Loop through the DataFrames and rename the columns
# for i, df in enumerate(df_list):
#     df_list[i] = rename_cols(df)
# 
# # Do the concatenation
# df = pd.concat(df_list, axis=0, ignore_index=True)
# 
# # c) Drop the duplicated bird numberrs
# # Stats about how many birds were measured more than once
# # print(  'There were', len(df['band'][df['band'].duplicated()].unique()), 
# #         'birds that were measured more than once.')
# # print('There were', len(df['band'].unique()), 'total birds measured.')
# 
# # Drop all rows with matching year and band (keep first)
# df = df.drop_duplicates(subset=['year', 'band'])
# 
# # Save DataFrame as a CSV file
# df.to_csv('data/final_grant_complete.csv', index=False)
# 
# # d) Plot the ECDF of the beak depths
# # Define ECDF function
# def ecdf(data):
#     """ Computes the ECDF of input data"""
#     return np.sort(data), np.arange(1,len(data) + 1) / len(data)
# # Pull out data for ECDF plotting
# # Beak depth
# bd_fortis = \
# bd_fortis = df.loc[(df['species']=='fortis') & (df['year']==1987), 'beak depth (mm)']
# bd_scandens = \
# bd_scandens = df.loc[(df['species']=='scandens') & (df['year']==1987), 'beak depth (mm)']
# # Beak length
# bl_fortis = \
# bl_fortis = df.loc[(df['species']=='fortis') & (df['year']==1987), 'beak length (mm)']
# bl_scandens = \
# bl_scandens = df.loc[(df['species']=='scandens') & (df['year']==1987), 'beak length (mm)']
# 
# # Plot the results
# fig1, ax = plt.subplots(2, 1, figsize=(8, 5))
# 
# # Plot beak depth ECDFs
# x, y = ecdf(bd_fortis)
# ax[0].plot(x, y, marker='.', linestyle='none')
# x, y = ecdf(bd_scandens)
# ax[0].plot(x, y, marker='.', linestyle='none')
# ax[0].margins(0.02)
# 
# # Plot beak length ECDFs
# x, y = ecdf(bl_fortis)
# ax[1].plot(x, y, marker='.', linestyle='none')
# x, y = ecdf(bl_scandens)
# ax[1].plot(x, y, marker='.', linestyle='none')
# ax[1].margins(0.02)
# 
# # Legends and axis labels, tidying
# ax[0].legend(('fortis', 'scandens'), loc='lower right')
# ax[0].set_xlabel('beak depth (mm)')
# ax[0].set_ylabel('ECDF')
# ax[1].set_xlabel('beak length (mm)')
# ax[1].set_ylabel('ECDF')
# fig1.tight_layout(h_pad=3)
# # fig1.show()
# 
# # e) Beak depth vs beak length
# # Extract data
# bd_fortis = df.loc[(df['species']=='fortis') & (df['year']==1987), 'beak depth (mm)']
# bd_scandens = df.loc[(df['species']=='scandens') & (df['year']==1987), 'beak depth (mm)']
# 
# bl_fortis = df.loc[(df['species']=='fortis') & (df['year']==1987), 'beak length (mm)']
# bl_scandens = df.loc[(df['species']=='scandens') & (df['year']==1987), 'beak length (mm)']
# # Plot beak depth vs. beak length
# fig2 = plt.figure(2)
# plt.plot(bl_fortis, bd_fortis, marker='.', color='blue', linestyle='none', alpha=0.5)
# plt.plot(bl_scandens, bd_scandens, marker='.', color='red', linestyle='none', alpha=0.5)
# plt.xlabel('beak length (mm)')
# plt.ylabel('beak depth (mm)')
# plt.margins(0.02)
# plt.legend(('Fortis','Scandens'),loc='lower right')
# # fig2.show()
# 
# # f) Repetition of the measurement for all the beaks.
# def plot_beak_data(ax, df, year, legend=False):
#     """ Plot beak length and beak depth data for a given year on a given axis. """
#     # Extract data we want
#     df_fortis = df[(df['year']==year) & (df['species']=='fortis')]
#     df_scandens = df[(df['year']==year) & (df['species']=='scandens')]
#     
#     # Plot the result
#     ax.plot(df_fortis['beak length (mm)'], df_fortis['beak depth (mm)'], 
#             marker='.', linestyle='none', alpha=0.5)
#     ax.plot(df_scandens['beak length (mm)'], df_scandens['beak depth (mm)'],
#             marker='.', linestyle='none', alpha=0.5)
# 
#     # Clean up
#     ax.margins(0.02)
#     ax.set_xlabel('beak length (mm)', fontsize=12)
#     ax.set_ylabel('beak depth (mm)', fontsize=12)
#     ax.set_title(str(year), fontsize=14)
#     if legend:
#         ax.legend(('fortis', 'scandens'), loc='upper left')
#         
#     return ax
# 
# # Plots layout
# fig3, ax = plt.subplots(2, 3, figsize=(8, 5), sharex=True, sharey=True)
# # Which axes to use
# ax_inds = ((0,0), (0,1), (0,2), (1,0), (1,1))
# 
# # Loop through years and make plots
# for i, year in enumerate(years):
#     if i == 0:
#         legend = True
#     else:
#         legend=False
#     _ = plot_beak_data(ax[ax_inds[i]], df, year, legend=legend)
# 
# # Tidy up
# ax[1, 2].axis('off')
# fig3.tight_layout()
# # fig3.show()
# 
# ###############
# # Exercise 4.2
# # a) Load the drone weight data in as a Pandas DataFrame
# df_weight = pd.read_csv('data/bee_weight.csv', comment='#')
# # b) plot ecdf of the weight data for control and pesticide
# df_control = df_weight.loc[df_weight['Treatment']=='Control', ('Weight')]
# df_pesticide = df_weight.loc[df_weight['Treatment']=='Pesticide', ('Weight')]
# 
# # Plot the ECDFs
# fig4 = plt.figure(4)
# 
# x_c, y_c = ecdf(df_control)
# plt.plot(x_c, y_c, marker='.', color='red', linestyle='none', alpha=0.5)
# x_p, y_p = ecdf(df_pesticide)
# plt.plot(x_p, y_p, marker='.', color='blue', linestyle='none', alpha=0.5)
# plt.xlabel('Weight (mg)')
# plt.ylabel('ECDF')
# plt.legend(('Control','Pesticide'), loc='lower right')
# plt.margins(0.02)
# fig4.show()
# 
# # c) Compute the mean drone weight for control and pesticide groups
# # Get data
# mean_control = np.mean(df_weight.loc[df_weight['Treatment']=='Control', 'Weight'])
# mean_pest = np.mean(df_weight.loc[df_weight['Treatment']=='Pesticide','Weight'])
# # Print means
# print('Mean control: ', mean_control, 'mg')
# print('Mean pesticide: ', mean_pest, 'mg')
# # Means are close, so we use boootstrapping 
# # Define replicate generating function
# def draw_bs_reps(data, func, size=1):
#     """ Draw bootstrap replicates from a data set."""
#     n = len(data)
#     
#     # Initialize array of replicates
#     reps = np.empty(size)
#     
#     for i in range(size):
#         # Generate bootstrap sample
#         bs_sample = np.random.choice(data, n)
#         # Compute replicate
#         reps[i] = func(bs_sample)
#     
#     return reps
# 
# # Draw 100 000 bootstrap reps for both.
# bs_reps_control = draw_bs_reps(
#         df_weight.loc[df_weight['Treatment']=='Control', 'Weight'], np.mean, size=100000)
# bs_reps_pest = draw_bs_reps(
#         df_weight.loc[df_weight['Treatment']=='Pesticide', 'Weight'], np.mean, size=100000)
# 
# conf_int_control = np.percentile(bs_reps_control, [2.5, 97.5])
# conf_int_pest = np.percentile(bs_reps_pest, [2.5, 97.5])
# # print('Confidence interval for weight of control group:', conf_int_control)
# # print('Confidence interval for weight of pesticide group:', conf_int_pest)
# 
# # d) Repeat the previous measurements with drone sperm
# # Load the drone sperm data
# df_sperm = pd.read_csv('data/bee_sperm.csv', comment='#')
# df_sperm_control = df_sperm.loc[df_sperm['Treatment']=='Control', 'Quality']
# df_sperm_pesticide = df_sperm.loc[df_sperm['Treatment']=='Pesticide', 'Quality']
# # Plot the ECDF of the data
# fig5 = plt.figure(5)
# (x_sperm_c, y_sperm_c) = ecdf(df_sperm_control)
# plt.plot(x_sperm_c, y_sperm_c, marker='.', color='red', linestyle='none', alpha=0.5)
# (x_sperm_p, y_sperm_p) = ecdf(df_sperm_pesticide)
# plt.plot(x_sperm_p, y_sperm_p, marker='.', color='blue', linestyle='none', alpha=0.5)
# plt.xlabel('sperm quality')
# plt.ylabel('ECDF')
# plt.legend(('Control','Pesticide'), loc='lower right')
# plt.margins(0.02)
# fig5.show()
# 
# # Calculate the means
# mean_sperm_control = np.mean(df_sperm.loc[df_sperm['Treatment']=='Control', 'Quality'])
# mean_sperm_pest = np.mean(df_sperm.loc[df_sperm['Treatment']=='Pesticide','Quality'])
# # Print means
# print('Mean control: ', mean_sperm_control, 'mg')
# print('Mean pesticide: ', mean_sperm_pest, 'mg')
# 
# # Get the bootstrap samples
# # Draw 100 000 bootstrap reps for both.
# bs_reps_control = draw_bs_reps(
#         df_sperm.loc[df_sperm['Treatment']=='Control', 'Quality'].dropna(), np.mean, size=100000)
# bs_reps_pest = draw_bs_reps(
#         df_sperm.loc[df_sperm['Treatment']=='Pesticide', 'Quality'].dropna(), np.mean, size=100000)
# 
# conf_int_control = np.percentile(bs_reps_control, [2.5, 97.5])
# conf_int_pest = np.percentile(bs_reps_pest, [2.5, 97.5])
# print('Confidence interval for sperm of control group:', conf_int_control)
# print('Confidence interval for sperm of pesticide group:', conf_int_pest)
# 
# 
# # Draw 100,000 bootstrap reps for both for median
# bs_reps_control = draw_bs_reps(
#         df_sperm.loc[df_sperm['Treatment']=='Control', 'Quality'].dropna(),
#         np.median,size=100000)
# bs_reps_pest = draw_bs_reps(
#         df_sperm.loc[df_sperm['Treatment']=='Pesticide', 'Quality'].dropna(),
#         np.median, size=100000)
# 
# # Compute and print confidence interval for median
# conf_int_control = np.percentile(bs_reps_control, [2.5, 97.5])
# conf_int_pest = np.percentile(bs_reps_pest, [2.5, 97.5])
# 
# print('Confidence interval for median sperm of control group:', conf_int_control)
# print('Confidence interval for median sperm of pesticide group:', conf_int_pest)

############
# Exercise 4.3: Monte Carlo simulation of transcriptional pausing

def ecdf(data):
    """ Computes the ECDF of input data"""
    return np.sort(data), np.arange(1,len(data) + 1) / len(data)

# a)
# We use @Numba to speed up the calculations
@numba.jit(nopython=True)
def backtrack_steps():
    """ 
    Computes the number of steps it takes for a random walker to get from x = 0 to x = 1.
    """
    # Initialize the position
    x = 0
    # Initialize the number of steps
    n_steps = 0
    #
    # Walk until we get to positive 1
    while x < 1:
        x += 2*np.random.randint(0, 2) - 1
        n_steps += 1
    
    return n_steps

# b) Generate 10 000 backtracks

# Initialize the total time
tau = 0.5 # seconds

# Number of samples
n_samples = 10000

# Define empty array of times
t_bt = np.empty(n_samples)

# Generate the samples
for i in range(n_samples):
    t_bt[i] = backtrack_steps()

# Convert to seconds
t_bt *= tau

# c) Plot histogram of backtrack times
fig6 = plt.figure(6)
_ = plt.hist(t_bt, bins=100, normed=True)
plt.xlabel('time (s)')
plt.ylabel('PDF')
fig6.show()

# d) Plot ECDF of samples
x, y = ecdf(t_bt)

fig7 = plt.figure(7)
plt.semilogx(x, y, marker='.', linestyle='none', alpha=0.5)
plt.xlabel('time(s)')
plt.ylabel('ECDF')
plt.margins(0.02)
fig7.show()

# e) 
# Plot the CCDF
fig8 = plt.figure(8)
plt.loglog(x, 1 - y, '.')
# Plot the asymptotic power law
t_smooth = np.logspace(0.5, 8, 100)
plt.loglog(t_smooth, 1/np.sqrt(t_smooth))

# Label axes
plt.xlabel('time (s)')
plt.ylabel('CCDF')
fig8.show()