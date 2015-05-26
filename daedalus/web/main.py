#! /usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Flask
from redis import StrictRedis
from rq import Queue
from daedalus.utils import get_config


def configure_app(app):
    app.config = get_config()


def configure_extensions(app):
    redis = StrictRedis.from_url(app.config['REDIS_URL'])
    app.extensions['redis'] = redis
    queue = Queue(connection=redis)
    app.extensions['queue'] = queue


def configure_views(app):
    @app.route('/')
    def index():
        return 'hello world'


def create_app():
    app = Flask('daedalus')
    configure_app(app)
    configure_extensions(app)
    configure_views(app)

    return app


if __name__ == '__main__':
    create_app().run(
        host='0.0.0.0', port=8000, debug=True)
