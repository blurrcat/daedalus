#!/usr/bin/env python
# -*- coding: utf-8 -*-
from daedalus.utils import get_config, config_from_env


def test_get_config(environ):
    for prefix, k, v in environ:
        if prefix == 'DAEDALUS_':
            assert get_config(k) == v
        else:
            assert not get_config(k)


def test_config_from_env(environ):
    env_config = config_from_env()
    for prefix, k, v in environ:
        if prefix == 'DAEDALUS_':
            assert env_config[k] == v
        else:
            assert k not in env_config
