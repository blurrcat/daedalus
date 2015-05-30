#!/usr/bin/env python
# -*- coding: utf-8 -*-
from docker.errors import APIError
from mock import Mock
import pytest
from daedalus.worker.docker_build import Docker


@pytest.fixture
def mock_login_failure(monkeypatch):
    mock = Mock(side_effect=APIError('login failed', None, '401'))
    monkeypatch.setattr('docker.client.Client.login', mock)
    return mock


@pytest.fixture
def mock_login(monkeypatch):
    monkeypatch.setattr(
        'docker.client.Client.login', lambda *args, **kwargs: True)


@pytest.fixture
def mock_builder():
    return Docker('1', 'localhost')


@pytest.fixture
def mock_command(monkeypatch):
    def run_command(*commands):
        for c in commands:
            yield '$ {}'.format(c)
            yield 'ok'
    monkeypatch.setattr(
        'daedalus.worker.docker_build.Docker._run_command', run_command)


@pytest.fixture
def mock_build(monkeypatch):
    def build(*args, **kwargs):
        for msg in [
            '{"stream":" ---\\u003e a9eb17255234\\n"}',
            '{"stream":"Step 1 : MAINTAINER first last\\n"}',
            '{"stream":" ---\\u003e Running in 08787d0ee8b1\\n"}',
            '{"stream":" ---\\u003e 23e5e66a4494\\n"}',
            '{"stream":"Removing intermediate container 08787d0ee8b1\\n"}',
            '{"stream":"Step 2 : VOLUME /data\\n"}',
            '{"stream":" ---\\u003e Running in abdc1e6896c6\\n"}',
            '{"stream":" ---\\u003e 713bca62012e\\n"}',
            '{"stream":"Removing intermediate container abdc1e6896c6\\n"}',
            '{"stream":"Step 3 : CMD [\\"/bin/sh\\"]\\n"}',
            '{"stream":" ---\\u003e Running in dba30f2a1a7e\\n"}',
            '{"stream":" ---\\u003e 032b8b2855fc\\n"}',
            '{"stream":"Removing intermediate container dba30f2a1a7e\\n"}',
            '{"stream":"Successfully built 032b8b2855fc\\n"}',
        ]:
            yield msg.encode('utf-8')

    monkeypatch.setattr(
        'docker.client.Client.build', build
    )
    return '032b8b2855fc'


@pytest.fixture
def mock_push(monkeypatch):
    def push(*args, **kwargs):
        for msg in [
            '{"status":"Pushing repository yourname/app (1 tags)"}',
            '{"status":"Pushing","progressDetail":{},"id":"511136ea3c5a"}',
            '{"status":"Image already pushed, skipping","progressDetail"' +
            ':{}, "id":"511136ea3c5a"}',
            '{"status":"Pushing tag for rev [918af568e6e5] on {https:' +
            '//cdn-registry-1.docker.io/v1/repositories/yourname/app/' +
            'tags/latest}"}',
        ]:
            yield msg.encode('utf-8')

    monkeypatch.setattr(
        'docker.client.Client.push', push
    )


@pytest.fixture
def registry_config(monkeypatch):
    for k, v in {
        'DOCKER_REGISTRY': 'localhost',
        'DOCKER_REGISTRY_USERNAME': 'u',
        'DOCKER_REGISTRY_PASSWORD': 'p',
    }.items():
        monkeypatch.setenv('DAEDALUS_{}'.format(k), v)


@pytest.fixture
def mock_redis_log(monkeypatch):
    mock = Mock()
    monkeypatch.setattr('daedalus.redis_log.RedisLog', mock)
    return mock
