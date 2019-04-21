from django.core.management.base import BaseCommand
from surf.models import SurfReport, Tag, Note
from django.utils import timezone
from datetime import timedelta
import random


class Command(BaseCommand):
    help = 'Seed the database with some example data.'

    def add_arguments(self, parser):
        parser.add_argument('-r', '--reports', type=int, help='define how many surf reports to create')

    def build_datetime(self, date, days):
        return date - timedelta(days=days)

    def build_reports(self, days_ago):
        date = self.build_datetime(timezone.now(), days_ago)
        min_swell = random.random() * 2
        max_swell = (random.random() * 2) + 3
        note = Note.generate()
        return SurfReport(captured_at=date, local_time=date, min_swell=max_swell, max_swell=min_swell, note=note)

    def handle(self, *args, **options):
        num_to_create = options['reports'] or 100
        tag_labels = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        saved_tags = list(map(lambda label: Tag.objects.get_or_create(label=label)[0], tag_labels))
        tags = dict(zip(map(lambda t: t.label.lower(), saved_tags), saved_tags))

        # this is more python-like, tho [] means that it is not lazily executed (use () for that)
        # surf_reports = [self.build_reports(days_ago) for days_ago in range(0, num_to_create)]
        surf_reports = map(lambda days_ago: self.build_reports(days_ago), range(0, num_to_create))

        for report in surf_reports:
            report.save()
            tag_label = report.captured_at.strftime('%A').lower()
            report.tags.add(tags[tag_label])

        print('created {0} surf reports.'.format(num_to_create))
