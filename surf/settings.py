import os

from django.conf import settings


class Settings:
    @staticmethod
    def get(name, default_value, translation_fn=lambda x: x):
        return translation_fn(getattr(settings, name, os.getenv(name, default_value)))


API_SURF_REPORTS_PER_PAGE = Settings.get('API_SURF_REPORTS_PER_PAGE', '3', int)
APP_VERSION = Settings.get('APP_VERSION', '1.0.0')
MEMCACHED_SERVER_URI = Settings.get('MEMCACHED_SERVER_URI', 'localhost:11211')
MEMCACHED_SERVER_CONNECT_TIMEOUT_SECONDS = Settings.get('MEMCACHED_SERVER_CONNECT_TIMEOUT_SECONDS', '5', int)
MEMCACHED_SERVER_READ_TIMEOUT_SECONDS = Settings.get('MEMCACHED_SERVER_READ_TIMEOUT_SECONDS', '5', int)
MAGIC_SEAWEED_API_KEY = Settings.get('SURF_MAGICSEAWEED_API_KEY', None)
MAGIC_SEAWEED_MANLY_NSW_SPOT_ID = Settings.get('MAGIC_SEAWEED_MANLY_NSW_SPOT_ID', '524')
MAGIC_SEAWEED_URL = 'http://magicseaweed.com/api/%s/forecast/?spot_id=%s' % (MAGIC_SEAWEED_API_KEY, MAGIC_SEAWEED_MANLY_NSW_SPOT_ID)
SEARCH_RESULTS_PER_PAGE = Settings.get('SEARCH_RESULTS_PER_PAGE', '14', int)
