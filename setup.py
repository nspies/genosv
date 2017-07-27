#!/usr/bin/env python

from setuptools import setup, find_packages
from setuptools.extension import Extension

import sys

if sys.version_info < (3, 3):
    raise RuntimeError("Python version >= 3.3 required.")

def get_version(string):
    """ Parse the version number variable __version__ from a script. """
    import re
    version_re = r"^__version__ = ['\"]([^'\"]*)['\"]"
    version_str = re.search(version_re, string, re.M).group(1)
    return version_str

def get_includes():
    class Includes:
        def __iter__(self):
            import pysam
            import numpy
            return iter(pysam.get_include()+[numpy.get_include()])
        def __getitem__(self, i):
            return list(self)[i]
    return Includes()

def get_defines():
    class Defines:
        def __iter__(self):
            import pysam
            return iter(pysam.get_defines())
        def __getitem__(self, i):
            return list(self)[i]
    return Defines()

# try:
#     from Cython.Build import cythonize
extensions = [
    Extension("genosv.remap._mapq",
              sources=["genosv/remap/_mapq.pyx"],
              include_dirs=get_includes(),
              define_macros=get_defines()
              )
    ]

# except ImportError:
#     extensions = [Extension("genosv.remap._mapq",
#                             sources=["genosv/remap/_mapq.c"],
#                             include_dirs=get_includes(),
#                             define_macros=get_defines()
#                             )
#                  ]


setup(name="genosv",
      version=get_version(open('genosv/__init__.py').read()),
      description="genosv",
      author="Noah Spies",
      packages=find_packages(),
      ext_modules = extensions,
      setup_requires=["cython"],
      entry_points={"console_scripts": ["genosv = genosv.app.main:main"]},
      install_requires=["pysam>=0.10", "numpy", "pyfaidx", "tqdm", "pandas", "numpy"], 
      python_requires=">=3.3"
     )
