from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.core.paginator import Paginator
from django.core.cache import cache

from surf import settings
from surf.forms import TagForm, SearchForm
from surf.models import SurfReport, Tag
from surf.services import SurfReportGateway, FetchService


class SurfReportHomeView:
    def view(self, request):
        all_reports = SurfReport.objects.all().fetch_tags().order_by_captured_at()
        reports = Paginator(all_reports, 15).get_page(request.GET.get('page'))

        context = {
            'latest': reports[0] if reports else None,
            'reports': reports,
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


class ApiSurfResults:

    def __init__(self, fetch_service=FetchService()):
        self.fetch_service = fetch_service

    def url_to_page(self, request, page):
        uri = request.build_absolute_uri(reverse('surf:api_surf_reports'))
        return '%s?page=%d' % (uri, page)

    def conditional_link(self, name, uri):
        return {name: uri} if uri else {}

    def view(self, request):
        reports, served_from_cache = self.fetch_service.load_page(request.GET.get('page', '1'))

        body_content = {
            'surf_reports': [{
                'id': report.id,
                'captured_at': report.captured_at.isoformat(),
                'min_swell': round(report.min_swell, 2),
                'max_swell': round(report.max_swell, 2),
                'tags': [tag.label for tag in report.tags.all()],
                'note': report.note,
            } for report in reports.results],
            'metadata': {
                'page': reports.page,
                'number_of_pages': reports.num_pages,
                'served_from_cache': served_from_cache,
            },
            'links': {
                'home': request.build_absolute_uri(reverse('surf:home')),
                **(self.conditional_link('previous_page', reports.has_previous() and self.url_to_page(request, reports.previous_page()))),
                **(self.conditional_link('next_page', reports.has_next() and self.url_to_page(request, reports.next_page()))),
                **(self.conditional_link('first_page', reports.has_previous() and self.url_to_page(request, 1))),
                **(self.conditional_link('last_page', reports.has_next() and self.url_to_page(request, reports.num_pages))),
            },
        }

        return JsonResponse(body_content)
