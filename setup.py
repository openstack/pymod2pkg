from __future__ import with_statement

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

import pymod2pkg

pymod2pkg_classifiers = [
    "Programming Language :: Python :: 2",
    "Programming Language :: Python :: 3",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: Apache Software License",
    "Topic :: Software Development :: Libraries",
    "Topic :: Utilities",
]

with open("README.rst", "r") as fp:
    pymod2pkg_long_description = fp.read()

setup(name="pymod2pkg",
      version=pymod2pkg.__version__,
      author="Jakub Ruzicka",
      author_email="jruzicka@fedorapeople.org",
      url="https://github.com/openstack/pymod2pkg",
      py_modules=["pymod2pkg"],
      description="python module name to package name map",
      long_description=pymod2pkg_long_description,
      classifiers=pymod2pkg_classifiers,
      license="Apache License, Version 2.0",
      )
