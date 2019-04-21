from django.db import models
import random


class Tag(models.Model):
    label = models.CharField(max_length=30, unique=True)


class SurfReport(models.Model):
    captured_at = models.DateTimeField()
    local_time = models.DateTimeField()
    min_swell = models.FloatField()
    max_swell = models.FloatField()
    tags = models.ManyToManyField(Tag)
    note = models.TextField(max_length=150)

    class Meta:
        indexes = [
            models.Index(fields=['-captured_at']),
        ]


class Note:
    words = ['folly', 'fun', 'times', 'cow', 'sheep', 'hello', 'weeee', 'holiday', 'lollipop', 'bird', 'run', 'seek',
             'climb', 'swim', 'crawl', 'sunshine', 'moon', 'the', 'a', 'fresh', 'food', 'fish', 'table', 'coffee',
             'pooky', 'egg', 'taco', 'maths', 'science', 'planet', 'star', 'bag', 'sat', 'on', 'medicine', 'tray',
             'sleep', 'blanket', 'cord', 'carpet', 'dear', 'love', 'regards', 'thanks', 'sorry', 'sure', 'see', 'you',
             'I', 'soon', 'run', 'running', 'dinosaur', 'did-you-think-he-saw-us-rex', 'saw', 'flute']

    @classmethod
    def generate(cls):
        return ' '.join([random.choice(cls.words) for i in range(10)])
