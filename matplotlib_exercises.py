# 26 February 2018 Miroslav Gasparek
# More practice in Python with Matplotlib

# Import modules
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats
# Import bootcamp_utils()
import bootcamp_utils

# Some pretty Seaborn settings 
import seaborn as sns
rc={'lines.linewidth': 2, 'axes.labelsize': 18, 'axes.titlesize': 18}
sns.set(rc=rc)

## Exercise 1 - toggle switch

# Load genetic toggle switch data
data = np.loadtxt('data/collins_switch.csv', delimiter=',', skiprows=2)
# Slice out the data for IPTG and GFP
iptg = data[:,0]
gfp = data[:,1]
# Plot the graph with semi-logarithmic axis
# plt.semilogx(iptg,gfp, marker='.', markersize='15', linestyle='none')
# plt.xlabel('[IPTG] (nM)')
# plt.ylabel('normalized GFP intensity')
# 
# # Display the figure
# plt.show()

## Exercise 2 - toggle switch with error bars

# Slice out the error bars
sem = data[:,2]

# Create the plot with error bars
# plt.errorbar(iptg,gfp,yerr=sem,xerr=None, marker='.', markersize='10', linestyle='none')
# plt.xlabel('[IPTG] (nM)')
# plt.ylabel('normalized GFP intensity')
# plt.xscale('log')
# plt.show()

# Exercise 3 - Computing and plotting a ECDFs

# 1. Function to compute ECDF
# def ecdf(data):
#     """ Function that computes empirical cumulative distribution function of data."""
#     # Get x data (sort out data)
#     x = np.sort(data)
#     # Get y data (compute from x)
#     y = np.arange(1, len(data)+1)/len(data)
#     return x,y
# # 2. Load in the data sets
# xa_high = np.loadtxt('data/xa_high_food.csv', comments='#')
# xa_low = np.loadtxt('data/xa_low_food.csv', comments='#')
# 
# # 3. Generate x and y values for the ECDFs for these data sets
# x_high, y_high = ecdf(xa_high)
# x_low, y_low = ecdf(xa_low)

# Plot the ECDFs
# plt.plot(x_high,y_high, marker='.', linestyle='none')
# plt.plot(x_low,y_low, marker='.', linestyle='none')
# plt.margins(0.02)
# plt.legend(('high food', 'low food'), loc = 'lower right')
# plt.xlabel('egg cross sectional area (sq. µm)')
# plt.ylabel('ECDF')
# plt.show()    

# Exercise 4 - Creation of bootcamp_utils.py file
# Plot results

# Exercise 5 - Normal distribution verification of DCDF

# 1. Generate ECDFs
# Get x and y data
xa_high = np.loadtxt('data/xa_high_food.csv', comments='#')
xa_low = np.loadtxt('data/xa_low_food.csv', comments='#')
# Generate x and y values for the ECDFs for these data sets
x_high, y_high = bootcamp_utils.ecdf(xa_high)
x_low, y_low = bootcamp_utils.ecdf(xa_low)

# 2. Plot ECDFs
plt.plot(x_high, y_high, marker='.', linestyle='none')
plt.plot(x_low, y_low, marker='.', linestyle='none')
plt.margins(0.02)
plt.legend(('high food', 'low food'), loc='lower right')
plt.xlabel('egg cross sectional area (sq. µm)')
plt.ylabel('ECDF')

# 3. Make smooth x-values
x = np.linspace(1600, 2500, 400)
cdf_high = scipy.stats.norm.cdf(x, loc=np.mean(xa_high), scale=np.std(xa_high))
cdf_low = scipy.stats.norm.cdf(x, loc=np.mean(xa_low), scale=np.std(xa_low))

# 4. Plot smooth curves in black
plt.plot(x, cdf_high, color='gray')
plt.plot(x, cdf_low, color='gray')

# 5.Label axes and add legent
plt.margins(0.02)
plt.legend(('high food', 'low food'), loc = 'lower right')
plt.xlabel('egg cross sectional area (sq. µm)')
plt.ylabel('ECDF')
plt.title("""Verification of normal distribution
 of the egg cross-section data""")
plt.show()    
