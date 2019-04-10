from django.http import HttpRequest
from django.shortcuts import render
from django.utils import timezone
from surf.models import SurfReport
from surf.services import SurfReportGateway
import datetime


class SurfReportView:
    def __init__(self, gateway: SurfReportGateway):
        self.gateway = gateway

    def view(self, request: HttpRequest):
        ten_secs_ago = timezone.now() - datetime.timedelta(seconds=10)

        # what if more than one result is returned?
        recent_report = SurfReport.objects.filter(captured_at__gte=ten_secs_ago)

        if not recent_report:
            recent_report = self.gateway.latest_report()
            recent_report.save()
        else:
            # there may be many results here - possibly not the best solution.
            # I wonder if we can limit the result set, or make sure an index is applied which will return the latest result set
            recent_report = recent_report.latest('captured_at')

        return render(request, 'surf/latest-report.html', {'surf_report': recent_report})
