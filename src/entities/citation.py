from util import UserInputError
from entities.citation_validator import CitationValidator

class Citation:
    def __init__(self, form):
        self._entry_types = {
                "article": Article,
                "book": Book,
                "inproceedings": Inproceedings
                }

        if not form["entry_type"] or not form["entry_type"] in self._entry_types:
            raise UserInputError("Virheellinen viitemerkintätyyppi.")

        self._entry_type = form["entry_type"]
        self._citation_object = self._entry_types[self._entry_type](form)

    def generate_bibtex(self):
        fields = self.get_fields()
        cite_key = self.generate_citekey(fields)
        first_line = "@" + fields["entry_type"] + "{" + cite_key + ",\n"
        last_line = "\n}"
        indent = "  "

        lines = [
            (str(key), value)
            for key, value in fields.items()
            if key != "entry_type" and value
        ]

        key_width = max((len(key) for key, _ in lines), default=0)

        formatted_lines = [
                f'{indent}{key:<{key_width}} = "{value}"'
                for key, value in lines
        ]

        joined_lines = ",\n".join(formatted_lines)
        return  first_line + joined_lines + last_line

    def generate_citekey(self, fields):
        author = fields["author"].strip().split(' ')[-1].lower()
        keyword = fields["title"].strip().split(' ')[-1].lower()
        year = fields["year"]
        if len(year) >= 2:
            year = year[-2:]
        return author + keyword + year

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

    def set_field(self, field, value):
        pass

    def get_fields(self):
        return self._validator.get_validated_fields()

class Book:
    def __init__(self, form):
        self._required_fields = ["author", "editor", "title", "publisher", "year"]
        self._optional_fields = ["volume", "number", "pages", "month", "note"]
        self._validator = CitationValidator(self._required_fields, self._optional_fields)
        self._validator.validate(form)

    def set_field(self, field, value):
        pass

    def get_fields(self):
        return self._validator.get_validated_fields()

class Inproceedings:
    def __init__(self, form):
        self._required_fields = ["author", "title", "booktitle", "year"]
        self._optional_fields = ["editor", "volume", "number", "series",
                                 "pages", "month", "address", "organization",
                                 "publisher", "note", "annote"]
        self._validator = CitationValidator(self._required_fields, self._optional_fields)
        self._validator.validate(form)

    def set_field(self, field, value):
        pass

    def get_fields(self):
        return self._validator.get_validated_fields()
