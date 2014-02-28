"""
mvdlib.oceanoptics

Read spectra datafiles from Ocean Optics spectromters.
"""

from __future__ import print_function
import fit_functions
import numpy as np
import scipy.optimize as spo
import matplotlib.pyplot as plt

class OOSpectrum(object):
    def __init__(self):
        self.lmbda = None
        self.response = None

    def load_sample(self, filename):
        """Load sample data from file filename."""
        data = np.loadtxt(filename, skiprows=18, comments='>>')
        self.lmbda = data[:,0]
        self.response = data[:,1]

    def fit_gaussian(self, p0=None):
        """Try to fit the spectral data to a Gaussian profile.

        Parameters
        ----------
            p0 : array-like
                Initial guess for parameters.

        Returns
        -------
            p : list
                List of best-fit parameters.
            cov : numpy array
                Numpy array of covariances for the fit parameters.

        """
        if self.response is None:
            raise RuntimeError("You must load data first.")
        p, cov = spo.curve_fit(fit_functions.gaussian,
                               self.lmbda, self.response, p0)
        return p, cov
    
    def plot_spectrum(self, p=None, p_type='gaussian',
                      xlims=None, filename=None):
        """Plot a spectrum and fit if p is not None and optionally save."""
        if self.response is None:
            raise RuntimeError("You must load data first.")
        plt.figure()
        plt.plot(self.lmbda, self.response, 'b-')
        if p is not None:
            if p_type == 'gaussian':
                y = fit_functions.gaussian(self.lmbda, *p)
            else:
                raise ValueError("p_type must be one of: 'gaussian'")
            plt.plot(self.lmbda, y, 'b-', lw=2)
        plt.xlabel('$\lambda$ [nm]')
        plt.ylabel('Response [arb. units]')
        if xlims is not None:
            plt.xlim(xlims)
        if filename is not None:
            plt.savefig(filename)
