#!/usr/bin/env python
# -*- coding: utf-8 -*-
import ast
import os
import tempfile
import time
import shutil
from daedalus import config


class TempDirectory(object):
    """
    Create a temporary directory.
    """
    DIR = tempfile.gettempdir()

    def __init__(self, name='', chdir=True, clean=True):
        self.d = os.path.join(self.DIR, name, str(time.time()))
        self.chdir = chdir
        self.clean = clean
        self.old_cwd = os.getcwd()

    def __enter__(self):
        os.makedirs(self.d)
        if self.chdir:
            os.chdir(self.d)
        return self.d

    def __exit__(self, type, value, tb):
        if self.clean:
            shutil.rmtree(self.d)
        if self.chdir:
            os.chdir(self.old_cwd)


def get_config(k, default=None, prefix='DAEDALUS_'):
    v = os.environ.get('{}{}'.format(prefix, k))
    if v:
        try:
            return ast.literal_eval(v)
        except (ValueError, SyntaxError):
            return v
    else:
        return getattr(config, k, default)
