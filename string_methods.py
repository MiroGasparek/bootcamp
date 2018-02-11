# Introduction to string methods in Python

my_str = 'The Dude abides.'
print(my_str[5])
print(my_str[:6])
print(my_str[::2])
print(my_str[::1])

# count() string methods

# Define sequence
seq = 'GACAGACUCCAUGCACGUGGGUAUCAUGUC'
# Count G's and C's
GC = seq.count('G') + seq.count('C')
print(GC)

# Substrings of more than one character
seq.count('GAC')
# Substrings cannot overlap
'AAAAAAA'.count('AA')
# Something that is not here
seq.count('nonsense')
print('The position of the start codon is: ')
print(seq.find('AUG'))
# Do not use find() to test if substring is present

# Start search from the right end
seq.rfind('AUG')

def complement_base(base):
    """Returns the Watson-Crick complement of a base."""
        # Convert to lovercase
    base = base.lower()
    if base == 'a':
        return 'T'
    elif base == 't':
        return 'A'
    elif base == 'g':
        return 'C'
    else:
        return 'G'

print(complement_base('A'))

print('make ME All CapS'.upper())

# Replace instances of strings
replaced_seq = seq.replace('U','T')
print(replaced_seq)
# Strings are immutable

word_tuple = ('The','dude','abides')
print(' '.join(word_tuple))
print(list(' '.join(word_tuple)))

print(' * '.join(word_tuple))

# Use of format method, where we can change kwarg in the string for a specific
# string
my_str = """
Let's do a Mad Lib!
During this bootcamp, I feel {adjective}.
The instructors give us {plural_noun}.
""".format(adjective='truculent', plural_noun='haircuts')

# Some uses of the format with string
print('There are {n:d} states.'.format(n=50))
print('Your file number is {n:d}.'.format(n=23))
print('π is approximately {pi:f}.'.format(pi=3.14))
print('e is approximately {e:.8f}.'.format(e=2.7182818284590451))
print('Avogadro''s number is approximately {N_A:e}.'.format(N_A=6.022e23))
print('ε_0 is approximately {eps_0:.16e} F/m.'.format(eps_0=8.854187817e-12))
print('That {thing:s} really tied the room together.'.format(thing='rug'))
