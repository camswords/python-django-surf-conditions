import json

from pymemcache.client.base import Client

from . import settings


class CacheError(Exception):
    pass


class JsonSerialisation:
    def serialise(self, key, value):
        if len(key) > 250:
            raise CacheError('cache key is longer than 250 chars, memcached wont store it. key is %s' % key)

        try:
            return json.dumps(value)
        except Exception as ex:
            raise CacheError('failed to serialise key %s for storing in cache' % key) from ex


    def deserialise(self, key, value):
        try:
            return json.loads(value)
        except Exception as ex:
            raise CacheError('failed to deserialise key %s for retrieval from cache' % key) from ex


class Cache:
    def __init__(self,
                 key_prefix=settings.APP_VERSION,
                 connect_timeout=settings.MEMCACHED_SERVER_CONNECT_TIMEOUT_SECONDS,
                 timeout=settings.MEMCACHED_SERVER_READ_TIMEOUT_SECONDS,
                 serialisation_strategy=JsonSerialisation()):
        self._cache = Client(settings.MEMCACHED_SERVER_URI,
                             key_prefix='%s:' % key_prefix,
                             serializer=serialisation_strategy.serialise,
                             deserializer=serialisation_strategy.deserialise,
                             connect_timeout=connect_timeout,
                             timeout=timeout)
