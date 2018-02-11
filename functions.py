# Introduction to functions in Python

# Nontrivial function that computes reverse complement of a sequence of DNA
def complement_base(base, material='DNA'):
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


def reverse_complement(seq, material='DNA'):
    """Compute reverse complement of a sequence."""
    # Initialize reverse complement
    rev_seq = ''
    # Loop through and populate list with reverse complement
    for base in reversed(seq):
        rev_seq += complement_base(base, material=material)

    return rev_seq
# 'named keyword argument', also known as a named kwarg was added
# Syntax for a named kwarg is kwarg_name=default_value ...
# ... in the 'def' clause of the function definition


print(reverse_complement('GCAGTTGCA'))

def display_complements(seq):
    """Print sequence above its reverse complement."""

    # Compute the reverse complement
    rev_comp = reverse_complement(seq)
    # Print template
    print(seq)
    # Print "base pairs"
    for base in seq:
            print('|',end='')
    # Print final newline character
    print()
    # Print reverse complement
    for base in reversed(rev_comp):
        print(base, end='')
    # Print final newline character
    print()

seq = 'GCAGTTGCA'
display_complements(seq)

# We used smaller chunks of code -> MODULAR PROGRAMMING

# Named keyword argument is optional:
print()
print(reverse_complement('GCAGTTGCA'))
print(reverse_complement('GCAGTTGCA',material='RNA'))

print()
# Calling a function with *tuple
def is_almost_right(a,b,c):
    """
    Checks to see if a triangle with side lengths 'a', 'b', and 'c' is right.
    """
    # Use sorted(), which gives a sorted list
    a,b,c = sorted([a,b,c])
    # Check to see if it is almost a right triangle
    if abs(a**2 + b**2 - c**2) < 1e-12:
        return True
    else:
        return False

    is_almost_right(13,5,12)
# We can have tuple with triangle side lengths
side_lengths = (13,5,12)
# All the side lengths can be passed in separately by splitting the tuple...
# ... By putting a * in front of it
is_almost_right(*side_lengths)
