from django.db import models


class Tag(models.Model):
    label = models.CharField(max_length=30)


class SurfReport(models.Model):
    captured_at = models.DateTimeField()
    local_time = models.DateTimeField()
    min_swell = models.FloatField()
    max_swell = models.FloatField()
    tags = models.ManyToManyField(Tag)              # this is on SurfReport because that's how we want to access the tags.

    class Meta:
        indexes = [
            models.Index(fields=['-captured_at']),
        ]

    # TODO: check the indexes that are used when searching for tags from surf reports
