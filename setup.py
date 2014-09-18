from setuptools import setup, find_packages
from mvdlib import __version__ as version

setup(
    name="mvdlib",
    version=version,
    packages=find_packages(),
    package_data={
        '': ['*.json'],
    },
    author="Michael V. DePalatis",
    author_email="depalatis@phys.au.dk",
    description="A collection of assorted things I find useful.",
    license="GPL 3.0",
    keywords="personal library",
    url="https://github.com/mivade/mvdlib",
    install_requires=(
        "numpy",
        "scipy",
        "matplotlib"
    )
)
