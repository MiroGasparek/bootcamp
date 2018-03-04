# 26 February 2018 Miroslav Gasparek
# The useful functions written over the course of the Python bootcamp
import numpy as np
import matplotlib.pyplot as plt

# Some pretty Seaborn settings
import seaborn as sns
rc={'lines.linewidth': 2, 'axes.labelsize': 18, 'axes.titlesize': 18}
sns.set(rc=rc)


def ecdf(data):
    """ Function that computes empirical cumulative distribution function of data."""
    # Get x data (sort out data)
    x = np.sort(data)
    # Get y data (compute from x)
    y = np.arange(1, len(data)+1)/len(data)
    return x,y

# Function to draw bootstrap replicates
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
