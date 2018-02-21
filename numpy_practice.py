# 21 February 2018 Miroslav Gasparek
# Practice with NumPy

import numpy as np

# Practice 1
# Generate array of 0 to 10
my_ar1 = np.arange(0,11,dtype='float')
print(my_ar1)

my_ar2 = np.linspace(0,10,11,dtype='float')
print(my_ar2)

# Practice 2
# Load in data
xa_high = np.loadtxt('data/xa_high_food.csv',comments='#')
xa_low = np.loadtxt('data/xa_low_food.csv',comments='#')

def xa_to_diameter(xa):
    """ Convert an array of cross-sectional areas to diameters with
    commensurate units."""

    # Compute diameter from area
    diameter = np.sqrt((4*xa)/np.pi)

    return diameter

# Practice 3
# Create matrix A
A = np.array([[6.7, 1.3, 0.6, 0.7],
              [0.1, 5.5, 0.4, 2.4],
              [1.1, 0.8, 4.5, 1.7],
              [0.0, 1.5, 3.4, 7.5]])

# Create vector b
b = np.array([1.1, 2.3, 3.3, 3.9])

# 1. Print row 1 (remember, indexing starts at zero) of A.
print(A[0,:])
# 2. Print columns 1 and 3 of A.
print(A[:,(0,2)])
# 3. Print the values of every entry in A that is greater than 2.
print(A[A > 2])
# 4. Print the diagonal of A. using the np.diag() function.
print(np.diag(A))

# 1. First, we'll solve the linear system  A⋅x=bA⋅x=b .
# Try it out: use np.linalg.solve().
# Store your answer in the Numpy array x.
x = np.linalg.solve(A,b)
print('Solution of A*x = b is x = ',x)
# 2. Now do np.dot(A, x) to verify that  A⋅x=bA⋅x=b .
b1 = np.dot(A,x)
print(np.isclose(b1,b))
# 3. Use np.transpose() to compute the transpose of A.
AT = np.transpose(A)
print('Transpose of A is AT = \n',AT)
# 4. Use np.linalg.inv() to compute the inverse of A.
AInv = np.linalg.inv(A)
print('Inverse of A is AInv = \n',AInv)


# 1. See what happens when you do B = np.ravel(A).
B = np.ravel(A)
print(B)
# 2. Look of the documentation for np.reshape(). Then, reshape B to make it look like A again.
C  = B.reshape((4,4))
print(C)
