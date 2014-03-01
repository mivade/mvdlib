"""
Plotting with different styles made easier by allowing for loading of
seettings from JSON files.

The _decode_list and _decode_dict functions are used to address a bug
in matplotlib when encountering unicode strings (probably fixed in
newer versions than what are in Debian wheezy). They come directly
from `this link`__

__ http://stackoverflow.com/a/6633651

"""

from __future__ import print_function
import os.path
import json
import matplotlib.pyplot as plt

_path = os.path.dirname(__file__)
_styles = {
    "default": _path + "/mpl_default.json",
    "test": _path + "/test.json",
    "latex": _path + "/latex.json",
    "aps": _path + "/aps.json"
    }

def _decode_list(data):
    rv = []
    for item in data:
        if isinstance(item, unicode):
            item = item.encode('utf-8')
        elif isinstance(item, list):
            item = _decode_list(item)
        elif isinstance(item, dict):
            item = _decode_dict(item)
        rv.append(item)
    return rv
        
def _decode_dict(data):
    rv = {}
    for key, value in data.iteritems():
        if isinstance(key, unicode):
            key = key.encode('utf-8')
        if isinstance(value, unicode):
            value = value.encode('utf-8')
        elif isinstance(value, list):
            value = _decode_list(value)
        elif isinstance(value, dict):
            value = _decode_dict(value)
        rv[key] = value
    return rv
    
def load_settings(style="default", show_info=True):
    """
    Loads the matplotlib settings from a file. The file does not need
    to define all rc parameters, but only the ones that should be
    different from the defaults.

    Parameters
    ----------
    style : str, optional
        Plotting style to use. If not given, matplotlib defaults will
        be used.
    show_info : bool, optional
        If True, print the comment string from the JSON file.

    """
    try:
        with open(_styles[style], 'r') as json_file:
            rc_params = json.load(json_file, object_hook=_decode_dict)
    except KeyError:
        print("style must be one of", _styles.keys())
    try:
        comment = rc_params.pop("comment")
        if show_info:
            print("PLOT SETTINGS INFO:", comment)
    except KeyError:
        pass
    finally:
        plt.rcParams.update(rc_params)

load_settings()

