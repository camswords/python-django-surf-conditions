from django.http import HttpRequest
from django.shortcuts import render
from django.utils import timezone
from surf.models import SurfReport
from surf.services import SurfReportGateway
import datetime


class SurfReportIndexView:
    def __init__(self, gateway: SurfReportGateway):
        self.gateway = gateway

    def __get_latest_reports(self, limit):
        latest_reports = list(SurfReport.objects.order_by('-captured_at')[:limit])

        if not latest_reports:
            new_report = self.gateway.latest_report()
            new_report.save()
            latest_reports = [new_report]

        elif latest_reports[:1][0].captured_at < timezone.now() - datetime.timedelta(seconds=10):
            new_report = self.gateway.latest_report()
            new_report.save()
            latest_reports = [new_report] + latest_reports

        return latest_reports[:1][0], latest_reports[1:limit]

    def view(self, request: HttpRequest):
        latest, rest = self.__get_latest_reports(11)

        context = {
            'latest': latest,
            'more_reports': rest,
        }

        return render(request, 'surf/index.html', context)
