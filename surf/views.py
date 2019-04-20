from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse

from surf.forms import TagForm
from surf.models import SurfReport, Tag
from surf.services import SurfReportGateway


class SurfReportHomeView:
    def __init__(self, gateway=SurfReportGateway()):
        self.gateway = gateway

    def view(self, request):
        latest, rest = self.gateway.get_or_retrieve_reports(limit=11, stale_after_seconds=2)
        # TODO: we can make this more efficient using a single call to the db

        context = {
            'latest': latest,
            'latest_tags': latest.tags.all(),
            'more_reports': rest,
            'more_reports_tags': dict(zip((report.id for report in rest), (report.tags.all() for report in rest))),
        }

        return render(request, 'surf/home.html', context)


class SurfReportDetailView:
    def view(self, request, **url_params):
        surf_report = get_object_or_404(SurfReport, pk=url_params['pk'])

        context = {
            'surf_report': surf_report,
            'tags': surf_report.tags.all(),
            'all_tags': Tag.objects.all(),
        }
        return render(request, 'surf/surf_report.html', context)


class CreateTagView:
    def view(self, request):
        if request.method == 'POST':
            form = TagForm(request.POST)

            if form.is_valid():
                Tag.objects.get_or_create(label=form.cleaned_data['label'])
                return HttpResponseRedirect(reverse('surf:home'))
        else:
            form = TagForm()

        return render(request, 'surf/new_tag.html', {'form': form})


class AddTagView:
    def view(self, request, **url_params):
        surf_report = get_object_or_404(SurfReport, pk=url_params['pk'])
        tag = get_object_or_404(Tag, pk=request.POST['tag'])

        surf_report.tags.add(tag)
        surf_report.save()
        return HttpResponseRedirect(reverse('surf:home'))


class FetchReportView:
    def __init__(self, gateway=SurfReportGateway()):
        self.gateway = gateway

    def view(self, request):
        if request.method == 'POST':
            report = self.gateway.latest_report()
            report.save()

        return HttpResponseRedirect(reverse('surf:home'))

