# 01 March 2018 Miroslav Gasparek
# Python bootcamp, lesson 27: Hacker statistics

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

rc={'lines.linewidth': 2, 'axes.labelsize': 18, 'axes.titlesize': 18}
sns.set(rc=rc)

# Close previously open figures
plt.close('all')

# Load the data
bd_1975 = np.loadtxt('data/beak_depth_scandens_1975.csv')
bd_2012 = np.loadtxt('data/beak_depth_scandens_2012.csv')

# Define function for calculation of ECDF
def ecdf(data):
    """ Define the function for calculation of ECDF."""
    return np.sort(data), np.arange(1, len(data)+1)/len(data)

# Compute ECDF for 1875 and 2012
x_1975, y_1975 = ecdf(bd_1975)
x_2012, y_2012 = ecdf(bd_2012)

# Plot the ECDFs
fig1 = plt.figure(1)
plt.plot(x_1975, y_1975, marker='.', linestyle='none')
plt.plot(x_2012, y_2012, marker='.', linestyle='none')
plt.margins(0.02)
plt.xlabel('beak depth (mm)')
plt.ylabel('ECDF')
plt.legend(('1975', '2012'), loc='lower right')
fig1.show()

# Compare statistics
mean_1975 = np.mean(bd_1975)
mean_2012 = np.mean(bd_2012)
print('Mean depth in 1975: ', mean_1975)
print('Mean depth in 2012: ', mean_2012)

# Bootstraping samples for 1975 measurement
bs_sample = np.random.choice(bd_1975, replace=True, size=len(bd_1975))

# Compute ECDF of bootstrap sample
x_bs, y_bs = ecdf(bs_sample)

# Plot the ECDFs
fig2 = plt.figure(2)
plt.plot(x_1975, y_1975, marker='.', linestyle='none')
plt.plot(x_bs, y_bs, marker='.', linestyle='none', alpha=0.5)
plt.margins(0.02)
plt.xlabel('beak depth (mm)')
plt.ylabel('ECDF')
plt.legend(('1975', 'bootstrap'), loc='lower right')
fig2.show()

# Compuute bootstrap replicated, i. e. mean of the bootstrap sample
bs_replicate = np.mean(bs_sample)
print(bs_replicate)

# Write a for loop to get lots of bootstrap replicas
# Number of replicas
n_reps = 100000
# Initialize bootstrap replicas array
bs_replicates_1975 = np.empty(n_reps)

# Compute replicates
for i in range(n_reps):
    bs_sample = np.random.choice(bd_1975, size=len(bd_1975))
    bs_replicates_1975[i] = np.mean(bs_sample)

# Plot the histogram of the replicas
fig3 = plt.figure(3)
_ = plt.hist(bs_replicates_1975, bins=100, normed=True)
plt.xlabel('mean beak depth (mm)')
plt.ylabel('PDF')
fig3.show()
# Compute 95% confidence interval
conf_int_1975 = np.percentile(bs_replicates_1975, [2.5,97.5])
print('95 confidence interval for 1975 data: ', conf_int_1975)

# Number of replicas
n_reps = 100000
# Initialize bootstrap replicas array
bs_replicates_2012 = np.empty(n_reps)

# Compute replicates
for i in range(n_reps):
    bs_sample = np.random.choice(bd_2012, size=len(bd_2012))
    bs_replicates_2012[i] = np.mean(bs_sample)

# Compute the confidence interval
conf_int_2012 = np.percentile(bs_replicates_2012, [2.5, 97.5])
print('95 confidence interval for 2012 data: ', conf_int_2012)

# Equivalence of bootstrap samples and standard error of the mean
bs_sem = np.std(bs_replicates_1975)
print('\n',bs_sem)

# Computing the bootstrap confidence interval of the standard deviation
# Number of replicas
n_reps = 100000

# Initialize bootstrap replicas array
bs_replicates_1975 = np.empty(n_reps)

# Compute replicates
for i in range(n_reps):
    bs_sample = np.random.choice(bd_1975, size=len(bd_1975))
    bs_replicates_1975[i] = np.std(bs_sample)

# Compute confidence interval
conf_int_1975 = np.percentile(bs_replicates_1975, [2.5, 97.5])
print(conf_int_1975)

# Plot histogram
fig4 = plt.figure(4)
_ = plt.hist(bs_replicates_1975, bins=100, normed=True)
plt.xlabel('std. dev. beak depth (mm)')
plt.ylabel('PDF')
fig4.show()
