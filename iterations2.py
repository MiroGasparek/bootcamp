# 04 February 2018
# Iterations

# The sequence to analyze
seq = 'GACAGACUCCAUGCACGUGGGUAUCUGUC'

# Initialize GC counter
n_gc = 0
# Initialize sequence length
len_seq = 0

# Loop through sequence and count G's and C's
for base in seq:
    len_seq += 1 # Same as len_seq = len_seq+1
    if base in 'GCgc':
        n_gc += 1

# Divide to get GC content
print(n_gc / len_seq)

# Print numbers 2 to 9
for i in range(2,10):
    print(i, end= ' ')
# Print a newline
print()
# Print even nubmers 2 through 9
for i in range(2,10,2):
    print(i,end = '  ')

# Make a list that has the same entries as range object with range 10
list(range(10))

# use the range() function along with the len() function on lists
# to double the elements of list

my_integers = [1,2,3,4,5]

for i in range(len(my_integers)):
    my_integers[i] *= 2

print('My integers are: ',my_integers)

# Initialize GC counter
n_gc = 0
# Initialize sequence length
len_seq = 0
# Initialize the base
base = 0
# Loop through sequence and print index of G's
for base in seq:
    if base in 'Gg':
        print(len_seq,end = ' ')
    len_seq += 1
print(len_seq)

# Better way to do this
# Loop through the sequence and print index of G's
for i, base in enumerate(seq):
    if base in 'Gg':
        print(i, end = ' ')

# enumerate() allows to use index and base at the same time
# Print index and identity of bases
for i, base in enumerate(seq):
    print(i,base)

# The doubling code with enumerate()
my_integers = [1,2,3,4,5]
for i, _ in enumerate(my_integers): # '_' for unused variable
    my_integers[i] *= 2

print(my_integers)

# zip() allwos us to iterate over several items at once
names = ('Lloyd','Holiday','Heath')
positions = ('MF','MF','F')
numbers = (10,12,17)

for num,pos,name in zip(numbers, positions, names):
    print(num,name,pos)

# reverse() can count backwards
count_up = ('ignition',1,2,3,4,5,6,7,8,9,10)

for count in reversed(count_up):
    print(count)

# Define start codon
start_codon = 'AUG'
# Initialize sequence index
i=0
# Scan sequence until we hit the start codon, but DONT DO this
while seq[i:i+3] != start_codon and i < len(seq):
    i += 1
# Show the result
    if i == len(seq):
        print(' Codon not found in sequence.')
        break
else:
    print('The codon starts at index ',i)
