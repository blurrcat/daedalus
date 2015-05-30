#!/usr/bin/env python
# -*- coding: utf-8 -*-
from redis import StrictRedis


class RedisLog(object):

    def __init__(self, redis_url='redis://127.0.0.1', ttl=3600, prefix='log'):
        self.ttl = ttl
        self.prefix = prefix
        self.redis = StrictRedis.from_url(redis_url)

    def _key(self, jid):
        return '{}.{}'.format(self.prefix, jid)

    def touch(self, jid):
        k = self._key(jid)
        self.redis.lpush(k, '')
        self.redis.expire(k, self.ttl)

    def append(self, jid, content):
        """
        returns length of log after append
        """
        if content:
            if isinstance(content, str):
                content = content.encode('utf-8')
            return self.redis.rpush(self._key(jid), content)

    def tail(self, jid, since=1):
        return [item.decode('utf-8')
                for item in self.redis.lrange(self._key(jid), since, -1)]
