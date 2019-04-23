from django.db import models


class SurfReportQuerySet(models.QuerySet):

    def fetch_tags(self):
        return self.prefetch_related('tags')

    def search_note(self, text):
        if not text:
            return self.none()

        return self.filter(note__icontains=text)
