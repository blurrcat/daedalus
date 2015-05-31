#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pytest
from daedalus.web.main import create_app


@pytest.fixture
def app(request):
    a = create_app()
    a.config.debug = True
    a.config.testing = True
    context = a.app_context()
    context.push()

    request.addfinalizer(context.pop)
    return a
