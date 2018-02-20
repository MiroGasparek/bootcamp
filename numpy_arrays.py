# 20 February 2018 Miroslav Gasparek
# NumPy Arrays

# Import the engine of scientific computing
import numpy as np

# Load the data without commments
xa_high = np.loadtxt('data/xa_high_food.csv', comments='#')
xa_low = np.loadtxt('data/xa_low_food.csv',comments='#')

# Divide the data array by a scalar (works equivalently for the other operators)
xa_high1 = xa_high/1e6
# Booleans with NumPy arrays and scalars
xa_high_bool = xa_high < 2000
# This cannot be used with if, it has to be used with a.any() or a.all()
print((xa_high > 2000).any())
print((xa_high > 2000).all())

# Never use equality (==) with floats, but we can use np.isclose()
# Compare two numbers
print(np.isclose(1.3,1.29999999))
# Compare an array to scalar
print(np.isclose(xa_high,1800))
# Compare all arrays to a scalar
print(np.allclose(xa_high, 1800))

# Adding arrays - only arrays with the same shape can be added
xa_low_slice = xa_low[:len(xa_high)]
xa_sum = xa_high + xa_low_slice
print(xa_sum)

# Comparing arrays
print(np.isclose(xa_high, xa_low_slice))

# Reversed arrays
xa_high[::-1]
# Every 5th element, starting at index 3
xa_high[3::5]
# Entries 10 to 20
xa_high[10:21]

# Fancy indexing - enables us to slice out specific values
xa_high[[1, 19, 6]]
# We could also ulse a NumPy array
xa_high[np.array([1, 19, 6])]
# Find out position of high values
np.where(xa_high > 2000)

## NumPy arrays are mutable
# Make an array
my_ar = np.array([1,2,3,4])
print(my_ar)
# Change an element
my_ar[2] = 6
# See the result
print(my_ar)

# Attach a new variable
my_ar2 = my_ar
# Set an entry using the new variable
my_ar2[3] = 9
# Does the original change? (yes.)
print(my_ar)

# Lets see how NumPy works with functions
# Re-instantiate my_ar
my_ar = np.array([1,2,3,4]).astype(float)

# Function to normalize x (/= works with mutable objects)
def normalize(x):
    x /= np.sum(x)
# Pass it through a function
normalize(my_ar)
# Is it normalized(yes.)
print(my_ar)
# What happens inside function happens outside function too

# make list and array
my_list = [1,2,3,4]
my_ar = np.array(my_list)
# Slice out of each
my_list_slice = my_list[1:-1]
my_ar_slice = my_ar[1:-1]

# Mess with the slices
my_list_slice[0] = 9
my_ar_slice[0] = 9
# Look at originals
print(my_list)
print(my_ar)
# Slices of NumPy arrays are **views**, not copies.
# Copies can be made using np.copy()
# Make a copy
xa_high_copy = np.copy(xa_high)
# Mess with an entry
xa_high_copy[10] = 2000
# Check equality
print(np.allclose(xa_high, xa_high_copy))

# NumPy arrays can be multidimensional
# New 2D array using the reshape() method
my_ar = xa_high.reshape((11,4))
# Look at it
print(my_ar)
print()

# It is like a list of lists
# Make list of lists
list_of_lists = [[1,2], [3,4]]
print(list_of_lists)
# Pull out value in first row, second column
print(list_of_lists[0][1])
# Arrays are indexed much more conveniently
print(my_ar[0,1])
# Get secod row
print(my_ar[2,:])
# Using boolean indexing
print(np.where(my_ar > 2000))
# fancy indexing
print(my_ar[np.array([0,1,8,10,10]), np.array([1,0,1,0,2])])

# Concatenate Arrays
combined = np.concatenate((xa_high,xa_low))
# Look at it
print(combined)

# Compute 25, 50 and 75 percentiles
high_perc = np.percentile(xa_high,(25,50,75))
low_perc = np.percentile(xa_low,(25,50,75))

# Print result
print("""
        25      median      75
high    {0:d}       {1:d}       {2:d}
low     {3:d}       {4:d}       {5:d}
""".format(*(tuple(high_perc.astype(int)) + tuple(low_perc.astype(int)))))
