from django.conf import settings
from surf.services import SurfReportGateway
from .views import SurfReportHomeView

# poor man's dependency injection
# TODO: we probably should remove this, and learn to do it the Django way

# gateways/services
surf_report_gateway = SurfReportGateway(settings.MAGIC_SEAWEED_URL, settings.MAGIC_SEAWEED_API_KEY)

# views
surf_report = SurfReportHomeView(surf_report_gateway).view
