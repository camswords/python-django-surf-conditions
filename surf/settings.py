import os

from django.conf import settings


def get_setting(name, default_value, translation_fn=lambda x: x):
    return translation_fn(getattr(settings, name, os.getenv(name, default_value)))


API_SURF_REPORTS_PER_PAGE = get_setting('API_SURF_REPORTS_PER_PAGE', '3', int)
MEMCACHED_SERVER_URI = get_setting('MEMCACHED_SERVER_URI', 'localhost:11211')
MEMCACHED_SERVER_CONNECT_TIMEOUT_SECONDS = get_setting('MEMCACHED_SERVER_CONNECT_TIMEOUT_SECONDS', '5', int)
MEMCACHED_SERVER_READ_TIMEOUT_SECONDS = get_setting('MEMCACHED_SERVER_READ_TIMEOUT_SECONDS', '5', int)
MAGIC_SEAWEED_API_KEY = get_setting('SURF_MAGICSEAWEED_API_KEY', None)
MAGIC_SEAWEED_MANLY_NSW_SPOT_ID = get_setting('MAGIC_SEAWEED_MANLY_NSW_SPOT_ID', '524')
MAGIC_SEAWEED_URL = 'http://magicseaweed.com/api/%s/forecast/?spot_id=%s' % (MAGIC_SEAWEED_API_KEY, MAGIC_SEAWEED_MANLY_NSW_SPOT_ID)
SEARCH_RESULTS_PER_PAGE = get_setting('SEARCH_RESULTS_PER_PAGE', '14', int)
