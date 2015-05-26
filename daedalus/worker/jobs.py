#!/usr/bin/env python
# -*- coding: utf-8 -*-
from functools import partial
from daedalus.worker.docker_build import Docker
from daedalus.utils import get_config
from daedalus.redis_log import RedisLog


def build_from_git(
        bid, url, username=None, password=None, commit='master', version=None):
    redis_log = RedisLog(
        redis_url=get_config('REDIS_URL'),
        ttl=get_config('REDIS_LOG_TTL'),
    )
    docker = Docker(
        bid=bid,
        registry=get_config('DOCKER_REGISTRY'),
        username=get_config('DOCKER_REGISTRY_USERNAME'),
        password=get_config('DOCKER_REGISTRY_PASSWORD'),
        nocache=get_config('DOCKER_BUILD_NOCACHE'),
        assert_hostname=get_config('DOCKER_ASSERT_HOSTNAME'),
        log_handler=partial(redis_log.append, bid)
    )
    docker.build_from_git(url, username, password, commit, version)
