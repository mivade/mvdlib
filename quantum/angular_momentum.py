"""
mvdlib.quantum.angular_momentum

Functions related to angular momentum.

"""

from __future__ import print_function
from __future__ import division
from numpy import sqrt
from scipy.misc import factorial
from sympy.physics.quantum import cg

# Iteration limit for computing Wigner 6j symbols.
_SIXJ_LIMIT = 50

def _triangle(a, b, c):
    """
    Compute the triangle coefficient Delta(a b c). See
    http://mathworld.wolfram.com/TriangleCoefficient.html.

    """
    x = factorial(a + b - c)
    y = factorial(a - b + c)
    z = factorial(-a + b + c)
    return x*y*z/factorial(a + b + c + 1)

def lande_g(S, L, J):
    """
    Return the Lande' g factor... prefactor. I'm not actually sure if
    this thing has a name.

    """
    num = J*(J + 1) + S*(S + 1) - L*(L + 1)
    den = 2*J*(J + 1)
    return 1 + num/den

def cg_coef(j1, j2, m1, m2, j, m):
    """
    Computes the Clebsch-Gordan coefficient
    <j1 j2; m1 m2|j1 j2; jm>.

    This is simply a wrapper around Sympy's Clebsch-Gordan
    calculations so that a float is returned automatically.

    """
    coef = cg.CG(j1, m1, j2, m2, j, m)
    return float(coef.doit())

def wigner_3j(j1, j2, j3, m1, m2, m3):
    """Compute the Wigner 3-j symbol:

       ([j1 j2 j3]
        [m1 m2 m3])

    This function is a wrapper around Sympy's calculations.

    """
    symbol = cg.Wigner3j(j1, m1, j2, m2, j3, m3)
    return float(symbol.doit())

def wigner_6j(j1, j2, j3, J1, J2, J3):
    """
    Computes the Wigner 6-j symbol:

        {[j1 j2 j3]
         [J1 J2 J3]}

    Notation follows Wolfram MathWorld. This is apparently not yet
    implemented in Sympy, so it is implemented here.

    """
    def f(t):
        args = [t - j1 - j2 - j3, t - j1 - J2 - J3, t - J1 - j2 - J3,
                t - J1 - J2 - j3, j1 + j2 + J1 + J2 - t,
                j2 + j3 + J2 + J3 - t,
                j3+j1+J3+J1-t]
        args = factorial(array(args))
        result = args.prod()
        return result
            
    sixj = sqrt(_triangle(j1, j2, j3)*_triangle(j1, J2, J3) * \
                _triangle(J1, j2, J3)*_triangle(J1, J2, j3))
    term = 0.
    for t in range(_SIXJ_LIMIT):
        g = f(t)
        if g <= 0:
            continue
        else:
            term += (-1)**t*factorial(t + 1)/g
    sixj *= term
    return sixj
