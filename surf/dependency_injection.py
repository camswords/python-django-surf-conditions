from django.conf import settings
from surf.services import SurfReportGateway
from .views import SurfReportIndexView

# poor man's dependency injection

# gateways/services
surf_report_gateway = SurfReportGateway(settings.MAGIC_SEAWEED_URL, settings.MAGIC_SEAWEED_API_KEY)

# views
surf_report = SurfReportIndexView(surf_report_gateway).view
