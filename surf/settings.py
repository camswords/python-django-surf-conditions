import os

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

MAGIC_SEAWEED_API_KEY = getattr(settings, 'SURF_MAGICSEAWEED_API_KEY', os.getenv('MAGIC_SEAWEED_API_KEY', None))
MAGIC_SEAWEED_MANLY_NSW_SPOT_ID = '524'
MAGIC_SEAWEED_URL = 'http://magicseaweed.com/api/{0}/forecast/?spot_id={1}'.format(MAGIC_SEAWEED_API_KEY, MAGIC_SEAWEED_MANLY_NSW_SPOT_ID)
