from django.urls import path

from surf.views import SurfReportHomeView
from . import views

app_name = 'surf'

urlpatterns = [
    path('', SurfReportHomeView().view, name='home'),
    path('<int:pk>/', views.SurfReportDetailView().view, name='surf_report'),
    path('<int:pk>/tag/add', views.AddTagView().view, name='add_tag'),
    path('tag/<int:pk>', views.ShowTagView().view, name='show_tag'),
    path('tag/new', views.CreateTagView().view, name='new_tag'),
    path('report/fetch', views.FetchReportView().view, name='fetch_report'),
    path('search', views.SearchView().view, name='search'),
    path('api/surf_reports', views.ApiSurfResults().view, name='api_surf_reports'),
]
