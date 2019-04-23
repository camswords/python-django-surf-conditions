from operator import or_
from functools import reduce

from django.db import models
from django.db.models import Q
from django.utils.text import smart_split, unescape_string_literal


class SearchTerms:
    stop_words = ["a", "an", "and", "are", "as", "at", "be", "but", "by",
                  "for", "if", "in", "into", "is", "it",
                  "no", "not", "of", "on", "or", "such",
                  "that", "the", "their", "then", "there", "these",
                  "they", "this", "to", "was", "will", "with"]

    @classmethod
    def parse(cls, terms):
        if not terms:
            return []

        unescaped = map(lambda x: unescape_string_literal(x) if x and x[0] in '"\'' else x, smart_split(terms))
        safe_terms = filter(lambda x: x and x not in cls.stop_words, unescaped)

        return safe_terms


class SurfReportQuerySet(models.QuerySet):

    def order_by_captured_at(self):
        return self.order_by('-captured_at')

    def fetch_tags(self):
        return self.prefetch_related('tags')

    def search(self, terms):
        queries = [Q(note__icontains=search_term) for search_term in SearchTerms.parse(terms)]

        if not queries:
            return self.none()

        return self.filter(reduce(or_, queries)).order_by_captured_at()
