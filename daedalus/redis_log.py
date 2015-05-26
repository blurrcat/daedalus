#!/usr/bin/env python
# -*- coding: utf-8 -*-
from redis import StrictRedis


class RedisLog(object):
    PREFIX = 'log'

    def __init__(self, redis_url, ttl=3600):
        self.ttl = ttl
        self.c = StrictRedis.from_url(redis_url)

    def _key(self, jid):
        return '{}.{}'.format(self.PREFIX, jid)

    def touch(self, jid):
        k = self._key(jid)
        self.c.lpush(jid, k, '')
        self.c.expire(k, self.ttl)

    def append(self, jid, content):
        """
        returns length of log after append
        """
        if content:
            return self.c.rpush(self._key(jid), content)

    def tail(self, jid, since=1):
        return self.c.lrange(self._key(jid), since, -1)
