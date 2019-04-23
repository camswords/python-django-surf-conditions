from datetime import datetime

import requests
from django.core.exceptions import ImproperlyConfigured
from django.utils import timezone

from surf.models import SurfReport, Note
from . import settings


class SurfReportGatewayException(Exception):
    def __init__(self, message, url, api_key):
        msg = 'Failed to retrieve {0} due to {1}'.format(url.replace(api_key, '*****'), message)
        super(SurfReportGatewayException, self).__init__(msg)


class SurfReportGatewayResponse:
    def parse(self, message):
        latest = max(message, key=lambda m: m['timestamp'])
        min_swell = latest['swell']['absMinBreakingHeight']
        max_swell = latest['swell']['absMaxBreakingHeight']
        local_time = timezone.make_aware(datetime.utcfromtimestamp(latest['localTimestamp']))
        note = Note.generate()

        return SurfReport(captured_at=timezone.now(), local_time=local_time,
                          min_swell=min_swell, max_swell=max_swell,
                          note=note)


class SurfReportGateway:
    def __init__(self, url=settings.MAGIC_SEAWEED_URL, api_key=settings.MAGIC_SEAWEED_API_KEY):
        self.url = url
        self.api_key = api_key

    def latest_report(self):
        if not self.api_key:
            raise ImproperlyConfigured('unable to contact the surf gateway as the api key is missing.')

        response = requests.get(self.url)

        if response.status_code != 200:
            raise SurfReportGatewayException('response returned at status code of {0}'.format(response.status_code), self.url, self.api_key)

        return SurfReportGatewayResponse().parse(response.json())
