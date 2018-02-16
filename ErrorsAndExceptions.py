# 16 February 2017 Miroslav Gasparek
# Errors and Exception handling in Python

import warnings
import bioinfo_dicts as bd

# 16 February 2018 Miroslav Gasparek
# Handling user error function
import warnings
import bioinfo_dicts as bd

def one_to_three(seq):
    """Converts a protein sequence using one-letter abbreviations
    to one using three-letter abbreviations. """

    # Convert seq to upper case
    seq = seq.upper()

    # Make sure there are no illegal amino acids
    for amino_acid in seq:
        if amino_acid not in bd.aa.keys():
            raise RuntimeError(amino_acid + 'is not a valid amino acid.')

    # Otherwise, do the conversion
    aa_list = []
    for amino_acid in seq:
        aa_list += [bd.aa[amino_acid], '-']

    # Return the result
    return ''.join(aa_list[:-1])


# Types of errors:
# - Syntax error
# Runtime error
# Semantic errors

# Try statement to handle runtime errors

# Try to get the gc_content module
try:
    import gc_content
    have_gc = True
except ImportError as e:
    have_gc = False
finally:
    # Do whatever is necessary here, like close files
    pass

seq = 'ACGATCTACGATCAGCTGCGCGCATCG'

if have_gc:
    print(gc_content(seq))
else:
    print(seq.count('G') + seq.count('C'))


# Issue warning
# Try to get the gc_content module
try:
    import gc_content
    have_gc = True
except ImportError as e:
    have_gc = False
    warnings.warn('Failed to load gc_content. Using custom function.', UserWarning)
    
finally:
    # Do whatever is necessary here, like close files
    pass

seq = 'ACGATCTACGATCAGCTGCGCGCATCG'

if have_gc:
    print(gc_content(seq))
else:
    print(seq.count('G') + seq.count('C'))


print(one_to_three('waeifnsdfklnsae'))
print(one_to_three('waeifnsdfzklnsae'))