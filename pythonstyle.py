# 16 February 2018 Miroslav Gasparek
# Python Style

import numpy as np

# Key points of PEP:
# Variable names need to be descriptive.

# Variable names are all lower case with underscores separating words.

# Do not name variables 1, 0 or I because they are hard to distinguish from
# ones and zeros.

# Function naems are lower case and may use underscores.

# Class names are in CamelCase.

# Module names are short and lower case. Underscores should be avoided unless
# necessary for readability.

# Lines are maximally 79 characters long.

# Doc strings are maximally 72 characters long.

# Avoid in-line comments; put comment directly above he code.

# Avoid excessive comments that state the obvious.

# Generally, put single spaces around binary operators, unelss omitting space
# improves readability. For exmaple, x**2  + y**2. Low precedence operators
# should have space.

# Assignment operators should aways have single spaces around the except when
# in keyword arugments E.g., no space in f(x, y=4)

# Put spaces after commas in function definitions and calls. This also applies
# for lists, tuples, NumPy arrays, etc.

# Avoid excessive spaces within parentheses, braces, and brackets.

# Use a single blank line to seaprate logical sections of your code.

# Put two blank lines between functions in a .py file.

# Put all import statements at the top of the file, importing from
# one module per line.

# Code without PEP 8
seq='AUCUGUACUAAUGCUCAGCACGACGUACG'
c='AUG'  # This is the start codon
i =0  # Initialize sequence index
while seq[ i : i + 3 ]!=c:
    i+=1

print('The start codon starts at index', i)

# Code with PEP 8

start_codon = 'AUG'

# Initiailize sequence index for while loop
i = 0

# Scan sequence until we hit the start codon
while seq[i:i+3] != start_codon:
    i += 1

print('The start codon starts at index', i)

# PEP 8 version of amino acids dictionary
aa = {'A': 'Ala',
      'R': 'Arg',
      'N': 'Asn',
      'D': 'Asp',
      'C': 'Cys',
      'Q': 'Gln',
      'E': 'Glu',
      'G': 'Gly',
      'H': 'His',
      'I': 'Ile',
      'L': 'Leu',
      'K': 'Lys',
      'M': 'Met',
      'F': 'Phe',
      'P': 'Pro',
      'S': 'Ser',
      'T': 'Thr',
      'W': 'Trp',
      'Y': 'Tyr',
      'V': 'Val'}

# Quadradic formula
def quadradic_roots(a, b, c):
    """Real roots of a second order polynomial."""

    # Compute square root of the discriminant
    sqrt_disc = np.sqrt(b**2 - 4 * a * c)

    # Compute two roots
    root_1 = (-b + sqrt_disc) / (2*a)
    root_2 = (-b - sqrt_disc) / (2*a)

    return root_1, root_2
