from django.http import HttpRequest
from django.shortcuts import render

from surf.models import SurfReport
from surf.services import SurfReportGateway


class SurfReportView:
    def __init__(self, gateway: SurfReportGateway):
        self.gateway = gateway

    def view(self, request: HttpRequest):
        # TODO: see if we can see the SQL, and add an index to make sure this query is efficient
        # TODO: it looks like if we slice here that it will be factored into the query - cool!

        count = SurfReport.objects.count()

        if count == 0:
            context = {
                'captured_at': None,
                'local_time': None,
                'min_swell': None,
                'max_swell': None,
                'results': count,
            }
            return render(request, 'surf/report.html', context)

        latest_report = SurfReport.objects.latest('local_time')
        
        context = {
            'captured_at': latest_report.captured_at,
            'local_time': latest_report.local_time,
            'min_swell': latest_report.min_swell,
            'max_swell': latest_report.max_swell,
            'results': count,
        }
        
        return render(request, 'surf/report.html', context)
