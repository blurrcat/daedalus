#! /usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Flask
from flask.ext.restful import Api
from redis import StrictRedis
from rq import Queue
from rq_dashboard import RQDashboard
from daedalus import config
from daedalus.redis_log import RedisLog
from daedalus.utils import config_from_env
from daedalus.web.views import build


def configure_app(app):
    app.config.from_object(config)
    app.config.update(config_from_env())


def configure_extensions(app):
    redis = StrictRedis.from_url(app.config['REDIS_URL'])
    # redis log
    redis_log = RedisLog(
        connection=redis,
        ttl=app.config['REDIS_LOG_TTL'],
        prefix=app.config['REDIS_LOG_PREFIX'],
    )
    app.extensions.update({
        'redis': redis,
        'redis_log': redis_log,
    })
    # rq
    for q in app.config['QUEUES']:
        queue = Queue(
            name=q, default_timeout=app.config[
                'RQ_JOB_TIMEOUT_{}'.format(q.upper())],
            connection=redis,
        )
        app.extensions['rq_{}'.format(q)] = queue

    # rq dashboard
    RQDashboard(app, url_prefix='/_rq')

    # api endpoints
    api = Api(prefix='/api')
    api.add_resource(build.Build, '/build/')
    api.add_resource(build.Logs, '/build/<build_id>/logs/')
    api.init_app(app)


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
