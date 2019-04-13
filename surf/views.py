import datetime

from django.http import HttpRequest, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.utils import timezone

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
        # TODO: we can make this more efficient using a single call to the db

        context = {
            'latest': latest,
            'latest_tags': latest.tags.all(),
            'more_reports': rest,
            'more_reports_tags': dict(zip((report.id for report in rest), (report.tags.all() for report in rest))),
        }

        return render(request, 'surf/home.html', context)


class SurfReportDetailView:
    def view(self, request: HttpRequest, **url_params):
        surf_report = get_object_or_404(SurfReport, pk=url_params['pk'])

        context = {
            'surf_report': surf_report,
            'tags': surf_report.tags.all(),
            'all_tags': Tag.objects.all(),
        }
        return render(request, 'surf/surf_report.html', context)


class CreateTagView:
    def view(self, request: HttpRequest):
        if request.method == 'POST':
            form = TagForm(request.POST)

            if form.is_valid():
                Tag.objects.get_or_create(label=form.cleaned_data['label'])
                return HttpResponseRedirect(reverse('surf:home'))
        else:
            form = TagForm()

        return render(request, 'surf/new_tag.html', {'form': form})


class AddTagView:
    def view(self, request: HttpRequest, **url_params):
        surf_report = get_object_or_404(SurfReport, pk=url_params['pk'])
        tag = get_object_or_404(Tag, pk=request.POST['tag'])

        surf_report.tags.add(tag)
        surf_report.save()
        return HttpResponseRedirect(reverse('surf:home'))
