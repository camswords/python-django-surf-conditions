import datetime

from django.http import HttpRequest, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.utils import timezone
from django.views.generic.detail import DetailView

from surf.forms import TagForm
from surf.models import SurfReport, Tag
from surf.services import SurfReportGateway


class SurfReportHomeView:
    def __init__(self, gateway: SurfReportGateway):
        self.gateway = gateway

    # TODO: move this to the model class I think
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

        return render(request, 'surf/home.html', context)


class SurfReportDetailView(DetailView):
    model = SurfReport
    context_object_name = 'surf_report'
    template_name = 'surf/surf_report.html'


class CreateTagView:
    def view(self, request: HttpRequest):
        if request.method == 'POST':
            form = TagForm(request.POST)

            if form.is_valid():
                tag = Tag(form.cleaned_data['label'])
                tag.save()
                return HttpResponseRedirect(reverse('surf:home'))

            # TODO: deal with form errors
            # TODO: ensure that tags are unique, both in the database and enforced by our app using custom validation

        return render(request, 'surf/new_tag.html', {'form': TagForm()})
