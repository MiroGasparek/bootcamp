# 28 February 2018 Miroslav Gasparek
# Python tutorial on random number generation

import random
import numpy as np

import matplotlib.pyplot as plt
# Some pretty Seaborn settings
import seaborn as sns
rc={'lines.linewidth': 2, 'axes.labelsize': 18, 'axes.titlesize': 18}
sns.set(rc=rc)

# Generate sorted random numbers
x = np.sort(np.random.random(size=100000))
# Generate y-axis for CDF
y = np.arange(1, len(x)+1)/len(x)
# Plot CDF from random numbers (only 100 points for the plotting purposes)
fig1 = plt.figure(1)
plt.plot(x[::1000], y[::1000], marker='.', linestyle='none', markersize=10)
# Plot expected CDF (just a straight line from (0,0) to (1,1) )
plt.plot([0, 1], [0, 1], 'k--')
fig1.show()

# Doing 'coin flips'
# Generate 20 random numbers on uniform interval
# x = np.random.random(size=20)
# # Make them coin flips
# heads = x > 0.5
# # Show which were heads, and count the number of heads
# print(heads)
# print('\nThere were', np.sum(heads), ' heads.')

# Seed the RNG
np.random.seed(42)
# Generate random numbers
rand_ar1 = np.random.random(size=10)

# Re-seed the RNG
np.random.seed(42)
# Generate random numbers
rand_ar2 = np.random.random(size=10)

# Seed with a number that is close to the answer to everything
np.random.seed(43)
rand_ar3 = np.random.random(size=10)

# Set parameters
mu = 10
sigma = 1
# Draw 10000 random samples
x = np.random.normal(mu, sigma, size=10000)
# Plot a histogram of our draws
fig2 = plt.figure(2)
_ = plt.hist(x, bins=100)
fig2.show()

sample_mean = np.mean(x)
sample_std = np.std(x)

# Selections from discrete distributions
# Draw random integers on [0, 4), i. e., exclusive of last one.
rand_ar_int = np.random.randint(0, 4, 20)

# This can be used to generate random DNA sequences
# Key of bases
bases = 'ATGC'
# Draw random numbers for sequence
x = np.random.randint(0, 4, 50)
# Make sequence
seq_list = [None]*50
for i,b in enumerate(x):
    seq_list[i] = bases[b]
# Join the sequence
seq = ''.join(seq_list)

# Choosing elements from an array
# Choose elements from array without replacement
rand_ar4 = np.random.choice(np.arange(51), 20, replace=False)
print(rand_ar4)
# Shuffiling an array
rand_ar5 = np.random.permutation(np.arange(53))
print('\n', rand_ar5)

# Random module
# Make sequence
seq_list = [None]*50
for i in range(len(seq_list)):
    seq_list[i] = random.choice('ATGC')

# Join the sequence
seq2 = ''.join(seq_list)
