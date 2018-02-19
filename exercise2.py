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
# with open('salmonella_spi1_seq.txt', 'w') as newfile:
#     newfile.write('This is salmonella \'s sequence')
#     newfile.write(seq)

# Exercise 2.3: Pathogenicity islands
# a)
def gc_content(seq):
    """ GC content of a given sequence. """
    seq = seq.upper()
    return (seq.count('G') + seq.count('C'))/len(seq)

def gc_blocks(seq,block_size):
    """ Divide sequence into non-overlapping blocks and compute GC content
    of each block."""
    blocks = []
    for i in range(0, len(seq) - (len(seq) % block_size), block_size):
        blocks.append(gc_content(seq[i:i+block_size]))
    return tuple(blocks)

# Exercise 2.3: Pathogenicty islands
# b)
def gc_map(seq, block_size, gc_thres):
    """ Returns original sequence where every base in a block with GC content
    above threshold is capitalized and every base below the threshold
    is lowercase."""

    out_seq = ''
    # Determine GC content of each block and change string accordingly
    for i in range(0, len(seq) - (len(seq) % block_size), block_size):
        if gc_content(seq[i:i+block_size]) < gc_thres:
            out_seq += seq[i:i+block_size].lower()
        else:
            out_seq += seq[i:i+block_size].upper()
    return out_seq

# Exercise 2.3
# c)
# Find pathogenicity islands for salmonella
sal_gcmap = gc_map(seq, 1000, 0.45)

# Exercise 2.3
# d)
# Write GC-mapped sequence to a new FASTA file.

# Write the result
with open('salmonella_spi1_region_gc_map.fna', 'w') as f:
    # Write description text
    f.write(descriptor + '\n')

    # Write sequence in blocks of 60
    i = 0
    while i < len(sal_gcmap) - 59:
        f.write(sal_gcmap[i:i+60] + '\n')
        i += 60
    # Write the last line
    f.write(sal_gcmap[i:])

# Print first and last lines of the pathogenicity islands file
# !head salmonella_spi1_region_gc_map.fna
# print('...')
# !tail salmonella_spi1_region_gc_map.fna

# Exercise 2.4
# a)
# There might be multiple longest ORF. We arbitrarily choose to return the
# one with the 3'-most starting index.

# We will find all start codons.
# For each start codon, find the first in-register stop codon.
# If there is an in-register stop codon, we store this start-stop pair.
# At the end, we sort them, longest to shortest.

# Three functions to be used:
    # find_all_starts(seq)
    # find_next_in_register_stop(seq)
    # all_orfs(seq)
def test_find_all_starts():
    assert find_all_starts('') == tuple()
    assert find_all_starts('GGAGACGACGCAAAAC'.lower()) == tuple()
    assert find_all_starts('AAAAAAATGAAATGAGGGGGGTATG'.lower()) == (6, 11, 22)
    assert find_all_starts('GGATGATGATGTAAAAC'.lower()) == (2, 5, 8)
    assert find_all_starts('GGATGCATGATGTAGAAC'.lower()) == (2, 6, 9)
    assert find_all_starts('GGGATGATGATGGGATGGTGAGTAGGGTAAG'.lower()) == \
                                                               (3, 6, 9, 14)
    assert find_all_starts('GGGatgatgatgGGatgGtgaGtagGGACtaaG'.lower()) == \
                                                               (3, 6, 9, 14)


def test_find_first_in_register_stop():
    assert find_first_in_register_stop('') == -1
    assert find_first_in_register_stop('GTAATAGTGA'.lower()) == -1
    assert find_first_in_register_stop('AAAAAAAAAAAAAAATAAGGGTAA'.lower()) == 18
    assert find_first_in_register_stop('AAAAAACACCGCGTGTACTGA'.lower()) == 21


def test_all_orfs():
    assert all_orfs('') == tuple()
    assert all_orfs('GGAGACGACGCAAAAC') == tuple()
    assert all_orfs('AAAAAAATGAAATGAGGGGGGTATG') == ((6, 15),)
    assert all_orfs('GGATGATGATGTAAAAC') == ((2, 14),)
    assert all_orfs('GGATGCATGATGTAGAAC') == ((6, 15),)
    assert all_orfs('GGGATGATGATGGGATGGTGAGTAGGGTAAG') == ((3, 21),)
    assert all_orfs('GGGatgatgatgGGatgGtgaGtagGGACtaaG') == ((14, 32), (3, 21))

# This is test-driven development
def find_all_starts(seq):
    """Find all start codons in sequence"""
    return None

# To be looked at in the last-year bootcamps: Class and RegEx
def find_all_starts_regex(seq):
    """ Find the starting index of all start codons in a lowercase seq """
    regex_start = re.compile('atg')

    # Find the indices of all start codons
    starts = []
    for match in regex_start.finditer(seq):
        starts.append(match.start())

    return tuple(starts)

# The function find_all_starts without regular expressions
def find_all_starts(seq):
    """ Find the starting index of all start codons in a lowercase seq. """
    # Initialize array of indices of start codons
    starts = []
    # Find index of first start codon (str.find() returns -1 if not found)
    i = seq.find('atg')
    # Keep looking for subsequent incrementing starting points of search
    while i >= 0:
        starts.append(i)
        i = seq.find('atg', i + 1)
    return tuple(starts)

# Function to find first stop codon in register
def find_first_in_register_stop_regex(seq):
    """
    Find first stop codon on lowercase seq that start at index that is
    divisible by three.
    """

    # Compile regexes for stop codons
    regex_stop = re.compile('(taa|tag|tga)')

    # Stop codon iterator
    stop_iterator = regex_stop.finditer(seq)

    # Find next stop codon that is in register
    for stop in stop_iterator:
        if stop.end() % 3 == 0:
            return stop.end()
    # Return -1 if we failed to find a stop codon
    return -1

# Function to find first stop codon in register without regular expressions
def find_first_in_register_stop(seq):
    """
    Find first stop codon on lowercase seq that start at index that is
    divisible by three.
    """

    seq = seq.lower()

    # Scan sequence for stop codon
    i = 0
    while i < len(seq) -2 and seq[i:i+3] not in ('taa','tag','tga'):
        i += 3
    # If before end, found codon, return end of codon
    if i < len(seq) - 2:
        return i + 3
    else: # Failed to find stop codon
        return -1
