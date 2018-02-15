# 11 February 2018 Miroslav Gasparek
# Python practical on File Input/Output
import os

# Open File
with open('data/1OLG.pdb', 'r') as f, open('atoms_chain_A.txt', 'w') as f_out:
    # Get all the lines
    lines = f.readlines()
    
    # Put the ATOM lines from chain A in new file
    for line in lines:
        if len(line) > 21 and line[:4] == 'ATOM' and line[21] == 'A':
            f_out.write(line)