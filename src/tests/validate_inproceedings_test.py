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
            citation = Citation(self.inproceedings_form)
        except UserInputError:
            self.fail("Citation raised exception unexpectedly.")

    def test_inproceedings_without_required_fields_raises_error(self):
        with self.assertRaises(UserInputError):
            self.inproceedings_form["author"] = ""
            self.inproceedings_form["title"] = ""
            self.inproceedings_form["booktitle"] = ""
            self.inproceedings_form["year"] = ""
            citation = Citation(self.inproceedings_form)

    def test_inproceedings_with_non_numeric_volume_raises_error(self):
        with self.assertRaises(UserInputError):
            self.inproceedings_form["volume"] = " a1b2  "
            citation = Citation(self.inproceedings_form)

    def test_inproceedings_with_whitespace_note_raises_error(self):
        with self.assertRaises(UserInputError):
            self.inproceedings_form["note"] = "   "
            citation = Citation(self.inproceedings_form)
