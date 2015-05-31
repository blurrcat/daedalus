#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json


def test_create_build(app):
    with app.test_client() as c:
        # create build
        r = c.post('/api/build/', data={
            'url': 'https://blurrcat@test.com/repo.git'
        })
        r = json.loads(r.data.decode('utf-8'))
        assert r['id']


def test_create_build_errors(app):
    with app.test_client() as c:
        for data in (
            {},  # missing url
            {'url': 'http://github.com/blurrcat/repo.git'},  # only https
        ):
            r = c.post('/api/build/', data=data)
            assert r.status_code == 400
            r = json.loads(r.data.decode('utf-8'))
            assert r['message']['url']


def test_logs(app):
    with app.test_client() as c:
        r = c.post('/api/build/', data={
            'url': 'https://github.com/blurrcat/repo.git',
            'username': 'blurrcat',
        })
        r = json.loads(r.data.decode('utf-8'))
        since = 10
        r = c.get('/api/build/{}/logs/'.format(r['id']), query_string={
            'since': since,
        })
        assert r.status_code == 200
        r = json.loads(r.data.decode('utf-8'))
        assert 'logs' in r
        assert r['since'] == since
        assert r['since'] + len(r['logs']) == r['next']
