#! /usr/bin/env python
# -*- coding: utf-8 -*-
import ast
import os
from flask import Flask
from redis import StrictRedis
from rq import Queue


def configure_app(app):
    app.config.from_object('daedalus.config')
    # production config via env vars
    prefix = 'DAEDALUS_'
    for k, v in os.environ.items():
        if k.startswith(prefix):
            k = k[len(prefix):]
            try:
                v = ast.literal_eval(v)
            except (ValueError, SyntaxError):
                pass
            app.config[k] = v
            m = 'override config %s via environment' % k
            if app.config.get('DEBUG', False):
                m = '%s: %s' % (m, v)
            print(m)


def configure_extensions(app):
    redis = StrictRedis.from_url(app.config['REDIS_DSN'])
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
