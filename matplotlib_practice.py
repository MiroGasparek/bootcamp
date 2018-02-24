# 24 February 2018 Miroslav Gasparek
# More plotting with Matplotlib - Python tutorial

import numpy as np
import scipy.special

# This is how we import the module of Matplotlib we will be using
import matplotlib.pyplot as plt

# Some pretty Seaborn settings 
import seaborn as sns
rc={'lines.linewidth': 2, 'axes.labelsize': 18, 'axes.titlesize': 18}
sns.set(rc=rc)

# The x-values we want
x = np.linspace(-15, 15, 400)
# The normalized intensity
norm_I = 4*(scipy.special.j1(x) / x)**2

# Plot the graph
# plt.plot(x, norm_I)
# plt.margins(0.02)
# plt.xlabel('$x$')
# plt.ylabel('$I(x)/I_0$')

# Load in data set
data = np.loadtxt('data/retina_spikes.csv', skiprows=2, delimiter=',')
# Slice out time and voltage
t = data[:,0]
V = data[:,1]

plt.plot(t,V)
plt.xlabel('t (ms)')
plt.ylabel('V (µV)')
# Set x-axis limits
plt.xlim(1395, 1400)
