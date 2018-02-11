# Exercises 1 for Python

# Exercise 1.3
def complement_base(base):
    """ Returns the Watson-Crick complement of a base."""
    if base == 'A' or base == 'a':
        return 'T'
    elif base == 'T' or base == 't':
        return 'A'
    elif base == 'G' or base == 'g':
        return 'C'
    else:
        return 'G'

def reverse_complement(seq):
    """ Compute reverse complement of a sequence. """
    # Initialize reverse complement
    rev_seq = ''
    # Loop through and populate list with reverse complement
    for base in seq:
        rev_seq += complement_base(base)
    return rev_seq[::-1]

def reverse_complement_no_loops(seq):
    """Return WC complement of a base without loops"""
    # Initialize rev_seq to a lowercase seq
    rev_seq = seq.lower()
    # Substitute bases
    rev_seq = rev_seq.replace('t','A')
    rev_seq = rev_seq.replace('a','T')
    rev_seq = rev_seq.replace('g','C')
    rev_seq = rev_seq.replace('c','G')

    return rev_seq[::-1]

# Exercise 1.4

# Function that takes two sequences and returns the longest common substring.
# A sobustring is a contiguous portion of a string. For example:
def longest_common_substring(s1,s2):
    """Returns longest common substring of two sequences."""
    # Make sure that s1 is the shorter one
    if len(s1) > len(s2):
    # If s1 was shorter, then switch sequence order
        s1, s2 = s2, s1
    # Start with the entire sequence and shorten
    substr_len = len(s1) # Define substring of length of s1
    # While substring is longer than zero, iterate.
    while substr_len > 0:
        # Try all substrings
        for i in range(len(s1) - substr_len+1):
            # Check if the whole string is in the sequence 2, if not ,then shorten
            # and start from beginning
            if s1[i:i+substr_len] in s2:
                return s1[i:i+substr_len]

        substr_len -= 1
    # If we haven't returned, there is no common substring
    return ''

# Exercise 1.5
# Function that returns true if parenthesis are valid and false if parenthesis are invalid
def verify_parenthesis(bracket_seq):
    """ Returns true if parenthesis are correct, returns false otherwise."""
    return bracket_seq.count('(') == bracket_seq.count(')')

def dot_parens_to_bp(bracket_seq):
    """ Converts dot-parens notation to a tuple of 2-tuples representing the base pairs."""
    if not verify_parenthesis(bracket_seq):
        print('Error in input structure.')
        return False

    # Initialize list of open parens and list of base pairs
    open_parens = []
    bps = []
    # Scan through string
    for i, x in enumerate(bracket_seq):
        if x== '(':
            open_parens.append(i)
        elif x == ')':
            if len(open_parens) > 0:
                bps.append((open_parens.pop(),i))
            else:
                print('Error in input structure.')
                return False
    # Return the result as a tuple
    return tuple(sorted(bps))

def hairpin_check(bps):
    """ Check to make sure no hairpins are too short."""
    for bp in bps:
        if bp[1] - bp[0] < 4:
            print('A hairpin is too short.')
            return False
        # Everything checks out
        return True

def rna_ss_validator(seq,sec_struc, wobble=True):
    """ Validate and RNA structure."""
    # Convert structure to base pairs
    bps = dot_parens_to_bp(sec_struc)
    # If this failed the structure was invalid
    if not bps:
        return False
    # Do the hairpin checks
    if not hairpin_check(bps):
        return False
    # Possible base pairs
        if wobble:
            ok_bps = ('gc','cg','au','ua','gu','ug')
        else:
            ok_bps = ('gc','cg','au','ua')
        # Check complementarity
        for bp in bps:
            bp_str = (seq[bp[0]] + seq[bp[1]]).lower()
            if bp_str not in ok_bps:
                print('Invalid base pair.')
                return False
        # Everything passed
        return True

def mean(values):
    """ Compute the mean of a sequence of numbers. """
    return sum(values)/len(values)
