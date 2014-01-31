"""fit_functions.py

Commonly used fit functions (and some utility functions) meant to be
used with scipy.optimize.curve_fit.

"""

import numpy as np

## Fit functions ##

def gaussian(t, A, B, t0, sigma):
    return A*np.exp(-(t - t0)**2/(2*sigma**2)) + B

def lorentzian(x, A, B, x0, gamma):
    return A/(np.pi*gamma*(1 + ((x - x0)/gamma)**2))

def sechsq(t, A, B, t0, tau):
    """sech^2 profile."""
    return A/np.cosh((t - t0)/tau)**2 + B

def sine(t, A, B, w, phi):
    return A*np.sin(w*t + phi) + B

def exp_decay(t, A, B, tau, t0):
    return A*np.exp(-(t - t0)/tau) + B

## Utility functions ##

def get_fwhm(p, ftype='gaussian'):
    """Find the FWHM of a given fit."""
    types = ['gaussian', 'sechsq', 'lorentzian']
    if ftype == 'gaussian':
        return 2*np.sqrt(2*np.log(2))*p[3]
    elif ftype == 'sechsq':
        return 1.76*p[3]
    elif ftype == 'lorentzian':
        return p[3]
    else:
        raise ValueError("ftype must be one of: %s, %s, %s" % \
                         (types[0], types[1], types[2]))
        
