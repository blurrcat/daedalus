#! /usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Flask


def create_app():
    app = Flask('daedalus')

    @app.route('/')
    def index():
        return 'hello world'

    return app


if __name__ == '__main__':
    create_app().run(
        host='0.0.0.0', port=8000, debug=True)
