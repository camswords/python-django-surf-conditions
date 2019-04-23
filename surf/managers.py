from django.db import models


class SurfReportQuerySet(models.QuerySet):

    def order_by_captured_at(self):
        return self.order_by('-captured_at')

    def fetch_tags(self):
        return self.prefetch_related('tags')

    def search_note(self, text):
        if not text:
            return self.none()

        return self.filter(note__icontains=text)
