# 28 May 2018 Miroslav Gasparek
# Python bootcamp, lesson 37: Performing regressions

# Import modules
import numpy as np
import pandas as pd

# We'll use scipy.optimize.curve_fit to do the nonlinear regression
import scipy.optimize

import matplotlib.pyplot as plt
import seaborn as sns
rc={'lines.linewidth': 2, 'axes.labelsize': 18, 'axes.titlesize': 18}
sns.set(rc=rc)

# Import the dataset
df = pd.read_csv('data/bcd_gradient.csv', comment = '#')

# Rename the columns for the ease of the access
df = df.rename(columns={'fractional distance from anterior': 'x',
'[bcd] (a.u.)' : 'I_bcd'})

# Optimizing function prototype is
# scipy.optimize.curve_fit(f, xdata, ydata, p0=None)

# Step 1. Define the fit function
# (Make sure that all arguments are positive)
def bcd_gradient_model(x, I_0, a, lam):
    """ Model for Bcf gradient: exponential decay plus background"""
    assert np.all(np.array(x) >= 0), 'All values of x must be >= 0.'
    assert np.all(np.array([I_0, a, lam]) >= 0), 'All parameters must be >= 0'

    return a + I_0 * np.exp(-x/lam)

# **Never** name a Python variable the same as a keyword!
# To see what the keywords are, do this: `import keyword; print(keyword.kwlist)`

# Step 2. Supply initial guess
# Otherwise, curve_fit() will guess value of 1 for all parameters,
#which is generally not good
# We can see nonzero background signal around a = 0.2, I_0 around 0.9 and
# lambda somewhere around 0.3 (here I drops to approx. 66%), but lets try 1

# Specify initial guess
I_0_guess = 0.9
a_guess = 0.2
lam_guess = 1.0

# Construct initial guess array
p0 = np.array([I_0_guess, a_guess, lam_guess])

# Do curve fit, but dump covariance into dummy variable
# p, _ = scipy.optimize.curve_fit(bcd_gradient_model, df['x'], df['I_bcd'], p0=p0)

# This does not work due to the possiblity of getting negative values of parameters
# when _.curve_fit() searches the parameter space.
# Possible solutions:
# 1. Take out error checking
# 2. Use something other than scipy.optimize.curve_fit()
# 3. Adjust the theoretical function by using the log of parameter values instead
# of parameter values themselves - lets do that

def bcd_gradient_model_log_params(x, log_I_0, log_a, log_lam):
    """ Model for Bcf gradueint: exponential decay plus background
    with log parameters.
    """

    # Exponentiate parameters
    I_0, a, lam = np.exp(np.array([log_I_0, log_a, log_lam]))

    return bcd_gradient_model(x, I_0, a, lam)

# Construct initial guess array
log_p0 = np.log(p0)

# Do curve fit but dump covariance into dummy variable
log_p, _ = scipy.optimize.curve_fit(bcd_gradient_model_log_params,
                                    df['x'], df['I_bcd'], p0=log_p0)

# Get the optimal parameter values
p = np.exp(log_p)

# Print the results
print("""
    I_0 = {0:.2f}
    a = {1:.2f}
    λ = {2:.2f}
    """.format(*tuple(p)))

# Plotting
# Smooth x vales (100 values between zero and one)
x_smooth = np.linspace(0, 1, 100)
# Compute smooth curve
I_smooth = bcd_gradient_model(x_smooth, *tuple(p))

# Plot everything together
plt.plot(x_smooth, I_smooth, marker='None', linestyle='-', color='gray')
plt.plot(df['x'], df['I_bcd'], marker='.', linestyle='None')

# Label axes
plt.xlabel('$x$')
plt.ylabel('$I$ (a.u.)')

# The length scale of the Bcd gradient is about 20% of the embryo length.
