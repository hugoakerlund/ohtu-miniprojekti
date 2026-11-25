import unittest
from entities.citation import Citation
from util import UserInputError

class TestInproceedingsValidation(unittest.TestCase):
    def setUp(self):
        self.inproceedings_form = {
                "entry_type": "inproceedings",
                "author": "author",
                "title": "title",
                "booktitle": "booktitle",
                "year": "1900",
                "editor": None,
                "volume": None,
                "number": None,
                "series": None,
                "pages": None,
                "month": None,
                "address": None,
                "organization": None,
                "publisher": None,
                "note": None,
                "annote": None
            }

    def test_inproceedings_passes(self):
        try:
            Citation(self.inproceedings_form)
        except UserInputError:
            self.fail("Citation raised exception unexpectedly.")

    def test_inproceedings_without_required_fields_raises_error(self):
        for field in ("author", "title", "booktitle", "year"):
            with self.subTest(field=field), self.assertRaises(UserInputError):
                form = self.inproceedings_form.copy()
                form[field] = "   "
                Citation(form)

    def test_inproceedings_with_non_numeric_volume_raises_error(self):
        with self.assertRaises(UserInputError):
            self.inproceedings_form["volume"] = " a1b2  "
            Citation(self.inproceedings_form)

    def test_inproceedings_with_whitespace_note_raises_error(self):
        with self.assertRaises(UserInputError):
            self.inproceedings_form["note"] = "   "
            Citation(self.inproceedings_form)
