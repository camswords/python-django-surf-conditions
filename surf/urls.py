from . import settings
from django.urls import path

from surf.services import SurfReportGateway
from surf.views import SurfReportHomeView
from . import views

app_name = 'surf'

# TODO: should move this into models probably :-(
surf_report_gateway = SurfReportGateway(settings.MAGIC_SEAWEED_URL, settings.MAGIC_SEAWEED_API_KEY)

urlpatterns = [
    path('', SurfReportHomeView(surf_report_gateway).view, name='home'),
    path('<int:pk>/', views.SurfReportDetailView().view, name='surf_report'),
    path('<int:pk>/tag/add', views.AddTagView().view, name='add_tag'),
    path('tag/new', views.CreateTagView().view, name='new_tag'),
]
