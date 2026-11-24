import unittest
from entities.citation import Citation
from util import UserInputError

class TestArticleValidation(unittest.TestCase):
    def setUp(self):
        self.article_form = {
                "entry_type": "article",
                "author": "author",
                "title": "title",
                "journal": "journal",
                "year": "1900",
                "volume": None,
                "number": None,
                "pages": None,
                "month": None,
                "note": None,
                "annote": None
            }

    def test_article_passes(self):
        try:
            citation = Citation(self.article_form)
        except UserInputError:
            self.fail("Citation raised exception unexpectedly.")

    def test_article_without_required_fields_raises_error(self):
        self.test_article_passes()

        with self.assertRaises(UserInputError):
            self.article_form["author"] = ""
            self.article_form["title"] = ""
            self.article_form["year"] = ""
            self.article_form["journal"] = ""
            citation = Citation(self.article_form)

            self.article_form["author"] = "author"
            citation = Citation(self.article_form)

            self.article_form["title"] = "title"
            citation = Citation(self.article_form)

            self.article_form["journal"] = "journal"
            citation = Citation(self.article_form)

            self.article_form["year"] = "1900"
            citation = Citation(self.article_form)


    def test_article_incorrect_entry_type_causes_error(self):
        with self.assertRaises(UserInputError):
            self.article_form["entry_type"] = "INCORRECT"
            citation = Citation(self.article_form)

    def test_article_with_too_long_fields_causes_error(self):
        with self.assertRaises(UserInputError):
            long_title = "a" * 101
            self.article_form["title"] = long_title
            citation = Citation(self.article_form)

    def test_article_with_incorrect_year_causes_error(self):
        with self.assertRaises(UserInputError):
            self.article_form["year"] = "abc"
            citation = Citation(self.article_form)

        self.article_form["year"] = "2000"
        self.test_article_passes()

    def test_article_with_incorrect_month_causes_error(self):
        with self.assertRaises(UserInputError):
            self.article_form["month"] = "abc"
            citation = Citation(self.article_form)

        self.article_form["month"] = "2"
        self.test_article_passes()

    def test_article_with_incorrect_pages_causes_error(self):
        with self.assertRaises(UserInputError):
            self.article_form["pages"] = "abc"
            citation = Citation(self.article_form)

        self.article_form["pages"] = "10-100"
        self.test_article_passes()
