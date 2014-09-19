# -*- coding: utf-8 -*-
"""Utilities for combining data files to build statistics with nice
error bars. Outputs data to a text-delimited format for easy use in
other programs.

TODO:

 * More Numpythonic summing/stdeving?

"""

import os.path
import numpy as np
import matplotlib.pyplot as plt
from types import NoneType, StringTypes

class CombinationError(Exception):
    pass

class Combiner(object):
    """Combines and outputs data."""
    def __init__(self, datadir, prefix, **kwargs):
        """Set up the Combiner.

        Parameters
        ----------
        datadir : str
            Directory where data files are stored.
        prefix : str
            String prefixing data files.

        Keyword arguments
        -----------------
        zpad : int
            Zero padding to use for indeces. Default: 4
        suffix : str
            Data file filename extension. Default: 'dat'
        delimiter : str or None
            Data file text delimiter. Default: None
        skiprows : int
            Skip the first skiprows rows. Default: 0

        """
        # Get and check arguments
        self.datadir = datadir
        assert isinstance(self.datadir, (str, unicode))
        if self.datadir == '.':
            self.datadir = os.path.abspath(os.path.curdir)
        self.prefix = prefix
        assert isinstance(self.prefix, (str, unicode))
        self.zpad = kwargs.get('zpad', 4)
        assert isinstance(self.zpad, int)
        self.suffix = kwargs.get('suffix', 'dat')
        assert isinstance(self.suffix, (str, unicode))
        self.delimiter = kwargs.get('delimiter', None)
        assert isinstance(self.delimiter, (str, unicode, NoneType))
        self.skiprows = kwargs.get('skiprows', 0)
        assert isinstance(self.skiprows, int)

        # Set data to None
        self.xdata = None
        self.ydata = None
        self.yerr = None

    def combine(self, indeces, plot=False):
        """Combine data files by averaging.

        Parameters
        ----------
        indeces : list
            List of indeces to use for data file names.
        plot : bool
            Plot the data (for testing mostly).

        Returns
        -------
        xdata : np.ndarray
            Array containing the independent variables.
        ydata : np.ndarry
            Array containing the averaged dependent variables.
        yerr : np.ndarray
            Array containing the standard deviation of the dependent
            variables.

        """
        # Load and combine data
        xdata, ydata = [], []
        self.indeces = indeces
        for i in indeces:
            fname = '{pre}{num:0{width}d}.{suf}'.format(
                pre=self.prefix, num=i,
                width=self.zpad, suf=self.suffix
            )
            fname = os.path.join(self.datadir, fname)
            x, y = np.loadtxt(
                fname, skiprows=self.skiprows,
                delimiter=self.delimiter, unpack=True
            )
            if len(xdata) != 0:
                if not np.in1d(xdata[0], x).all():
                    raise CombinationError("x data must all be identical")
            xdata.append(x)
            ydata.append(y)

        # Find the standard deviation and average
        xdata = np.array(xdata)
        ydata = np.array(ydata)
        self.yerr = [np.std(ydata[:,i]) for i in range(ydata.shape[1])]
        self.xdata = xdata[0]
        ydata = [np.sum(ydata[:,i]) for i in range(ydata.shape[1])]
        self.ydata = np.array(ydata)/len(indeces)

        # Plot if requested and return
        if plot:
            plt.errorbar(self.xdata, self.ydata, self.yerr)
            plt.show()
        return self.xdata, self.ydata, self.yerr

    def write(self, location='.', readme='', header='', **kwargs):
        """Write the combined data to a file. Additionally, write a
        README file which contains information on where the raw data
        came from and anything else the user desires.

        Parameters
        ----------
        location : str
            Directory to write the data and README file to. Default: '.'
        readme : str
            Additional text to write to the README file. Default: ''
        header : list or None
            Length 3 list of strings to label the resulting data
            columns. Default: ''

        """
        # Verify data exists
        if self.xdata is None:
            raise CombinationError("You must combine data first!")
        
        # Determine output file name
        assert isinstance(location, StringTypes)
        if location == '.':
            location = os.path.abspath(os.path.curdir)
        basename = '{pre}_combined_{i:0{zpad}d}.csv'
        i = 1
        while True:
            outfile = os.path.join(
                location, basename.format(
                    pre=self.prefix, zpad=self.zpad, i=i
                )
            )
            if not os.path.exists(outfile):
                break
            i += 1

        # Generate header
        header = '{},{},{}'.format(header[0], header[1], header[2])

        # Write data
        np.savetxt(
            outfile,
            np.transpose([self.xdata, self.ydata, self.yerr]),
            delimiter=',',
            header=header,
            fmt=kwargs.get('fmt', '%f')
        )        
        
        # README output
        readme_fname = os.path.join(
            location, outfile[:-4] + '.README.txt'
        )
        readme = (
            'Data directory: {}\n'.format(self.datadir),
            'Data prefix: {}\n'.format(self.prefix),
            'Data indeces {}\n'.format(str(self.indeces)),
            '\n', readme
        )
        with open(readme_fname, 'w') as out:
            out.writelines(readme)
        return outfile

if __name__ == "__main__":
    data = Combiner('/home/mvd/tmp/20140918', 'rabi_', skiprows=1)
    #data.write('/tmp')
    data.combine(range(6, 11), plot=True)
    data.write('/tmp', 'Testing readme', ['xdata', 'ydata', 'err'])
    