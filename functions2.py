# 04 February 2018 Functions


# Define function using def()
def ratio(x,y):
    """The ratio of 'x' to 'y'."""
    return x/y

# Define function that always returns the same thing
def IReturnOne():
    """This returns 1"""
    return 1

print(ratio(4,2))
print(IReturnOne())

# Function without return argument
def think_too_much():
    """Express Caesar's skepticism about Cassius """
    print("Not too much...")

think_too_much()

# The function that returns nothing
return_val = think_too_much()
print()
print(return_val)

def complement_base(base, material ='DNA'):
    """Returns the Watson-Crick complement of a base."""
    if base == 'A' or base == 'a':
        if material == 'DNA':
            return 'T'
        elif material == 'RNA':
            return 'U'
    elif base == 'T' or base == 't' or base == 'U' or base == 'u':
        return 'A'
    elif base == 'G' or base == 'g':
        return 'C'
    else:
        return 'G'

def reverse_complement(seq,material = 'DNA'):
    """ Compute reverse complement of a sequence."""
    # Initialize reverse complement
    rev_seq = ''
    # Loop through and populate list with reverse complement
    for base in reversed(seq):
        rev_seq += complement_base(base,material)
    return rev_seq

reversed_sequence = reverse_complement('GCATTGCA')
print(reversed_sequence)

# Define function displaying template strand above its reverse complement
def display_complements(seq):
        """ Print sequence above its reverse complement."""

        # Compute the reverse complement
        rev_comp = reverse_complement(seq)
        # Print template
        print(seq)
        # Print "base pairs"
        for base in seq:
            print('|',end = '')
        # Print final newline character after base pairs
        print()
        # Print reverse complement
        for base in reversed(rev_comp):
            print(base, end='')
        # Print final newline character
        print()

#####
seq = 'GCAGTTGCA'
print(seq)
print()
display_complements(seq)


print(reverse_complement('GCAGTTGCA',material='RNA'))


# Function checks if triangle is right-angled
def is_almost_right(a,b,c):
    """ Checks if triangle is right-angled."""
    # Use sorted(), which gives a sorted list
    a,b,c = sorted([a,b,c])

    # Check to see if it is almost a right triangle
    if abs(a**2+b**2-c**2) < 1e-12:
        return True
    else:
        return False
