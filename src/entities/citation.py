from util import UserInputError
from entities.citation_validator import CitationValidator

class Citation:
    def __init__(self, form):
        self._entry_types = {
                "article": Article(form)
                }

        if not form["entry_type"] or not form["entry_type"] in self._entry_types:
            raise UserInputError("Virheellinen viitemerkintätyyppi.")

        self._entry_type = form["entry_type"]
        self._citation_object = self._entry_types[self._entry_type]

    def generate_bibtex(self):
        return self._citation_object.generate_bibtex()

    def get_fields(self):
        fields = self._citation_object.get_fields()
        fields["entry_type"] = self._entry_type
        return fields

class Article:
    def __init__(self, form):
        self._required_fields = ["author", "title", "journal", "year"]
        self._optional_fields = ["volume", "number", "pages", "month", "note", "annote"]
        self._validator = CitationValidator(self._required_fields, self._optional_fields)
        self._validator.validate(form)

    def get_fields(self):
        return self._validator.get_validated_fields()

    def generate_bibtex(self):
        pass
