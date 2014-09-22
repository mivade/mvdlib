"""Plotting of arbitrary (text-based) data files."""

import os.path
from types import StringTypes
import itertools
import numpy as np
import matplotlib.pyplot as plt
from .. import plot_settings

_markers = itertools.cycle(('o', 's', 'D', '+', '^', 'v', '<', '>', '*'))

class Plotter(object):
    def __init__(self, datadir, prefix, suffix='dat', **kwargs):
        """Create a new Plotter object.

        Parameters
        ----------
        datadir : str
            Path to find data files.
        prefix : str
            Data file prefix, e.g., 'rabi_' if data files are named
            something like 'rabi_0001.csv'.
        suffix : str
            Data file extension. Default: 'dat'

        Keyword arguments
        -----------------
        columns : int
            Number of columns in the data file. This does nothing
            now. Default: 2
        labels : list
            A list of axis labels. In the future, this could be
            modified to allow for more than 2 axes.
            Default: ['', '']
        zpad : int
            Zero padding for data file names.

        """
        # Process arguments
        assert isinstance(datadir, StringTypes)
        assert os.path.exists(datadir)
        self.datadir = datadir
        assert isinstance(prefix, StringTypes)
        self.prefix = prefix
        assert isinstance(suffix, StringTypes)
        self.suffix = suffix
        self.columns = kwargs.get('columns', 2)
        assert self.columns is 2 # TODO: allow this to be changed
        self.labels = kwargs.get('labels', ['', ''])
        assert isinstance(self.labels, (list, tuple))
        assert len(self.labels) is 2 # TODO: allow this to be changed
        self.zpad = kwargs.get('zpad', 4)
        assert isinstance(self.zpad, int)

        # Setup data storage lists and labels
        self.x = []
        self.y = []
        self.legend = []

    def add_data(self, index, **kwargs):
        """Add data files to the Plotter.

        Parameters
        ----------
        index : int or list
            Add a single data file or multiple data files.

        Keyword arguments
        -----------------
        delimiter: str
            Text delimiter for data file. Default: None
        skiprows : int
            Number of rows in the data file to skip. Default: 1
        legend : str
            A legend label to give the data. If None, uses the
            filename. Default: None

        """
        # Read data
        # TODO: allow i to actually be a list
        fname = '{pre}{i:0{pad:d}d}.{suf}'.format(
            pre=self.prefix, i=index, pad=self.zpad, suf=self.suffix
        )
        delimiter = kwargs.get('delimiter', None)
        skiprows = kwargs.get('skiprows', 1)
        data = np.loadtxt(
            os.path.join(self.datadir, fname),
            delimiter=delimiter,
            skiprows=skiprows
        )
        x, y = data[:,0], data[:,1]

        # Add to list
        self.x.append(x)
        self.y.append(y)
        legend = kwargs.get('legend', None)
        if legend is None:
            legend = fname
        self.legend.append(legend)

    def plot(self, style='web', **kwargs):
        """Plot the loaded data.

        Parameters
        ----------
        style : str
            The plot style to use.

        Keyword arguments
        -----------------
        xlabel : str
            Label for the horizontal axis.
        ylabel : str
            Label for the vertical axis.
        linestyle : str
            Matplotlib linestyle specification. Default: '-'
        linewidth : float
            Line width. Default: 1.5

        """
        # Check that there's actually something to plot
        if len(self.x) == 0:
            raise ValueError("You must load data first!")
            
        # Check arguments
        assert isinstance(style, StringTypes)
        assert style in plot_settings.styles
        xlabel = kwargs.get('xlabel', '')
        assert isinstance(xlabel, StringTypes)
        ylabel = kwargs.get('ylabel', '')
        assert isinstance(ylabel, StringTypes)
        linestyle = kwargs.get('linestyle', '-')
        assert isinstance(linestyle, StringTypes)
        linewidth = kwargs.get('linewidth', 1.5)
        assert isinstance(linewidth, (int, float))

        # Plotting
        plot_settings.load_settings(style)
        plt.figure()
        plt.hold(True)
        for i in range(len(self.x)):
            plt.plot(
                self.x[i], self.y[i],
                label=self.legend[i],
                marker=_markers.next(),
                linestyle=linestyle,
                linewidth=linewidth
            )
        plt.legend()
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.hold(False)
        plt.savefig(
            os.path.join(self.datadir, 'last.svg'), bbox_inches='tight'
        )
        plt.show()
        