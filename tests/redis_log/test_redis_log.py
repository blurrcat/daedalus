#!/usr/bin/env python
# -*- coding: utf-8 -*-


def test_log(redis_log):
    jid = 1
    redis_log.touch(jid)
    msgs = [str(i) for i in range(3)]
    for msg in msgs:
        redis_log.append(jid, msg)
    lines = redis_log.tail(jid)
    assert lines == msgs


def test_ttl(redis_log):
    jid = 2
    redis_log.touch(jid)
    redis_log.append(jid, '1')
    ttl = redis_log.redis.ttl(redis_log._key(jid))
    assert ttl > 0
