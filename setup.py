# Copyright (C) 2015-2020 by the RBniCS authors
#
# This file is part of RBniCS.
#
# SPDX-License-Identifier: LGPL-3.0-or-later

from setuptools import find_packages, setup

setup(name="RBniCS",
      description="Reduced order modelling in FEniCS",
      long_description="Reduced order modelling in FEniCS",
      author="Francesco Ballarin (and contributors)",
      author_email="francesco.ballarin@sissa.it",
      version="0.1.dev1",
      license="GNU Library or Lesser General Public License (LGPL)",
      url="http://mathlab.sissa.it/rbnics",
      classifiers=[
          "Development Status :: 3 - Alpha",
          "Intended Audience :: Developers",
          "Intended Audience :: Science/Research",
          "Programming Language :: Python :: 3",
          "Programming Language :: Python :: 3.4",
          "Programming Language :: Python :: 3.5",
          "Programming Language :: Python :: 3.6",
          "License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)",
          "Topic :: Scientific/Engineering :: Mathematics",
          "Topic :: Software Development :: Libraries :: Python Modules",
      ],
      packages=find_packages(),
      include_package_data=True,
      install_requires=[
          "cvxopt>=1.2.0",
          "mpi4py",
          "multipledispatch>=0.5.0",
          "pylru",
          "pytest-runner",
          "sympy>=1.0",
          "toposort"
      ],
      tests_require=[
          "pytest",
          "pytest-benchmark",
          "pytest-dependency",
          "pytest-flake8",
          "pytest-html",
          "pytest-instafail",
          "pytest-xdist"
      ],
      zip_safe=False
      )
