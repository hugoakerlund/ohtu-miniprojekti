import unittest
from entities.citation import Citation
from util import validate_citation, UserInputError

class TestCitationValidation(unittest.TestCase):
    def setUp(self):
        self.citation_fields = {
                "id": "",
                "type": "",
                "title": "",
                "author": "",
                "howpublished": "",
                "year": "",
                "month": "",
                "address": "",
                "publisher": "",
                "edition": "",
                "pages": ""
            }

    def test_citation_without_required_fields_raises_error(self):
        with self.assertRaises(UserInputError):
            validate_citation(self.citation_fields)

            self.citation_fields["type"] = "Article"
            validate_citation(self.citation_fields)

            self.citation_fields["title"] = "Title"
            validate_citation(self.citation_fields)

        try:
            self.citation_fields["title"] = "Title"
            self.citation_fields["type"] = "Article"
            self.citation_fields["author"] = "Author"
            validate_citation(self.citation_fields)

        except UserInputError:
            self.fail("validate_citation() raised exception unexpectedly.")
