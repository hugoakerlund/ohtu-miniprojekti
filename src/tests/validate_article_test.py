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
            Citation(self.article_form)
        except UserInputError:
            self.fail("Citation raised exception unexpectedly.")

    def test_article_without_required_fields_raises_error(self):
        with self.assertRaises(UserInputError):
            self.article_form["author"] = ""
            self.article_form["title"] = ""
            self.article_form["year"] = ""
            self.article_form["journal"] = ""
            Citation(self.article_form)

    def test_article_incorrect_entry_type_causes_error(self):
        with self.assertRaises(UserInputError):
            self.article_form["entry_type"] = "INCORRECT"
            Citation(self.article_form)

    def test_article_with_too_long_fields_causes_error(self):
        with self.assertRaises(UserInputError):
            long_title = "a" * 5000
            self.article_form["title"] = long_title
            Citation(self.article_form)

    def test_article_with_a_large_number_of_authors_succeeds(self):
        self.article_form["author"] = """Charles R. Harris, K. Jarrod Millman, Stéfan J. van der Walt, Ralf
                                         Gommers, Pauli Virtanen, David Cournapeau, Eric Wieser, Julian Taylor,
                                         Sebastian Berg, Nathaniel J. Smith, Robert Kern, Matti Picus, Stephan
                                         Hoyer, Marten H. van Kerkwijk, Matthew Brett, Allan Haldane, Jaime
                                         Fernández del Río, Mark Wiebe, Pearu Peterson, Pierre Gérard-Marchant,
                                         Kevin Sheppard, Tyler Reddy, Warren Weckesser, Hameer Abbasi, Christoph
                                         Gohlke & Travis E. Oliphant"""
        self.test_article_passes()

    def test_article_with_incorrect_year_causes_error(self):
        with self.assertRaises(UserInputError):
            self.article_form["year"] = "abc"
            Citation(self.article_form)

        self.article_form["year"] = "2000"
        self.test_article_passes()

    def test_article_with_incorrect_month_causes_error(self):
        with self.assertRaises(UserInputError):
            self.article_form["month"] = "abc"
            Citation(self.article_form)

        self.article_form["month"] = "2"
        self.test_article_passes()

    def test_article_with_incorrect_pages_causes_error(self):
        with self.assertRaises(UserInputError):
            self.article_form["pages"] = "abc"
            Citation(self.article_form)

            self.article_form["pages"] = "1,  10--9"
            Citation(self.article_form)

    def test_article_with_different_correct_page_entries_succeeds(self):
        self.article_form["pages"] = "1,2,3,4,5,6"
        self.test_article_passes()

        self.article_form["pages"] = "1--2,3--4,5--6"
        self.test_article_passes()

        self.article_form["pages"] = "2, 10--100"
        self.test_article_passes()

        self.article_form["pages"] = "2,     10--100,    101"
        self.test_article_passes()

        self.article_form["pages"] = "1--2, 10, 3--4,5--6"
        self.test_article_passes()
