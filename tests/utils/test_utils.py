#!/usr/bin/env python
# -*- coding: utf-8 -*-


def test_envvar(envvar):
    from daedalus.utils import get_config
    k, v = envvar
    assert get_config(k) == v
