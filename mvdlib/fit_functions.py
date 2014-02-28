"""
Commonly used fit functions (and some utility functions) meant to be
used with :py:meth:`scipy.optimize.curve_fit`.

"""

import numpy as np

# Fit functions
# -------------

def gaussian(t, A, B, t0, sigma):
    r"""
    Computes the Gaussian profile

    .. math::
    
        f(t; A, B, t_0, \sigma) = A \exp \left[
        \frac{-(t - t_0)^2}{2 \sigma^2} \right] + B

    Parameters
    ----------
    t : float or array-like
        List of points to evaluate the function over.
    A : float
        Overal multiplicative factor.
    B : float
        Overall zero level offset.
    t0 : float
        Position of the center of the Gaussian.
    sigma : float
        Standard deviation.

    Returns
    -------
    float or array-like

    """
    return A*np.exp(-(t - t0)**2/(2*sigma**2)) + B

def lorentzian(x, A, B, x0, gamma):
    r"""
    Computes the Lorentzian profile

    .. math::

        f(x; A, B, x_0, \gamma) = \frac{A}{\pi \gamma \left[
        1 + \left( \frac{x - x_0}{\gamma} \right)^2 \right]}

    Parameters
    ----------
    x : float or array-like
        List of points to evaluate the function over.
    A : float
        Overal multiplicative factor.
    B : float
        Overall zero level offset.
    x0 : float
        Position of the center of the Gaussian.
    gamma : float
        Lorentzian width.

    Returns
    -------
    float or array-like
    
    """
    return A/(np.pi*gamma*(1 + ((x - x0)/gamma)**2))

def sechsq(t, A, B, t0, tau):
    r"""
    Computes a :math:`\text{sech}^2` profile.

    Parameters
    ----------
    t : float or array-like
        List of points to evaluate the function over.
    A : float
        Overal multiplicative factor.
    B : float
        Overall zero level offset.
    t0 : float
        Position of the center of the profile.
    tau : float
        Width of the profile.

    Returns
    -------
    float or array-like    

    """
    return A/np.cosh((t - t0)/tau)**2 + B

def sine(t, A, B, w, phi):
    """
    Sine function with arguments compatible with the other fit
    functions.

    """
    return A*np.sin(w*t + phi) + B

def exp_decay(t, A, B, tau, t0):
    """
    Exponential decay function with arguments compatible with the
    other fit functions.

    """
    return A*np.exp(-(t - t0)/tau) + B

# Utility functions
# -----------------

def get_fwhm(p, ftype='gaussian'):
    """
    Find the FWHM of a given fit.

    Parameters
    ----------
    p : tuple
        Fit parameters found using
        :py:meth:`scipy.optimize.curve_fit`.
    ftype : str, optional
        Specifies the type of fit function used. Valid options are
        'gaussian', 'sechsq', or 'lorentzian'.

    """
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
        
