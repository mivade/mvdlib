"""
misc.py

Miscellaneous utility functions that don't fit anywhere else.

"""

import numpy as np

def remove_offset(data):
    """Makes the minimum value of data be zero."""
    return data - np.min(data)

def normalize(data):
    """Normalizes data by dividing by the maximum value."""
    return data/np.max(data)

def fix_offset_and_normalize(data):
    """Removes dc offsets and normalizes data."""
    offset = remove_offset(data)
    return normalize(offset)
