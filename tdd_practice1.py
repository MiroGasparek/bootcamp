# 27 May 2018 Miroslav Gasparek
# Python bootcamp, lesson 36: Exercise on testing and test-driven development

# Import modules
import re
import pytest

import numpy as np
import pandas as pd


### Practice 1 ###
def find_codon_lesson6(codon, seq):
    """ Find a specified codon within a given sequence."""

    i = 0
    # Scan sequence until we hit the start codon or the end of the sequence
    while seq[i:i+3] != codon and i < len(seq):
        i += 1

    if i == len(seq):
        return -1

    return i

# We are trying to test our function with inputs and corresponding outputs
# to see if we get match between them.

# Select the sequence
synapto_nuc = ("ATGGAGAACAACGAAGCCCCCTCCCCCTCGGGATCCAACAACAACGAGAACAACAATGCAGCCCAGAAGA"
"AGCTGCAGCAGACCCAAGCCAAGGTGGACGAGGTGGTCGGGATTATGCGTGTGAACGTGGAGAAGGTCCT"
"GGAGCGGGACCAGAAGCTATCGGAACTGGGCGAGCGTGCGGATCAGCTGGAGCAGGGAGCATCCCAGTTC"
"GAGCAGCAGGCCGGCAAGCTGAAGCGCAAGCAATGGTGGGCCAACATGAAGATGATGATCATTCTGGGCG"
"TGATAGCCGTTGTGCTGCTCATCATCGTTCTGGTGTCGCTTTTCAATTGA")

synapto_prot = ("MENNEAPSPSGSNNNENNNAAQKKLQQTQAKVDEVVGIMRVNVEKVLERDQKLSELGERADQLEQGASQF"
"EQQAGKLKRKQWWANMKMMIILGVIAVVLLIIVLVSLFN")

# Print the results
print('ATG : ', find_codon_lesson6('ATG', synapto_nuc))
print('AAT : ', find_codon_lesson6('AAT', synapto_nuc))
print('TGT : ', find_codon_lesson6('TGT', synapto_nuc))
print('TGC : ', find_codon_lesson6('TGC', synapto_nuc))
print()

# Check if the amino acids corresponding to the codons actually exist
# in the protein sequence

print("M : ", synapto_prot.find("M"))
print("N : ", synapto_prot.find("N"))
print("C : ", synapto_prot.find("C"))

# Separate the nucleotide sequence into codons to check using regexp-s
all_codons = re.findall('...', synapto_nuc)
print('ATG : ', 'ATG' in all_codons)
print('AAT : ', 'AAT' in all_codons)
print('TGT : ', 'TGT' in all_codons)
print('TGC : ', 'TGC' in all_codons)

# Write a new function that makes sure that  we only look at the register codons
# after the start codon.
def find_codon_new(codon, seq):
    """ Find a specified codon within a given sequence. """
    i = 0
    # Scan sequenece until we hit a start codon or the end of sequence
    while seq[i:i+3] != codon and i < len(seq):
        i += 3

    if i == len(seq):
        return -1

    return i

# Write a function with synaptobrevin seq. as the test and run the test
def test_find_codon(find_codon):
    """
    A function to test another function that looks for a codon within
    a coding sequence.
    """
    synapto_nuc = ("ATGGAGAACAACGAAGCCCCCTCCCCCTCGGGATCCAACAACAACGAGAACAACAATGCAGCCCAGAAGA"
    "AGCTGCAGCAGACCCAAGCCAAGGTGGACGAGGTGGTCGGGATTATGCGTGTGAACGTGGAGAAGGTCCT"
    "GGAGCGGGACCAGAAGCTATCGGAACTGGGCGAGCGTGCGGATCAGCTGGAGCAGGGAGCATCCCAGTTC"
    "GAGCAGCAGGCCGGCAAGCTGAAGCGCAAGCAATGGTGGGCCAACATGAAGATGATGATCATTCTGGGCG"
    "TGATAGCCGTTGTGCTGCTCATCATCGTTCTGGTGTCGCTTTTCAATTGA")

    assert find_codon('ATG', synapto_nuc) == 0
    assert find_codon('AAT', synapto_nuc) == 54
    assert find_codon('TGT', synapto_nuc) == -1
    assert find_codon('TGC', synapto_nuc) == -1

    return None

# Run all the tests
test_find_codon(find_codon_new)
