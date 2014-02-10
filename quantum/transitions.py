"""
mvdlib.quantum.transitions

Miscellaneous stuff dealing with atomic transitions (e.g., converting
between inverse cm and frequency. Yeah, this mostly just involves
multiplying by c or 1/c, but sometimes factors of 2*pi are forgotten,
so this helps prevent that from happening!

"""

# TODO: Add conversions to/from eV.
# TODO: Additional testing.

from __future__ import print_function
import numpy as np
from scipy.constants import c

def wavenumber_to_frequency(wavenumber, angular=False):
    """
    Convert the wavenumber in inverse cm to frequency in Hz. If
    angular is True, return the angular frequency instead.

    """
    f = c*wavenumber*1e2
    if angular:
        return 2*np.pi*f
    else:
        return f

def wavenumber_to_wavelength(wavenumber, wl_units="nm"):
    """
    Convert the wavenumber in inverse cm to wavelength in nm, um, or
    angstroms.

    """
    lmbda = 1/wavenumber
    if wl_units == "nm":
        return lmbda*1e7
    elif wl_units == "um":
        return lmbda*1e4
    elif wl_units == "angstroms":
        return lmbda*1e8
    else:
        raise ValueError("wl_units must be nm, um, or angstroms.")

def frequency_to_wavenumber(freq, angular=False):
    """
    Convert the frequency freq into inverse cm units. If angular is
    True, freq is presumed to be an angular frequency (2*pi*f in Hz),
    otherwise the units are assumed to be Hz.

    """
    wavenumber = 1e-2*freq/c
    if angular:
        return wavenumber/(2*np.pi)
    else:
        return wavenumber

def frequency_to_wavelength(freq, wl_units="nm", angular=False):
    """
    Convert the frequency in Hz (or 2*pi*Hz if angular is True) into
    wavelength in units of nm, um, or angstroms.

    """
    lmbda = c/freq
    if angular:
        lmbda *= 2*np.pi
    if wl_units == "nm":
        return lmbda/1e-9
    elif wl_units == "um":
        return lmbda/1e-6
    elif wl_units == "angstrom":
        return lmbda/1e-10
    else:
        raise ValueError("wl_units must be nm, um, or angstroms.")

if __name__ == "__main__":
    wavenum = 25191.51 # wavenumber in 1/cm for Ca+ 397 nm transition
    print("1/lambda -> lambda:",
          wavenumber_to_wavelength(wavenum), "nm")
    print("1/lambda -> f:",
          wavenumber_to_frequency(wavenum)/1e12, "THz")

