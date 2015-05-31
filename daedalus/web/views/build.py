#!/usr/bin/env python
# -*- coding: utf-8 -*-
import uuid
from flask import current_app
from flask.ext.restful import Resource, reqparse, inputs
from daedalus.worker.jobs import build_from_git


class Build(Resource):

    def __init__(self):
        parser = reqparse.RequestParser()
        parser.add_argument(
            'url', required=True,
            type=inputs.regex(
                r'https://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|'
                r'(?:%[0-9a-fA-F][0-9a-fA-F]))+'))
        parser.add_argument('username')
        parser.add_argument('password')
        parser.add_argument('version')
        parser.add_argument('commit', default='master')
        self.parser = parser

    def post(self):
        kwargs = self.parser.parse_args()
        kwargs['id'] = uuid.uuid4().hex
        rq = current_app.extensions['rq']
        redis_log = current_app.extensions['redis_log']
        redis_log.touch(kwargs['id'])
        rq.enqueue(build_from_git, **kwargs)
        return kwargs


class Log(Resource):

    def __init__(self):
        parser = reqparse.RequestParser()
        parser.add_argument('since', type=inputs.natural, default=1)
        self.parser = parser

    def get(self, build_id):
        kwargs = self.parser.parse_args()
        redis_log = current_app.extensions['redis_log']
        return {
            'id': build_id,
            'since': kwargs['since'],
            'log': redis_log.tail(build_id, kwargs['since'])
        }

