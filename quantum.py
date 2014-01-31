"""
mvdlib.quantum

Quantum calculation routines.
"""

from __future__ import print_function
from __future__ import division

# Angular momentum-related functions
# ----------------------------------

def lande_g(S, L, J):
    """Return the Lande' g factor."""
    num = J*(J + 1) + S*(S + 1) - L*(L + 1)
    den = 2*J*(J + 1)
    return 1 + num/den
