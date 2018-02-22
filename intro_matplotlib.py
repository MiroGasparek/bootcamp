# 22 February 2018 Miroslav Gasparek
# Introduction to Matplotlib: plotting a histogram

import numpy as np

# This is how we import the module Matplotlib we will be using
import matplotlib.pyplot as plt

# We will use Seaborn styling to make plots look nicer
# Comment out for demonstration later in the session
import seaborn as sns
sns.set()

# This is specific Jupyter notebook
# %matplotlib inline
# %config InlineBackend.figure_formats = {'png', 'retina'}

# In our terminal we do 
# %matplotlib

# JB's favorite Seaborn settings for notebooks
rc={'lines.linewidth': 2, 'axes.labelsize': 18, 'axes.titlesize': 18}
sns.set(rc=rc)

# Making a histogram
# Load in data
xa_high = np.loadtxt('data/xa_high_food.csv',comments='#')
xa_low = np.loadtxt('data/xa_low_food.csv',comments='#')


# Make bin boundaries, reset bins
bins = np.arange(1600, 2501, 50)

# Generate the histogram for low-density fed mother
# Underscore is just dummy variable
# _ = plt.hist((xa_low, xa_high), bins=bins)

# Other way to do it for two histograms
_ = plt.hist(xa_low, normed=True, bins=bins, histtype='stepfilled', alpha=0.5)
_ = plt.hist(xa_high, normed=True, bins=bins, histtype='stepfilled', alpha=0.5)

# Add axis labels
# Dollar sign to invoke LaTeX
plt.xlabel('Cross-sectional area (µm$^2$)', fontsize=18)
plt.ylabel('Count', fontsize=18)
# Add a legend
plt.legend(('low','high'), loc='upper right')
# You need this if you did not use %matplotlib in IPython shell
# plt.show()

# Save figure into file 'fig.pdf' in PDF format
plt.savefig('fig.pdf')
# Save figure in SVG format
plt.savefig('fig.svg')