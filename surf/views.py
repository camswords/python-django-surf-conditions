from django.http import HttpResponse, HttpRequest

from surf.services import SurfReportGateway


class SurfReport:
    def __init__(self, gateway: SurfReportGateway):
        self.gateway = gateway

    def view(self, request: HttpRequest):
        return HttpResponse(self.gateway.latest_report())
