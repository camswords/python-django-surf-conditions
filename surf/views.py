from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.core.paginator import Paginator

from surf import settings
from surf.forms import TagForm, SearchForm
from surf.models import SurfReport, Tag
from surf.services import SurfReportGateway


class SurfReportHomeView:
    def view(self, request):
        latest = SurfReport.objects.fetch_tags().order_by_captured_at().first()
        reports = SurfReport.objects.all().fetch_tags().order_by_captured_at()
        pages = Paginator(reports, 15)

        context = {
            'latest': latest,
            'reports': pages.get_page(request.GET.get('page')),
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

    def __init__(self, results_per_page=settings.SEARCH_RESULTS_PER_PAGE):
        self.results_per_page = results_per_page

    def view(self, request):
        query = request.GET.get('query')
        results = SurfReport.objects.fetch_tags().search(query)
        pages = Paginator(results, self.results_per_page)

        context = {
            'form': SearchForm(request.GET) if query else SearchForm(),
            'num_of_results': SurfReport.objects.search(query).count(),
            'results': pages.get_page(request.GET.get('page')),
            'query_params': {'query': query} if query else None,
            'search_term': query,
        }

        return render(request, 'surf/search.html', context)
