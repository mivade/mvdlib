"""Plot utilities

The _decode_list and _decode_dict functions are used to address a bug
in matplotlib when encountering unicode strings (probably fixed in
newer versions than what are in Debian wheezy). They come directly
from `this link`__

__ http://stackoverflow.com/a/6633651

"""

from __future__ import print_function
import os
import os.path
import shutil
import tempfile
import subprocess
import json
import matplotlib.pyplot as plt

_path = os.path.join(os.path.dirname(__file__), 'styles')
styles = {
    "default": _path + "/mpl_default.json",
    "test": _path + "/test.json",
    "latex": _path + "/latex.json",
    "aps": _path + "/aps.json",
    "ipython": _path + "/ipython.json",
    "presentation": _path + "/presentation.json",
    "poster": _path + "/poster.json",
    "web": _path + "/web.json"
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

def set_style(style="default", show_info=True):
    """Loads the matplotlib settings from a file. The file does not
    need to define all rc parameters, but only the ones that should be
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
        with open(styles[style], 'r') as json_file:
            rc_params = json.load(json_file, object_hook=_decode_dict)
    except KeyError:
        print("style must be one of", styles.keys())
    try:
        comment = rc_params.pop("comment")
        if show_info:
            print("PLOT SETTINGS INFO:", comment)
    except KeyError:
        pass
    finally:
        plt.rcParams.update(rc_params)

_export_formats = ['pdf']
_tex = r"""\documentclass{{standalone}}
\usepackage{{pgf}}
{preamble}
\begin{{document}}
\input{{{fig:s}}}
\end{{document}}
"""
def pgfsave(filename, **kwargs):
    """Use the matplotlib pgf backend to render the figure and save it
    as an image file.

    Keyword arguments
    -----------------
    format: str
        For now, limited to 'pdf'.
    preamble : list
        List of strings to use as the pgf preamble.

    """
    format = kwargs.get('format', 'pdf')
    assert format in _export_formats
    assert isinstance(filename, (str, unicode))
    texcmd = 'xelatex'
    preamble = kwargs.get('preamble', [])
    assert isinstance(preamble, (list, tuple))

    # Temporarily turn off rc fonts
    rc = plt.rcParams
    plt.rcParams['pgf.rcfonts'] = False

    # Compile the figure
    prefix = filename[:-3]
    tmp = tempfile.gettempdir()
    pgf_file = os.path.join(tmp, prefix + 'pgf')
    tex_file = os.path.join(tmp, prefix + 'tex')
    pdf_file = os.path.join(tmp, prefix + 'pdf')
    plt.savefig(pgf_file, bbox_inches='tight')
    with open(tex_file, 'w') as out:
        out.write(_tex.format(preamble=('\n'.join(preamble)), fig=prefix + 'pgf'))
    if subprocess.check_call([texcmd, os.path.basename(tex_file)], cwd=tmp):
        raise RuntimeError("Error when processing LaTeX.")
    os.rename(pdf_file, os.path.join(os.getcwd(), prefix + 'pdf'))

    # Restore rcParams
    plt.rcParams = rc
    
