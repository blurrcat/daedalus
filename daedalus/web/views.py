#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Blueprint, request


bp_build = Blueprint('docker', 'docker', url_prefix='/build')


@bp_build.route('/', methods=['POST'])
def build():
    """
    submit a build
    """
    pass


@bp_build.route('/<bid>/logs/')
def logs(bid):
    """
    get build logs of a container
    :return:
    """
    pass
