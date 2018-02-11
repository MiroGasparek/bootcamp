# Module for import of the bioinfo dictionaries
import bioinfo_dicts as bd
bd.aa, bd.codons

def my_fun(a,b, **kwargs):
    """ Concatenate sequences. """
    seq = a + b

    for key in kwargs:
        seq += kwargs[key]
    return seq

# 11 February 2018 Miroslav Gasparek
# Dictionaries and Hash tables in Python

name = ('jane','doe')

# Create dictionary
my_dict = {'a':6, 'b': 7, 'c': 27.6}
print(my_dict)

# Another way to create Dictionaries
my_dict2 = dict((('a',6),('b',7),('c',27.6)))
print(my_dict2)

# Another dictionary
my_dict3 = dict(a='yes',b='no',c='maybe')

my_dict = {0: 'zero',
            1.7:  [1,2,3],
            (5,6,'dummy string'): 3.14,
            'strings are immutable': 42}
# Dictionary of amino acirds
aa_dict = {'A': 'Ala',
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

# The set of DNA bases
bases = ['T', 'C', 'A', 'G']

# Build list of codons
codon_list = []
for first_base in bases:
    for second_base in bases:
        for third_base in bases:
            codon_list += [first_base + second_base + third_base]

# The amino acids that are coded for (* = STOP codon)
amino_acids = 'FFLLSSSSYY**CC*WLLLLPPPPHHQQRRRRIIIMTTTTNNKKSSRRVVVVAAAADDEEGGGG'

# Build dictionary from tuple of 2-tuples (technically an iterator, but it works)
codons = dict(zip(codon_list, amino_acids))

# Show that we did it
print(codons)

# Create dictionary
my_dict = {'a': 6, 'b': 7,'c': 12.6}
# Find where they are stored
print(id(my_dict))
print(id(my_dict['a']))
print(id(my_dict['b']))
print(id(my_dict['c']))


# Hash function converts input into integer
hash('a'), hash('b'), hash('c')
# A collection of elements that can be indexed to integers
# corresponding to locations in memory is called hash table

# Dictionaries are mutable
print(my_dict)
# Add an entry
my_dict['d'] = 'Bootcamp is so much fun!'
# Look at dictionary again
print(my_dict)
# Change an entry
my_dict['a'] = 'I was not satisfied with entry a.'
# Look at it again
print(my_dict)

print()
print()
# Make a fresh my_dict
my_dict = {'a': 1, 'b': 2, 'c': 3}
# in works with keys only
print('b' in my_dict, 'd' in my_dict, 'e' not in my_dict)
print(2 in my_dict)

# Iterate over keys
for key in my_dict:
    print(key,':',my_dict[key])

# Iterate over keys
for key,item in my_dict.items():
    print(key, item)
# Items cannot be changed through items, only through keys
for key,item in my_dict.items():
    item = 'this string will not be in dictionary.'
print(my_dict)

for key,item in my_dict.items():
    my_dict[key] = 'this will be in the dictionary.'
print(my_dict)
# len(d) gives the number of entries in dictionary d
# del(k) deletes entry with key k from dictionary d

# Create my_list and my_dict for reference
my_dict = dict(a=1, b=2, c=3, d=4)
my_list = [1,2,3,4]
# Print them
print('my_dict:', my_dict)
print('my_list:',my_list)
# Get lengths
print('Length of my_dict:',len(my_dict))
print('length of my_list:',len(my_list))
# Delete a key from my_dict
del my_dict['b']
# len(d) gives the number of entries in dictionary d
# del(k) deletes entry with key k from dictionary d

# Create my_list and my_dict for reference
my_dict = dict(a=1, b=2, c=3, d=4)
my_list = [1,2,3,4]
# Print them
print('my_dict:', my_dict)
print('my_list:',my_list)
# Get lengths
print('Length of my_dict:',len(my_dict))
print('length of my_list:',len(my_list))
# Delete a key from my_dict
del my_dict['b']
# Delete entry from my_list
del my_list[1]
# Show post-deleted objects
print('post-deleted my_dict:', my_dict)
print('post-deleted my_list:', my_list)

# Dictionaries methods
my_dict = dict(a=1, b=2, c=3, d=4)
my_dict.keys()


print(my_fun('TACAC','CAGGGA',c='GGGGG',d='AAAATTTTT'))

# Take a dictionary of values and pass it to the function
my_dict = {'a': 'TGACAC',
           'b': 'CAGGGA',
           'c': 'GGGGGGGGG',
           'd': 'AAAATTTTT'}
# Pass directly into the function by preceding it with a double asterisk.
print(my_fun(**my_dict))
