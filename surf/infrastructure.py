from django.core.cache import cache


class Cache:
    def get_or_set(self, key, get_value_func):
        value = cache.get(key)

        if value:
            return value, True

        value = get_value_func()
        cache.set(key, value)
        return value, False
