#!/usr/bin/env python
# -*- coding: utf-8 -*-
from functools import partial
from redis import StrictRedis
from daedalus.worker.docker_build import Docker
from daedalus.utils import get_config
from daedalus.redis_log import RedisLog


def build_from_git(
        id, url, username=None, password=None, commit='master', version=None):
    redis = StrictRedis.from_url(get_config('REDIS_URL'))
    redis_log = RedisLog(
        connection=redis,
        ttl=get_config('REDIS_LOG_TTL'),
        prefix=get_config('REDIS_LOG_PREFIX'),
    )
    docker = Docker(
        registry=get_config('DOCKER_REGISTRY'),
        username=get_config('DOCKER_REGISTRY_USERNAME'),
        password=get_config('DOCKER_REGISTRY_PASSWORD'),
        nocache=get_config('DOCKER_BUILD_NOCACHE'),
        assert_hostname=get_config('DOCKER_ASSERT_HOSTNAME'),
        log_handler=partial(redis_log.append, id),
        api_version=get_config('DOCKER_API_VERSION'),
    )
    return docker.build_from_git(url, username, password, commit, version)
