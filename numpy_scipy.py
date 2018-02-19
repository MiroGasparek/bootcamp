# 19 February 2018 Miroslav Gasparek
# Exercises on Python: Introduction to NumPy and SciPy stack

# NumPy, the engine of scientific computing
import numpy as np
# We'll demo a couple SciPy modules
import scipy.special

# Central object for Numpy and SciPy is the ndarray, reffered as NumPy array

# Create a NumPy array from a list
my_ar = np.array([1,2,3,4])
# Look at it 
my_ar 
# Convert the datatype of array
my_ar = my_ar.astype(float)

# Couple of things
print(my_ar.max())
print(my_ar.min())
print(my_ar.sum())
print(my_ar.mean())
print(my_ar.std())
print()

# NumPy arrays can be argments to NumPy functions
print(my_ar.max())
print(my_ar.min())
print(my_ar.sum())
print(my_ar.mean())
print(my_ar.std())

# Other ways to make NumPy arrays
# How long our arrays will be
n = 10
# Make a NumPy array of length n filled with zeros
print(np.zeros(n))
# Make a NumPy array of length n filled with ones
np.ones(n)
# Make an empty NumPy array of length n without initializing entries
# (while it initially holds whatever values were previously in the memory
# locations assigned, zeros will be displayed)
np.empty(n)
# Make a NumPy array filled with zeros the same shape as another NumPy array
my_ar = np.array([[1,2],[3,4]])
print(np.zeros_like(my_ar))

my_ar = np.array([1,2,3,4])
# Exponential
exponential = np.exp(my_ar)
print(exponential)
# Cosine
cosine = np.cos(my_ar)
print(cosine)
# Square root
square_root = np.sqrt(my_ar)

# Matrix operations
dot_product = np.dot(my_ar, my_ar)
print(dot_product)

# Other useful attributes
print(np.pi)

# Using special functions in scipy
print(scipy.special.erf(my_ar))
# Numpy and scipy are fast.

# Make array of 10,000 random numbers
x = np.random.random(10000)

# Time-testing can be done using function '%timeit'
