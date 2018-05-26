# 25 May 2018 Miroslav Gasparek
# Python bootcamp, lesson 35: Testing and test-driven development

# Import modules
import pytest
import bioinfo_dicts as bd


def n_neg(seq):
    """ Number of negative residues of a protein sequence."""

    # Convert sequence into upper case
    seq = seq.upper()

    # Check for a valid sequence
    for aa in seq:
        if aa not in bd.aa.keys():
            raise RuntimeError(aa + ' is not a valid amino acid.')
    # Count E's and D's, since these are the negative residues
    return seq.count('E') + seq.count('D')

# We are trying to test our function with inputs and corresponding outputs
# to see if we get match between them.

# We can use 'assert' statement with appended comment

def test_n_neg():
    """ Perform unit tests on n_neg."""

    assert n_neg('E') == 1
    assert n_neg('D') == 1
    assert n_neg('') == 0
    assert n_neg('ACKLWTTAE') == 1
    assert n_neg('DDDDEEEE') == 8
    assert n_neg('acklwttae') == 1

    pytest.raises(RuntimeError, "n_neg('Z')")
    pytest.raises(RuntimeError, "n_neg('z')")
    pytest.raises(RuntimeError, "n_neg('KAACABAYABADDLKPPSD')")

# Run all the tests
test_n_neg()

# Assertions vs. exceptions
# Use exceptions to check inputs to see if the user is using the function properly
# Use assertions to make sure the function operates as expected for given input.

# Can use 'pytest' (py.test)
# Also there are 'unittest' and 'nose' packages for Python for testing

# For each function you want to test:
# 1. write a function called test_fun() that has all the unit tests with the
# desired assert statement

# 2. Put all these tests in a directory called 'tests', which is in the directory
# containing the code

# 3. 'cd' into the directory with code and enter py.test at the cmd line.
# 'pytest' will then take over and automatically run all of the unit tests and give reports.
