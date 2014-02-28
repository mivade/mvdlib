"""
mvdlib.quantum.transitions

Miscellaneous stuff dealing with atomic transitions (e.g., converting
between inverse cm and frequency. Yeah, this mostly just involves
multiplying by c or 1/c, but sometimes factors of 2*pi are forgotten,
so this helps prevent that from happening!

TODO: Additional testing.
TODO: Convert to using the _x_units dicts for everything

"""

from __future__ import print_function
from __future__ import division
import numpy as np
from scipy.constants import h, c, physical_constants as consts

# Units
# -----

# Conversion factors from non-SI to SI
_wl_units = {'nm': 1e-9, 'um': 1e-6, 'angstrom': 1e-10}
_f_units = {'Hz': 1.0, 'kHz': 1e3, 'MHz': 1e6, 'THz': 1e12}
_E_units = {'eV': consts['electron volt'][0], 'J': 1.0}

# Error messages
# --------------

def _units_err_msg(measure):
    if measure == 'wl':
        units = _wl_units
        name = "Wavelength"
    elif measure == 'f':
        units = _f_units
        name = "Frequency"
    elif measure == 'E':
        units = _E_units
        name = "Energy"
    print(name, "must be one of:", units.keys())

# Functions
# ---------

def wavenumber_to_frequency(wavenumber, angular=False):
    """
    Convert the wavenumber in inverse cm to frequency.

    Parameters
    ----------
    wavenumber : float
        The wavenumber to convert.
    angular : bool
        If True, return an angular frequency instead of an ordinary
        frequency.

    Returns
    -------
    f : float
        Calculated frequency.

    See Also
    --------
    wavenumber_to_wavelength
    frequency_to_wavenumber

    """
    f = c*wavenumber*1e2
    if angular:
        return 2*np.pi*f
    else:
        return f

def wavenumber_to_wavelength(wavenumber, wl_units="nm"):
    """
    Convert the wavenumber in inverse cm to wavelength.

    Parameters
    ----------
    wavenumber : float
        The wavenumber to convert.
    wl_units : str, optional
        Desired units for the resulting wavelength.

    Returns
    -------
    lmbda : float
        Calculated wavelength.

    See Also
    --------
    wavenumber_to_frequency

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
    Convert the frequency freq into a wavenumber.

    Parameters
    ----------
    freq : float
        The frequency to convert.
    angular : bool, optional
        If True, return an angular frequency instead of an ordinary
        frequency.

    Returns
    -------
    wavenumber : float
        The calculated wavenumber.

    See Also
    --------
    frequency_to_wavelength
    wavenumber_to_frequency

    """
    wavenumber = 1e-2*freq/c
    if angular:
        return wavenumber/(2*np.pi)
    else:
        return wavenumber

def frequency_to_wavelength(freq, wl_units="nm", angular=False):
    """
    Convert the frequency freq to wavelength.

    Parameters
    ----------
    freq : float
        The frequency to convert.
    wl_units : str, optional
        Units the wavelength is given in.    
    angular : bool, optional
        If True, return an angular frequency instead of an ordinary
        frequency.

    Returns
    -------
    lmbda : float
        The calculated wavelength.

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

def frequency_to_energy(freq, f_units="THz", E_units="eV"):
    """
    Convert a frequency to an energy.

    Parameters
    ----------
    freq : float
        Frequency.
    f_units : str, optional
        Units the frequency is given in.
    E_units : str, optional
        Units for the returned energy value.

    Returns
    -------
    E : float
        The energy corresponding to the given wavelength.

    """
    try:
        f_SI = freq*_f_units[f_units]
    except KeyError:
        _units_err_msg('f')
    E_SI = h*f_SI
    try:
        E = E_SI/E_units
    except KeyError:
        _units_err_msg('E')
    return E

def wavelength_to_frequency(wl, wl_units="nm", f_units="THz"):
    """
    Convert a wavelength to frequency.

    Parameters
    ----------
    wl : float
        Wavelength.
    wl_units : str, optional
        Units the wavelength is given in.
    f_units : str, optional
        Units for the returned frequency value.

    Returns
    -------
    f : float
        The frequency corresponding to the given wavelength.

    """
    try:
        wl_SI = wl*_wl_units[wl_units]
    except KeyError:
        _units_err_msg('wl')
    f_SI = c/wl_SI
    try:
        f = f_SI/_f_units[f_units]
    except KeyError:
        _units_err_msg('f')
    return f


def wavelength_to_energy(wl, wl_units="nm", E_units="eV"):
    """
    Convert a wavelength to energy.

    Parameters
    ----------
    wl : float
        Wavelength.
    wl_units : str, optional
        Units the wavelength is given in.
    E_units : str, optional
        Units for the returned energy value.

    Returns
    -------
    E : float
        The energy corresponding to the given wavelength.

    """
    try:
        E_SI = h*c/(wl*_wl_units[wl_units])
    except KeyError:
        _units_err_msg('wl')
    try:
        E = E_SI/_E_units[E_units]
    except KeyError:
        _units_err_msg('E')
    return E

def energy_to_frequency(E, E_units="eV", f_units="THz"):
    """
    Convert energy to frequency.

    Parameters
    ----------
    E : float
        Energy.
    E_units : str, optional
        Units the energy is given in.
    f_units : str, optional
        Units for the returned frequency value.

    Returns
    -------
    f : float
        The frequency corresponding to the given energy.

    """
    try:
        E_SI = E*_E_units[E_units]
    except KeyError:
        _units_err_msg('E')
    f_SI = E_SI/h
    try:
        f = f_SI/_f_units[f_units]
    except KerError:
        _units_err_msg('f')
    return f

if __name__ == "__main__":
    wavenum = 25191.51 # wavenumber in 1/cm for Ca+ 397 nm transition
    print("1/lambda -> lambda:",
          wavenumber_to_wavelength(wavenum), "nm")
    print("1/lambda -> f:",
          wavenumber_to_frequency(wavenum)/1e12, "THz")

    lam = 397.
    print("lambda -> eV:",
          wavelength_to_energy(lam), "eV")

