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


def config_from_env(prefix, show=False):
    result = {}
    offset = len(prefix)
    for k, v in os.environ.items():
        if k.startswith(prefix):
            k = k[offset:]
            try:
                v = ast.literal_eval(v)
            except (ValueError, SyntaxError):
                pass
            result[k] = v
    if show:
        print('override from env: ')
        for k, v in result.items():
            print('{}={}'.format(k, v))
    return result


def config_from_obj(config_obj):
    conf = {}
    for k in dir(config_obj):
        if k.isupper():
            conf[k] = getattr(config_obj, k)
    return conf


_config = config_from_obj(config)
# production config via env vars
_config.update(config_from_env('DAEDALUS_'))


def get_config(k=None, default=None):
    if not k:
        return _config
    return _config.get(k, default)
