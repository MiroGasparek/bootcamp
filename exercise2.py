# 17 February 2018 Miroslav Gasparek
# Python tutorial Exercise 2

import re
import bioinfo_dicts

# Exercise 2.2
# Read all the liens into a list
with open('data/salmonella_spi1_region.fna' ,'r') as f:
    file_str = f.read()
# Cut off first line, but keep descriptor
descriptor = file_str[:file_str.find('\n')]
file_str = file_str[file_str.find('\n')+1:]
# Eliminate newlines
seq = file_str.replace('\n','')

# Save the sequence into new text file
with open('salmonella_spi1_seq.txt', 'w') as newfile:
    newfile.write('This is salmonella \'s sequence')
    newfile.write(seq)
