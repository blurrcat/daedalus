#!/usr/bin/env python
# -*- coding: utf-8 -*-
from daedalus.utils import get_config


def test_build(
        mock_login, mock_command, mock_build, mock_push, mock_redis_log,
        registry_config):
    from daedalus.worker.jobs import build_from_git
    u, p, r = 'username', 'password', 'localhost'
    image, image_id = build_from_git(
        id='build-test',
        url='https://bitbucket.com/blurrcat/daedalus.git',
        username=u, password=p, version='latest',
    )
    assert image == '{}/{}/daedalus:latest'.format(
        get_config('DOCKER_REGISTRY'), get_config('DOCKER_REGISTRY_USERNAME'))
    assert image_id == mock_build
