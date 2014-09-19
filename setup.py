from distutils.core import setup
from mvdlib import __version__ as version

setup(
    name="mvdlib",
    version=version,
    packages=(
        'mvdlib',
        'mvdlib.analysis',
        'mvdlib.optics',
        'mvdlib.plot_settings'
        'mvdlib.quantum',
    ),
    package_data={
        '': ['*.json'],
    },
    author="Michael V. DePalatis",
    author_email="depalatis@phys.au.dk",
    description="A collection of assorted things I find useful.",
    license="GPL 3.0",
    keywords="personal library",
    url="https://github.com/mivade/mvdlib",
    requires=(
        "numpy",
        "scipy",
        "matplotlib"
    )
)
