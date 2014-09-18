"""Utilities for Rabi flopping data."""

from __future__ import division
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from .. import plot_settings

class RabiFlop(object):
    def __init__(self, datafile, **kwargs):
        """Rabi flopping plot object.

        Parameters
        ----------
        datafile : str
            Data file to plot

        Keyword arguments
        -----------------
        
        delimiter : str
            Column delimiter. Default: ';'
        percent : bool
            When True, populations are assumed to be 0-100 instead of
            0-1.0. Default: False
        use_errorbars : bool
            If False, only load time and population columns.

        """
        delimiter = kwargs.get('delimiter', ';')
        data = np.loadtxt(datafile, delimiter=delimiter)
        self.t = data[:,0]
        self.P = data[:,1]
        
        self.use_errorbars = kwargs.get('use_errobars', True)
        if self.use_errorbars:
            self.err = data[:,2]
        else:
            self.err = np.zeros(self.t.shape)

        percent = kwargs.get('percent', False)
        if not percent:
            self.P *= 0.01
            self.err *= 0.01

    def _func(self, t, A, f, tau):
        return A*(0.5 - 0.5*np.sin(f*t + np.pi/2.)*np.exp(-t/tau))

    def fit(self, f0, tau):
        """Fit the data using initial guess Rabi (angular) frequency
        f0 and decoherence time constant tau.

        """
        p0 = [1., f0, tau]
        self.p, self.cov = curve_fit(self._func, self.t, self.P, p0)
        self.rabi_frequency = self.p[1]
        return self.p, self.cov
            
    def plot(self, outfile, **kwargs):
        """Plot the data.

        Parameters
        ----------
        outfile : str
            Figure file to output.

        Keyword arguments
        -----------------
        style : str
            String specifying the plot style to use. Default:
            'default'
        show_fit : bool
            If True, plot with a fit. Default: True
        points : int
            Number of points to use for the fit plotting for
            smoothing. Default: 500
        show : bool
            Show the plot upon completion. Default: False

        """
        style = kwargs.get('style', 'default')
        plot_settings.load_settings(style, show_info=False)
        plt.figure()
        plt.hold(True)
        if kwargs.get('show_fit', True):
            if self.use_errorbars:
                plt.errorbar(self.t, self.P, self.err, fmt='o', mfc='b', mec='b')
            else:
                plt.plot(self.t, self.P, fmt='o', mfc='b', mec='b')
            points = kwargs.get('points', 500)
            t_fit = np.linspace(self.t[0], self.t[-1], points)
            plt.plot(t_fit, self._func(t_fit, *self.p), 'r-', lw=1.5)
        else:
            plt.plot(self.t, self.P, 'o-', mfc='b', mec='b')
        plt.xlabel(r'Pulse duration [$\mu$s]')
        plt.ylabel('Excitation probability')
        plt.savefig(outfile, bbox_inches='tight')
        if kwargs.get('show', False):
            plt.show()
            
        