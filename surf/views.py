from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse

from surf.forms import TagForm, SearchForm
from surf.models import SurfReport, Tag
from surf.services import SurfReportGateway


class SurfReportHomeView:
    def view(self, request):
        reports = SurfReport.objects.all().prefetch_related('tags').order_by('-captured_at')[:11]

        context = {
            'latest': reports[0] if reports else None,
            'reports': reports[1:],
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


class ShowTagView:
    def view(self, request, **url_params):
        tag = get_object_or_404(Tag, pk=url_params['pk'])
        reports = SurfReport.objects.prefetch_related('tags').filter(tags=tag).order_by('-captured_at')

        context = {
            'tag': tag,
            'reports': reports,
        }
        return render(request, 'surf/show_tag.html', context)


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


class SearchView:
    def view(self, request):
        query = request.GET.get('query', None)

        context = {
            'form': SearchForm(request.GET) if query else SearchForm(),
            'num_of_results': SurfReport.objects.search_note(query).count(),
            'results': SurfReport.objects.fetch_tags().search_note(query)[:10],
        }
        return render(request, 'surf/search.html', context)
