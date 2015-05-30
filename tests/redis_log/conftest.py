#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pytest
from daedalus.redis_log import RedisLog
from daedalus.utils import get_config


@pytest.fixture
def redis_log(request):
    log = RedisLog(get_config('REDIS_URL'))
    request.addfinalizer(log.redis.flushdb)
    return log
