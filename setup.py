#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    Setup file for eflute.

    This file was generated with PyScaffold 2.5.2, a tool that easily
    puts up a scaffold for your new Python project. Learn more under:
    http://pyscaffold.readthedocs.org/
"""
import os
import sys
from distutils.sysconfig import get_python_inc

import numpy as np
from Cython.Distutils import build_ext

from setuptools import setup, Extension


def setup_package():
    py_inc = [get_python_inc()]

    np_lib = os.path.dirname(np.__file__)
    np_inc = [os.path.join(np_lib, 'core/include')]
    folder_path = "utilFunctions_C/"
    sourcefiles = [folder_path + "utilFunctions.c", folder_path + "cutilFunctions.pyx"]

    needs_sphinx = {'build_sphinx', 'upload_docs'}.intersection(sys.argv)
    sphinx = ['sphinx'] if needs_sphinx else []
    setup(setup_requires=['six', 'pyscaffold>=2.5a0,<2.6a0'] + sphinx,
          use_pyscaffold=True,
          cmdclass={'build_ext': build_ext},
          ext_modules=[Extension("utilFunctions_C", sourcefiles, libraries=['m'], include_dirs=py_inc + np_inc)])


if __name__ == "__main__":
    setup_package()
