from django.urls import path
from . import views
from . import dependency_injection as di

app_name = 'surf'

urlpatterns = [
    path('', di.surf_report, name='surf_report'),
]
