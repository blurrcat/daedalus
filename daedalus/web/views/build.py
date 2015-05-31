#!/usr/bin/env python
# -*- coding: utf-8 -*-
import uuid
from flask import current_app
from flask.ext.restful import Resource, reqparse, inputs
from daedalus.worker.jobs import build_from_git


class HttpsURL(inputs.regex):

    def __init__(self):
        super().__init__(
            r'https://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|'
            r'(?:%[0-9a-fA-F][0-9a-fA-F]))+')

    def __call__(self, value):
        try:
            return super().__call__(value)
        except ValueError as e:
            e.message = 'Invalid url. Only https is accepted'
            raise



class Build(Resource):

    def __init__(self):
        parser = reqparse.RequestParser()
        parser.add_argument('url', required=True, type=HttpsURL())
        parser.add_argument('username')
        parser.add_argument('password')
        parser.add_argument('version')
        parser.add_argument('commit', default='master')
        self.parser = parser

    def post(self):
        kwargs = self.parser.parse_args()
        kwargs['id'] = uuid.uuid4().hex
        build_queue = current_app.extensions['rq_build']
        redis_log = current_app.extensions['redis_log']
        redis_log.touch(kwargs['id'])
        build_queue.enqueue(build_from_git, **kwargs)
        return kwargs


class Logs(Resource):

    def __init__(self):
        parser = reqparse.RequestParser()
        parser.add_argument('since', type=inputs.natural, default=1)
        self.parser = parser

    def get(self, build_id):
        kwargs = self.parser.parse_args()
        redis_log = current_app.extensions['redis_log']
        since = kwargs['since']
        logs = redis_log.tail(build_id, since)
        return {
            'id': build_id,
            'since': since,
            'next': since + len(logs),
            'logs': logs,
        }

