#! /usr/bin/env python
# -*- coding: utf-8 -*-
import subprocess
from daedalus.worker.docker_build import Docker
from docker.errors import APIError
import pytest


def test_login(mock_builder, mock_login_failure):
    with pytest.raises(RuntimeError):
        mock_builder.login_registry('user', 'pass', 'localhost')


def test_set_auth(mock_builder):
    username, password = 'user', 'pass'
    # auth passed via url or username/password are the same
    for args in ((
        'https://github.com/test/repo.git', username, password
    ), (
        'https://{}@github.com/test/repo.git'.format(username), None, password
    ), (
        'https://{}:{}@github.com/test/repo.git'.format(username, password),
        None, None
    )):
        url, u, p = mock_builder._set_auth(*args)
        assert url == 'https://{}:{}@github.com/test/repo.git'.format(
            username, password)
        assert u == username
        assert p == password


def test_parse_reponame(mock_builder):
    name = mock_builder._parse_repo('https://github.com/blurrcat/daedalus.git')
    assert name == 'daedalus'
    with pytest.raises(ValueError):
        mock_builder._parse_repo('https://github.com/blurrcat/daedalus')


def test_parse_image_id(mock_builder):
    image_id = mock_builder._parse_image_id(
        'Successfully built 032b8b2855fc\\n')
    assert image_id == '032b8b2855fc'
    assert not mock_builder._parse_image_id('Failed to build image\\n')


def test_build(mock_builder, mock_login, mock_command, mock_build, mock_push):
    u, p, r = 'username', 'password', 'localhost'
    mock_builder.login_registry(u, p, r)
    image, image_id = mock_builder.build_from_git(
        'https://bitbucket.com/blurrcat/daedalus.git',
        'blurrcat', '123', version='latest'
    )
    assert image == '{}/{}/daedalus:latest'.format(r, u)
    assert image_id == mock_build


def test_run_command(mock_builder):
    lines = [line for line in mock_builder._run_command('date')]
    assert lines
    with pytest.raises(subprocess.CalledProcessError):
        _ = [line for line in mock_builder._run_command('date sdfsadfasdf')]
