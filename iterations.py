# The sequence we want to analyze
seq = 'GACAGACUCCAUGCACGUGGGUAUCUGUC'

# Initialize GC counter
n_gc = 0
# Initialize sequence length
len_seq = 0

# Loop through sequence and count G's and C's
for base in seq:
    len_seq += 1
    if base in 'GCgc':
        n_gc += 1

# Divide to get GC content
print(n_gc / len_seq)

# We'll do one through 5
my_integers = [1,2,3,4,5]
# Double each one
for n in my_integers:
    n *= 2
# Check out the result
print(my_integers)
# Does not work quite right
# We have to use iterators

# Range function gives an iterable that enables counting.
for i in range(10):
    print(i, end=' ')

# Range function gives an iterable that enables counting.
for i in range(2,10):
    print(i, end=' ')
# Print a newline
print()
# Print even numbers, 2 through 9
for i in range(2,10,2):
    print(i, end='  ')
# Type conversion from range to list
list = list(range(10))
print()
print(list)
print()
# Make the previous function working
my_integers = [1,2,3,4,5]
print(my_integers)
print()
for i in range(len(my_integers)):
    my_integers[i] *= 2

print(my_integers)
print()
print(seq)
# Initialize GC counter
n_gc = 0
# Initialized sequence length
len_seq = 0
# Loop through sequence and print index of G's
for base in seq:
    if base in 'Gg':
        print(len_seq, end=' ')
    len_seq += 1
print()
# We can use enumerate ()
# Loop through sequence and print index of G's
for i, base in enumerate(seq):
    if base in 'Gg':
        print(i, end=' ')
print()
for i, base in enumerate(seq):
    print(i,base)

print()
for i in range(len(seq)):
    print(i,seq[i])

print()

my_integers = [1,2,3,4,5]
# Double each one
for i, _ in enumerate(my_integers):
    my_integers[i] *= 2
# Check out the result
my_integers


# The zip() function
names = ('Lloyd','Holiday','Heath')
positions = ('MF','MF','F')
numbers = (10,12,17)
for num, pos, name in zip(numbers,positions, names):
    print(num,name,pos)

# reversed() function

count_up = ('ignition', 1,2,3,4,5,6,7,8,9,10)
for count in reversed(count_up):
    print(count)

# 'while' Loop
# Define start codon
start_codon = 'AUG'
# Initialize sequence index
i = 0
# Scan sequence until we hit start codon
while seq[i:i+3] != start_codon:
    i += 1
# Show the result
print('The start codon starts at index',i)
print()
# Define codon of interest
codon = 'GCC'
# Initialize sequence index
i = 0
# Scan sequence until we hit the start codon or end of the sequence
while seq[i:i+3] != codon and i < len(seq):
    i += 1
# Show the result
if i == len(seq):
    print('Codon not found in sequence.')
else:
    print('The codon starts at index',i)

# Use 'for' loop with break instead of 'while'
start_codon = 'AUG'
# Scan sequence until we hit the start codon
for i in range(len(seq)):
    if seq[i:i+3] == start_codon:
        print('The start codon starts at index',i,'as expected')
        break
    else:
        print('Codon not found in sequence.')
