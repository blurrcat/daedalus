#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pytest
from redis import StrictRedis
from daedalus.redis_log import RedisLog
from daedalus.utils import get_config


@pytest.fixture
def redis_log(request):
    log = RedisLog(StrictRedis.from_url(get_config('REDIS_URL')))
    request.addfinalizer(log.redis.flushdb)
    return log
