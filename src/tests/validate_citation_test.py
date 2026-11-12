import unittest
from entities.citation import Citation
from util import validate_citation, UserInputError

class TestCitationValidation(unittest.TestCase):
    def setUp(self):
        pass

    def test_citation_without_required_fields_raises_error(self):
        with self.assertRaises(UserInputError):
            validate_citation(Citation(1, "", "", ""))
            validate_citation(Citation(1, "Article", "", ""))
            validate_citation(Citation(1, "Article", "Title", ""))

        try:
            validate_citation(Citation(1, "Article", "Title", "Author"))
        except UserInputError:
            self.fail("validate_citation() raised exception unexpectedly.")
