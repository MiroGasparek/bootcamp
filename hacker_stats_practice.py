# 02 March 2018 Miroslav Gasparek
# Python bootcamp, lesson 28: Practice with hacker stats

# Import modules
import numpy as np
import matplotlib.pyplot as plt

# Some pretty Seaborn settings
import seaborn as sns
rc={'lines.linewidth': 2, 'axes.labelsize': 18, 'axes.titlesize': 18}
sns.set(rc=rc)

# Practice 1: Function to draw bootstrap replicates
def draw_bs_reps(data, func, size=1):
    """ Function that takes in an array and returns statistics:
    - data: array of data
    - func: function, such as numpy.mean(), numpy.std(), etc.
    - size: number of replicates to generate
    """
    # Length of the input data array
    n = len(data)
    # Initialize the empty array of replicates
    reps = np.empty(size)
    # For loop for drawing a bootstrap sample and applying the func to the array
    for i in range(size):
        # Generate bootstrap sample
        bs_sample = np.random.choice(data, n)
        # Compute replicate
        reps[i] = func(bs_sample)
        
    return reps

# # Try the function on the beak depth data 
# bd_1975 = np.loadtxt('data/beak_depth_scandens_1975.csv')
# # Compute replicates
# bs_replicates = draw_bs_reps(bd_1975, np.mean, size=100000)
# # 95% confidence interval
# print(np.percentile(bs_replicates, [2.5, 97.5]))

# Practice 2: Plot ECDF of bootstrap samples

# Define ECDF function so that we have it
def ecdf(data):
    """ Returns the ECDF of the data."""
    return np.sort(data), np.arange(1, len(data)+1)/len(data)


# Load in the data
bd_1975 = np.loadtxt('data/beak_depth_scandens_1975.csv')

# Generate the x,y values for the plot
x,y = ecdf(bd_1975)
# Plot the data
fig1 = plt.figure(1)
plt.plot(x,y, marker='.', markersize='10', linestyle='none', color='blue')
plt.margins(0.02)
plt.xlabel('beak depth (mm)')
plt.ylabel('ECDF')
fig1.show()

# For loop for generation of bootstrap samples from the data set
n_it = 100

# Define figure
fig2 = plt.figure(2)

# Define a for loop
for i in range(n_it):
    # Generate a bootstrap sample
    bs_sample = np.random.choice(bd_1975, len(bd_1975))
    # Compute x and y values for the ECDF of the bootstrap sample
    x, y = ecdf(bs_sample)
    # Plot the data on the same plot
    plt.plot(x,y, marker='.', markersize='10', linestyle='none', color='blue', alpha=0.01)

# Label axes and set margins
plt.xlabel('beak depth (mm)')
plt.ylabel('ECDF')
plt.margins(0.02)
fig2.show()