from django.db import models


class SurfReport(models.Model):
    captured_at = models.DateTimeField()
    local_time = models.DateTimeField()
    min_swell = models.IntegerField()
    max_swell = models.IntegerField()
