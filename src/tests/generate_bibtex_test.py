import unittest
from entities.citation import Citation
from util import UserInputError

class TestBibtexGeneration(unittest.TestCase):
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

    def test_generating_bibtex_with_required_fields_succeeds(self):
        expected = ('@article{authortitle00,\n'
                     '  author  = {author},\n'
                     '  title   = {title},\n'
                     '  journal = {journal},\n'
                     '  year    = {1900}\n'
                     '}')
        result = Citation(self.article_form).generate_bibtex()

        self.assertEqual(expected, result)

    def test_generating_bibtex_with_all_fields_succeeds(self):
        self.article_form["volume"] = "1"
        self.article_form["number"] = "1"
        self.article_form["pages"] = "1--10"
        self.article_form["month"] = "1"
        self.article_form["note"] = "note"
        self.article_form["annote"] = "annote"

        expected = ('@article{authortitle00,\n'
                     '  author  = {author},\n'
                     '  title   = {title},\n'
                     '  journal = {journal},\n'
                     '  year    = {1900},\n'
                     '  volume  = {1},\n'
                     '  number  = {1},\n'
                     '  pages   = {1--10},\n'
                     '  month   = {1},\n'
                     '  note    = {note},\n'
                     '  annote  = {annote}\n'
                     '}')
        result = Citation(self.article_form).generate_bibtex()
        self.assertEqual(expected, result)

    def test_optional_fields_are_omitted_when_none(self):
            result = Citation(self.article_form).generate_bibtex()

            self.assertNotIn("volume", result)
            self.assertNotIn("number", result)
            self.assertNotIn("pages", result)
            self.assertNotIn("month", result)
            self.assertNotIn("note", result)
            self.assertNotIn("annote", result)


    def test_cite_key_uses_last_author_and_title_words(self):
        self.article_form["author"] = "Donald Knuth"
        self.article_form["title"] = "Structured Programming with go to Statements"
        self.article_form["year"] = "1974"
        self.article_form["publisher"] = "Association for Computing Machinery"

        result = Citation(self.article_form).generate_bibtex()

        self.assertTrue(result.startswith("@article{knuthstatements74,\n"))


    def test_field_alignment_uses_longest_field_name(self):
        self.article_form["annote"] = "extra"

        result = Citation(self.article_form).generate_bibtex()

        self.assertIn('  author  = {author}', result)
        self.assertIn('  annote  = {extra}', result)


    def test_fields_appear_in_input_order(self):
        self.article_form["volume"] = "2"
        self.article_form["pages"] = "10--20"

        result = Citation(self.article_form).generate_bibtex()

        self.assertLess(result.index('journal ='), result.index('year    ='))
        self.assertLess(result.index('year    ='), result.index('volume  ='))
        self.assertLess(result.index('volume  ='), result.index('pages   ='))

    def test_entry_type_is_in_output(self):
        result = Citation(self.article_form).generate_bibtex()
        self.assertTrue(result.startswith("@article{"))
        self.assertTrue(result.endswith("\n}"))


    def test_empty_optional_values_are_omitted(self):
        self.article_form["note"] = ""
        self.article_form["volume"] = ""

        result = Citation(self.article_form).generate_bibtex()

        self.assertNotIn("note", result)
        self.assertNotIn("volume", result)

    def test_whitespace_between_pages_gets_stripped_out(self):
        self.article_form["pages"] = "1,   20,   30"
        result = Citation(self.article_form).generate_bibtex()
        self.assertIn('  pages   = {1,20,30}\n', result)

        self.article_form["pages"] = "1,   100--23333,         30"
        result = Citation(self.article_form).generate_bibtex()
        self.assertIn('  pages   = {1,100--23333,30}\n', result)

        self.article_form["pages"] = "33,  1,  5--10,    30"
        result = Citation(self.article_form).generate_bibtex()
        self.assertIn('  pages   = {33,1,5--10,30}\n', result)

