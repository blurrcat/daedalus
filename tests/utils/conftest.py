#!/usr/bin/env python
# -*- coding: utf-8 -*-
import importlib
import pytest


@pytest.fixture
def envvar(monkeypatch):
    monkeypatch.setenv('DAEDALUS_TEST', 'test')
    import daedalus.utils
    importlib.reload(daedalus.utils)  # make sure env var are loaded
    return 'TEST', 'test'
