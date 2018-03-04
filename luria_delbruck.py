# 03 March 2018 Miroslav Gasparek
# Python bootcamp, lesson 29: Luria-Delbruck distribution

# Import modules
import numpy as np

import matplotlib.pyplot as plt
import seaborn as sns
rc={'lines.linewidth': 2, 'axes.labelsize': 18, 'axes.titlesize': 18}
sns.set(rc=rc)

# Adaptive mutation hypothesis
# Specification of parameters
n_gen = 16
r = 1e-5
# Total number of cells
n_cells = 2**(n_gen-1)
# Draw 100000 binomial samples
ai_samples = np.random.binomial(n_cells, r, 100000)
print("""
Adaptive immunity hypothesis
----------------------------
mean:        {mean:.4f}
variance:    {var:.4f}
Fano factor: {fano:.4f}
""".format(mean=np.mean(ai_samples), var=np.var(ai_samples),
           fano=np.var(ai_samples) / np.mean(ai_samples)))

# Plot histogram, but it is a probability density function, so
# no need for bins
fig1 = plt.figure(1)
plt.plot(np.bincount(ai_samples) / len (ai_samples), marker='.', markersize=10, linestyle='none')
plt.xlabel('Number of survivors')
plt.ylabel('Probability')
plt.xticks(np.arange(ai_samples.max()+1))
plt.margins(0.02)
fig1.show()

# Random mutation hypothesis
def draw_random_mutation(n_gen, r):
    """ Draw a sample out of the Luria-Delbruck distribution."""
    # Initialize number of mutants
    n_mut = 0

    for g in range (n_gen):
        n_mut = 2 * n_mut + np.random.binomial(2**g - 2 * n_mut, r)

    return n_mut

def sample_random_mutation(n_gen, r, n_samples):
    """ Sample out of the Luria-Delbruck distribution."""
    # Initialize samples
    samples = np.empty(n_samples)

    # Draw the samples
    for i in range(n_samples):
        samples[i] = draw_random_mutation(n_gen, r)

    return samples

rm_samples = sample_random_mutation(n_gen, r, 100000).astype(int)
print("""
Random mutation hypothesis
--------------------------
mean:        {mean:.4f}
variance:    {var:.4f}
Fano factor: {fano:.4f}
""".format(mean=np.mean(rm_samples), var=np.var(rm_samples),
           fano=np.var(rm_samples) / np.mean(rm_samples)))

# Plot histogram, but it's a probability mass function, so no need for bins
fig2 = plt.figure(2)
plt.semilogx(np.bincount(rm_samples.astype(int)) / len(rm_samples),
             marker='.', markersize=10, linestyle='None')

plt.xlabel('Number of survivors')
plt.ylabel('Probability')
plt.margins(0.02)
fig2.show()

# Sort the samples
rm_samples = np.sort(rm_samples)
# Generate y-axis for CDF
y = np.arange(1, len(rm_samples)+1)/len(rm_samples)
# Plot CDF from random numbers
fig3 = plt.figure(3)
plt.semilogx(rm_samples, y, '.', markersize=10)
t_smoorth = np.logspace(0.5, 8, 100)
# Clean up plot
plt.margins(y=0.02)
plt.xlabel(r'$t_{bt} (s)$')
plt.ylabel('cum.hist.')
# Clean up plot
plt.margins(y=0.02)
plt.xlabel('number of survivors')
plt.ylabel('CDF')
fig3.show()
