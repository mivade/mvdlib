"""
Plotting with different styles made easier by allowing for loading of
seettings from JSON files.

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
            rc_params = json.load(json_file)
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

