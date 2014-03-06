"""
Transitions

Conversions between different ways of describing atomic and molecular
energy levels, e.g., converting between inverse cm and
frequency. Yeah, this mostly just involves multiplying by c or 1/c,
but sometimes factors of 2*pi are forgotten, so this helps prevent
that from happening!

TODO: Additional testing.

"""

from __future__ import print_function
from __future__ import division
import numpy as np
from scipy.constants import h, c, physical_constants as consts

# Units
# -----

# Conversion factors from non-SI to SI
_wl_units = {'nm': 1e-9, 'um': 1e-6, 'angstrom': 1e-10}
_f_units = {'Hz': 1.0, 'kHz': 1e3, 'MHz': 1e6, 'GHz': 1e9 'THz': 1e12}
_E_units = {'eV': consts['electron volt'][0], 'J': 1.0}

# TODO: Eventually I'll make this into its own class.
UnitsError = ValueError

# Error messages
# --------------

def _units_err_msg(measure):
    """
    Return a string with an error message appropriate to whichever
    units were incorrect.
    
    """
    if measure == 'wl':
        units = _wl_units
        name = "Wavelength"
    elif measure == 'f':
        units = _f_units
        name = "Frequency"
    elif measure == 'E':
        units = _E_units
        name = "Energy"
    return name + "must be one of: " + str(units.keys())

# Functions
# ---------

def wavenumber_to_frequency(wavenumber, f_units="THz"):
    """
    Convert the wavenumber in inverse cm to frequency.

    Parameters
    ----------
    wavenumber : float
        The wavenumber in inverse cm to convert.

    Returns
    -------
    f : float
        Calculated frequency.

    See Also
    --------
    wavenumber_to_wavelength
    frequency_to_wavenumber

    """
    f_SI = c*wavenumber*1e2
    try:
        f = f_SI/_f_units[f_units]
    except KeyError:
        raise UnitsError(_units_err_msg('f'))
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

def frequency_to_wavenumber(freq, f_units='Hz'):
    """
    Convert the frequency freq into a wavenumber.

    Parameters
    ----------
    freq : float
        The frequency to convert.

    Returns
    -------
    wavenumber : float
        The calculated wavenumber.

    See Also
    --------
    frequency_to_wavelength
    wavenumber_to_frequency

    """
    freq *= _f_units[f_units]
    wavenumber = 1e-2*freq/c
    return wavenumber

def frequency_to_wavelength(freq, f_units="THz", wl_units="nm"):
    """
    Convert the frequency freq to wavelength.

    Parameters
    ----------
    freq : float
        The frequency to convert.
    wl_units : str, optional
        Units the wavelength is given in.    

    Returns
    -------
    lmbda : float
        The calculated wavelength.

    """
    try:
        f_SI = freq*_f_units[f_units]
    except KeyError:
        raise UnitsError(_units_err_msg('f'))
    lmbda_SI = c/f_SI
    try:
        lmbda = lmbda_SI/_wl_units[wl_units]
    except KeyError:
        raise UnitsError(_units_err_msg('wl'))
    return lmbda

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
        raise UnitsError(_units_err_msg('f'))
    E_SI = h*f_SI
    try:
        E = E_SI/E_units
    except KeyError:
        raise UnitsError(_units_err_msg('E'))
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
        raise UnitsError(_units_err_msg('wl'))
    f_SI = c/wl_SI
    try:
        f = f_SI/_f_units[f_units]
    except KeyError:
        raise UnitsError(_units_err_msg('f'))
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
        raise UnitsError(_units_err_msg('wl'))
    try:
        E = E_SI/_E_units[E_units]
    except KeyError:
        raise UnitsError(_units_err_msg('E'))
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
        raise UnitsError(_units_err_msg('E'))
    f_SI = E_SI/h
    try:
        f = f_SI/_f_units[f_units]
    except KeyError:
        raise UnitsError(_units_err_msg('f'))
    return f

if __name__ == "__main__":
    wavenum = 25191.51 # wavenumber in 1/cm for Ca+ 397 nm transition
    wavelength = wavenumber_to_wavelength(wavenum, "nm")
    freq = wavenumber_to_frequency(wavenum, "THz")
    energy = wavelength_to_energy(wavelength, E_units="eV")

    print("1/lambda -> lambda:", wavelength, "nm")
    print("1/lambda -> f:", freq, "THz")
    print("lambda -> eV:", energy, "eV")

    freq = energy_to_frequency(energy, f_units="GHz", E_units="eV")
    
    print("eV -> MHz:", freq, "MHz")
