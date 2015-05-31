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


def _parse_var(v):
    try:
        return ast.literal_eval(v)
    except (ValueError, SyntaxError):
        return v


def get_config(key, default=None, prefix='DAEDALUS_'):
    """
    Get configuration value of key. This tries to load the value of key from
    environment variables; if not found then try config file
    :param key: item to get
    :param default: default value to return if key is not found
    :param prefix: prefix of environment variables
    :return:
    """
    v = os.environ.get('{}{}'.format(prefix, key))
    if v:
        return _parse_var(v)
    else:
        return getattr(config, key, default)


def config_from_env(prefix='DAEDALUS_'):
    """
    Load all environment variables prefixed by `prefix`
    """
    l = len(prefix)
    conf = {}
    for k, v in os.environ.items():
        if k.startswith(prefix):
            conf[k[l:]] = _parse_var(v)
    return conf
