import unittest
from entities.citation import Citation
from util import validate_citation, UserInputError

class TestCitationValidation(unittest.TestCase):
    def setUp(self):
        self.citation = {
                "title": "title",
                "type": "article",
                "author": "author",
                "howpublished": None,
                "year": None,
                "month": None,
                "address": None,
                "publisher": None,
                "edition": None,
                "pages": None
            }

    def test_citation_passes(self):
        try:
            validate_citation(self.citation)
        except UserInputError:
            self.fail("validate_citation() raised exception unexpectedly.")

    def test_citation_without_required_fields_raises_error(self):
        with self.assertRaises(UserInputError):
            self.citation["type"] = ""
            validate_citation(self.citation)

        self.citation["type"] = "article"
        self.test_citation_passes()

    def test_citation_incorrect_entry_type_causes_error(self):
        with self.assertRaises(UserInputError):
            self.citation["type"] = "INCORRECT"
            validate_citation(self.citation)

    def test_citation_with_too_long_fields_causes_error(self):
        with self.assertRaises(UserInputError):
            long_title = "a" * 101
            self.citation["title"] = long_title
            validate_citation(self.citation)

    def test_citation_with_incorrect_year_causes_error(self):
        with self.assertRaises(UserInputError):
            self.citation["year"] = "abc"
            validate_citation(self.citation)

        self.citation["year"] = "2000"
        self.test_citation_passes()

    def test_citation_with_incorrect_month_causes_error(self):
        with self.assertRaises(UserInputError):
            self.citation["month"] = "abc"
            validate_citation(self.citation)

        self.citation["month"] = "2"
        self.test_citation_passes()

    def test_citation_with_incorrect_pages_causes_error(self):
        with self.assertRaises(UserInputError):
            self.citation["pages"] = "abc"
            validate_citation(self.citation)

        self.citation["pages"] = "10-100"
        self.test_citation_passes()
