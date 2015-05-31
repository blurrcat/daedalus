#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import logging
import re
import subprocess
import urllib.parse as urlparse
from docker import Client
from docker.errors import APIError
from docker.utils import kwargs_from_env
from daedalus.utils import TempDirectory


class Docker(object):

    def __init__(self, registry=None, username=None, password=None,
                 nocache=False, assert_hostname=None, log_handler=None):
        self.re_repo = re.compile(r'.*/(\w+).git')
        self.re_image_id = re.compile(r'Successfully built (\w+)')
        self.logger = logging.getLogger('daedalus.docker')
        self.nocache = nocache
        if log_handler:
            self.log_handler = log_handler
        self.client = Client(**kwargs_from_env(
            assert_hostname=assert_hostname))
        self.registry = registry
        self.registry_username = username
        if username and password and registry:
            self.login_registry(username, password, registry)

    def login_registry(self, username, password, registry):
        self.logger.info('login %s@%s', username, registry)
        try:
            resp = self.client.login(username, password, registry=registry)
        except APIError:
            self.logger.error('login failed: %s@%s', username, registry)
            raise RuntimeError('login failed')
        self.registry_username = username
        self.registry = registry
        return resp

    def log_handler(self, content):
        self.logger.info(content)

    def _run_command(self, *commands):
        print(len(commands))
        for c in commands:
            yield '$ {}'.format(c)
            if isinstance(c, str):
                c = c.split()
            self.logger.debug('run command "%s"', c)
            yield subprocess.check_output(c).decode('utf-8').strip()

    @staticmethod
    def _set_auth(url, username, password):
        parsed = urlparse.urlparse(url)
        if not username:
            username = parsed.username
        if not password:
            password = parsed.password
        auth = ':'.join(item for item in (username, password) if item)
        netloc = '{}@{}'.format(auth, parsed.netloc.split('@')[-1])
        url = urlparse.ParseResult(
            parsed.scheme, netloc, parsed.path, parsed.params, parsed.query,
            parsed.fragment).geturl()
        return url, username, password

    def _parse_repo(self, url):
        match = self.re_repo.match(url)
        if match:
            return match.groups()[0]
        else:
            raise ValueError('invalid git url: {0}'.format(url))

    def _parse_image_id(self, data):
        match = self.re_image_id.match(data)
        if match:
            return match.groups()[0]
        else:
            return None

    def _get_repo(self, git_url, commit):
        self.logger.info('fetching %s..', git_url)
        try:
            for line in self._run_command(
                'git init',
                'git pull --depth 50 {0}'.format(git_url),
                'git checkout -f {0}'.format(commit),
            ):
                self.log_handler(line)
        except subprocess.CalledProcessError as e:
            self.log_handler(e.output)
            self.logger.error(
                'fail to run shell command "%s": %s', e.cmd, e.output)
            raise
        self.logger.info('fetched %s at %s', git_url, commit)

    def build_from_git(
            self, url, username=None, password=None, commit='master',
            version=None
    ):
        """
        build image from git. Currently only supports https

        :param url: git url
        :param username: git username
        :param password: git password
        :param version: image version. Default: git commit hash
        :return: tag name of the image built
        """
        # find repo name
        reponame = self._parse_repo(url)
        # set auth
        url, username, password = self._set_auth(url, username, password)

        # repo example: tutum.co/blurrcat/daedalus:0.1
        repo = '/'.join((self.registry, self.registry_username, reponame))
        if not version:
            # 7 digits of git hash
            version = list(
                self._run_command('git rev-parse HEAD'))[1][:7]
        image = '{}:{}'.format(repo, version)

        with TempDirectory(image):
            self._get_repo(url, commit)
            self.logger.info('building image %s...', image)

            self.log_handler(
                '$ docker build -t{nocache} {image} .'.format(
                    nocache=' --no-cache' if self.nocache else '',
                    image=image))
            last = None
            for line in self.client.build(
                    path='.', tag=image, nocache=self.nocache):
                data = json.loads(line.decode('utf-8'))
                last = data['stream']
                self.log_handler(last)
            image_id = self._parse_image_id(last)
            self.logger.info('build finished %s(image id %s)', image, image_id)

            self.logger.info(
                'pushing image %s(image id %s) ...', image, image_id)
            self.log_handler('$ docker push {}'.format(image))
            status = None
            for line in self.client.push(image, stream=True):
                data = json.loads(line.decode('utf-8'))
                if status != data['status']:
                    status = data['status']
                    self.log_handler(status)
            self.logger.info('pushed image %s@(image id %s)', image, image_id)
        return image, image_id
