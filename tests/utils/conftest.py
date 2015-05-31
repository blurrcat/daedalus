#!/usr/bin/env python
# -*- coding: utf-8 -*-
import importlib
import pytest


@pytest.fixture
def environ(monkeypatch):
    env = (
        ('DAEDALUS_', 'KEY1', 'value'),
        ('DAEDALUS_', 'KEY2', 'value'),
        ('', 'KEY3', 'value')
    )
    for prefix, k, v in env:
        monkeypatch.setenv('{}{}'.format(prefix, k), v)
    return env
