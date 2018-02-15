# 11 February 2018 Miroslav Gasparek
# Python practical on File Input/Output
import os

# Open File
f = open('data/1OLG.pdb','r')
# What is f?
f

f_str = f.read()
f_str[:1000]

f_list = f.readlines()
f_list

# To rewind back to the beginning, we do f.seek(0)
# Go to the beginning of the file
f.seek(0)
# Read the contents in as a list
f_list = f.readlines()
# Check out the first 10 entries
f_list[:10]

# Strip all whitespaces including newlines from the end of a string
f_list[0].rstrip()

# We must close file when we are done with it
f.close()
# Check if file is closed
print('Is file closed?' ,f.closed)
print()
## Use of context managers with files
with open('data/1OLG.pdb', 'r') as f:
    f_lines = f.readlines()
    print('In the with block, is the file closed?', f.closed)

print('Out of the with block, is the file closed?',f.closed)

# Check the first three lines
f_lines[:3]

# Print the first ten lines of the file
with open('data/1OLG.pdb', 'r') as f:
    counter = 0
    for line in f:
        print(line.rstrip())
        counter += 1
        if counter >= 10:
            break

print()
# Another way to print first ten lines of the file
with open('data/1OLG.pdb', 'r') as f:
    counter = 0
    while counter < 10:
        print(f.readline().rstrip())
        counter += 1

# Check if the file already exists:
LogicVal = os.path.isfile('data/1OLG.pdb')
print('Does given file exist? ',LogicVal)

# Otherwise, get ready to open a file to write.
# if os.path.isfile('mastery.txt'):
#     raise RuntimeError('File mastery.txt already exists.')
# with open('mastery.txt', 'w') as f:
#     f.write('This is my file.')
#     f.write('There are many like it, but this one is mine.')
#     f.write('I must master my file like I must master my life.')

# f.write() only accepts strings, so numbers must be converted to strings
with open('gimme_phi.txt', 'w') as f:
    f.write('The golden ratio is phi = ')
    f.write('{phi: .8f}'.format(phi=1.61803398875))
