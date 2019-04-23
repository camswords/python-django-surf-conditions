from django.test import TestCase

from surf.managers import SearchTerms


class SearchTermsTest(TestCase):

    def test_should_return_single_word(self):
        self.assertListEqual(list(SearchTerms.parse('word')), ['word'])

    def test_should_be_empty_when_none(self):
        self.assertListEqual(list(SearchTerms.parse('')), [])
        self.assertListEqual(list(SearchTerms.parse('   ')), [])
        self.assertListEqual(list(SearchTerms.parse(None)), [])

    def test_should_separate_words(self):
        self.assertListEqual(list(SearchTerms.parse('some words separate')), ['some', 'words', 'separate'])

    def test_should_remove_stop_words(self):
        self.assertListEqual(list(SearchTerms.parse('cam and jojo')), ['cam', 'jojo'])

    def test_should_search_for_complete_match(self):
        self.assertListEqual(list(SearchTerms.parse('testing "this value"')), ['testing', 'this value'])
