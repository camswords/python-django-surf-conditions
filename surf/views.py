from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.core.paginator import Paginator

from surf import settings
from surf.forms import TagForm, SearchForm
from surf.models import SurfReport, Tag
from surf.services import SurfReportGateway


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

    def __init__(self, results_per_page=settings.API_SURF_REPORTS_PER_PAGE):
        self.results_per_page = results_per_page

    def _build_surf_report(self, surf_report):
        return {
            'id': surf_report.id,
            'captured_at': surf_report.captured_at.isoformat(),
            'min_swell': round(surf_report.min_swell, 2),
            'max_swell': round(surf_report.max_swell, 2),
            'tags': [tag.label for tag in surf_report.tags.all()],
        }

    def _build_url_to_page(self, request, page):
        uri = request.build_absolute_uri(reverse('surf:api_surf_reports'))
        return '%s?page=%d' % (uri, page)

    def view(self, request):
        all_reports = SurfReport.objects.fetch_tags().order_by_captured_at().all()
        reports = Paginator(all_reports, self.results_per_page).get_page(request.GET.get('page'))

        body_content = {
            'surf_reports': [self._build_surf_report(report) for report in reports],
            'metadata': {
                'page': reports.number,
                'number_of_pages': reports.paginator.num_pages,
            },
            'links': {
                'home': request.build_absolute_uri(reverse('surf:home')),
            },
        }

        if reports.has_previous():
            body_content['links']['first_page'] = self._build_url_to_page(request, 1)
            body_content['links']['previous_page'] = self._build_url_to_page(request, reports.previous_page_number())

        if reports.has_next():
            body_content['links']['next_page'] = self._build_url_to_page(request, reports.next_page_number())
            body_content['links']['last_page'] = self._build_url_to_page(request, reports.paginator.num_pages)

        return JsonResponse(body_content)
