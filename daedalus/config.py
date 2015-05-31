#!/usr/bin/env python
# -*- coding: utf-8 -*-
DEBUG = False
SECRET = '123'
REDIS_URL = 'redis://127.0.0.1'

# docker client
DOCKER_ASSERT_HOSTNAME = False
DOCKER_API_VERSION = None

# docker registry
DOCKER_REGISTRY = 'tutum.co'
# DOCKER_REGISTRY_USERNAME = ''
# DOCKER_REGISTRY_PASSWORD = ''

DOCKER_BUILD_NOCACHE = False

# redis log
REDIS_LOG_TTL = 3600
REDIS_LOG_PREFIX = 'log'

# rq
QUEUES = ['build']
RQ_JOB_TIMEOUT_BUILD = 1200  # 20min
