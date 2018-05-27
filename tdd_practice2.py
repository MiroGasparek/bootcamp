# 27 May 2018 Miroslav Gasparek
# Python bootcamp, lesson 36: Exercise on testing and test-driven development

# Import modules
import re
import pytest

import numpy as np
import pandas as pd


### Practice 2 ###

def test_dissoc_equil():
    """ Tests for dissoc_equil()."""

    # Check for the validity of the response to the proper inputs
    # Edge cases
    assert np.allclose(dissoc_equil(1,0,0), np.array([0,0,0]))
    assert np.allclose(dissoc_equil(0,0,0), np.array([0,0,0]))
    assert np.allclose(dissoc_equil(0, 1, 1), np.array([0, 0, 1]))
    assert np.allclose(dissoc_equil(0, 1, 2), np.array([0, 1, 1]))
    assert np.allclose(dissoc_equil(0, 2, 1), np.array([1, 0, 1]))
    assert np.allclose(dissoc_equil(np.inf,1,1), np.array([1,1,0]))

    # Standard cases
    # Check for the range of initial conditions on a log scale
    # This will exhibit an error - due to the numerical stability issue
    Kd_vals = np.logspace(-10, 1, 50)
    ca0_vals = np.logspace(-5, 2, 50)
    cb0_vals = np.logspace(-5, 2, 50)
    for Kd in Kd_vals:
        for ca0 in ca0_vals:
            for cb0 in cb0_vals:
                assert check_eq(Kd, ca0, cb0, *dissoc_equil(Kd, ca0, cb0)), \
                    'Kd = %g, ca0 = %g, cb0 = %g' % (Kd, ca0, cb0)
    # Check for the validity of the user input
    # Errors
    pytest.raises(RuntimeError, "dissoc_equil(-1,1,1)")
    pytest.raises(RuntimeError, "dissoc_equil(1, -1, 1)")
    pytest.raises(RuntimeError, "dissoc_equil(1, 1, -1)")
    pytest.raises(RuntimeError, "dissoc_equil(1, np.inf, 1)")
    pytest.raises(RuntimeError, "dissoc_equil(1, 1, np.inf)")

    return None

def dissoc_equil(Kd, ca0, cb0):
    """ Compute equilibrium for dissociation reaction."""

    # Check input
    if Kd < 0 or ca0 < 0 or cb0 < 0:
        raise RuntimeError('All input must be nonnegative.')
    if not (ca0 < np.inf and cb0 < np.inf):
        raise RuntimeError('Input concentrations must be finite.')

    # If we have infinite Kd
    if Kd == np.inf:
        return ca0, cb0, 0

    # Compute cab from quadratic formula
    b = ca0 + cb0 + Kd
    cab = (b - np.sqrt(b**2 - 4*ca0*cb0))/2

    # Compute ca and cb from conservation of mass
    ca = ca0 - cab
    cb = cb0 - cab
    return ca, cb, cab


def check_eq(Kd, ca0, cb0, ca, cb, cab):
    """Verify equilibrium expressions hold."""
    eq = np.isclose(Kd, ca * cb / cab)
    cons_mass_A = np.isclose(ca0, ca + cab)
    cons_mass_B = np.isclose(cb0, cb + cab)

    return eq and cons_mass_A and cons_mass_B

# Test the function
test_dissoc_equil()
