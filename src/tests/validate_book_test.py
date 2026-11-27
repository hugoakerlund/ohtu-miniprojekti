import unittest
from datetime import datetime
from entities.citation import Citation
from util import UserInputError

class TestBookValidation(unittest.TestCase):
    def setUp(self):
        self.book_form = {
                "entry_type": "book",
                "author": "author",
                "editor": "editor",
                "title": "title",
                "publisher": "publisher",
                "year": "1900",
                "volume": None,
                "number": None,
                "pages": None,
                "month": None,
                "note": None,
            }

    def test_book_passes(self):
        try:
            Citation(self.book_form)
        except UserInputError:
            self.fail("Citation raised exception unexpectedly.")

    def test_book_without_required_fields_raises_error(self):
        with self.assertRaises(UserInputError):
            self.book_form["author"] = ""
            self.book_form["editor"] = ""
            self.book_form["title"] = ""
            self.book_form["publisher"] = ""
            self.book_form["year"] = ""
            Citation(self.book_form)

    def test_book_with_whitespace_only_required_fields_raises_error(self):
        for field in ("author", "editor", "title", "publisher"):
            with self.subTest(field=field), self.assertRaises(UserInputError):
                form = self.book_form.copy()
                form[field] = "   "
                Citation(form)

    def test_book_with_invalid_year_raises_error(self):
        for year in ("abc", "-1", str(datetime.now().year + 1)):
            with self.subTest(year=year), self.assertRaises(UserInputError):
                form = self.book_form.copy()
                form["year"] = year
                Citation(form)

    def test_book_with_non_numeric_volume_or_number_raises_error(self):
        for field in ("volume", "number"):
            with self.subTest(field=field), self.assertRaises(UserInputError):
                form = self.book_form.copy()
                form[field] = "1a"
                Citation(form)

    def test_book_with_invalid_pages_raises_error(self):
        for pages in ("abc", "1b", "20-10", "1-a"):
            with self.subTest(pages=pages), self.assertRaises(UserInputError):
                form = self.book_form.copy()
                form["pages"] = pages
                Citation(form)

    def test_book_with_invalid_month_raises_error(self):
        for month in ("abc", "0", "13"):
            with self.subTest(month=month), self.assertRaises(UserInputError):
                form = self.book_form.copy()
                form["month"] = month
                Citation(form)

    def test_book_with_whitespace_only_optional_note_raises_error(self):
        with self.assertRaises(UserInputError):
            form = self.book_form.copy()
            form["note"] = "   "
            Citation(form)

    def test_book_with_too_long_field_raises_error(self):
        with self.assertRaises(UserInputError):
            form = self.book_form.copy()
            form["title"] = "a" * 101
            Citation(form)
