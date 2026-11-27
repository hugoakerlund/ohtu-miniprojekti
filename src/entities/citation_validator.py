import re
from datetime import datetime
from util import UserInputError

class CitationValidator:
    def __init__(self, required_fields, optional_fields):
        self._field_to_validator = {
                "author": self._validate_author,
                "title": self._validate_title,
                "journal": self._validate_journal,
                "year": self._validate_year,
                "volume": self._validate_volume,
                "number": self._validate_number,
                "pages": self._validate_pages,
                "month": self._validate_month,
                "note": self._validate_note,
                "annote": self._validate_annote,
                "howpublished": self._validate_howpublished,
                "booktitle": self._validate_booktitle,
                "editor": self._validate_editor,
                "series": self._validate_series,
                "address": self._validate_address,
                "organization": self._validate_organization,
                "publisher": self._validate_publisher,
                }
        self._field_length_limit = {
                "author": 5000,
                "title": 2000,
                "journal": 500,
                "year": 4,
                "volume": 100,
                "number": 100,
                "pages": 100,
                "month": 2,
                "note": 5000,
                "annote": 10000,
                "howpublished": 1000,
                "booktitle": 1000,
                "editor": 5000,
                "series": 1000,
                "address": 500,
                "organization": 1000,
                "publisher": 1000,
                }
        self._required_fields = required_fields
        self._optional_fields = optional_fields
        self._validated_fields = {field: "" for field in self._field_to_validator.keys()}

    def get_validated_fields(self):
        return self._validated_fields

    def validate(self, form):
        form = self._convert_to_str(form)
        self._validate_required_fields(form)
        self._validate_optional_fields(form)

    def _convert_to_str(self, form):
        result = {}
        for key, value in form.items():
            if value is not None:
                result[key] = str(value)
            else:
                result[key] = value
        return result

    def _validate_required_fields(self, form):
        for required_field in self._required_fields:
            if required_field not in form:
                raise UserInputError(f"Kenttä {required_field} on pakollinen.")
            validated_field = self._validate_field(required_field, form[required_field])
            self._validated_fields[required_field] = validated_field

    def _validate_optional_fields(self, form):
        for optional_field in self._optional_fields:
            if form[optional_field]:
                validated_field = self._validate_field(optional_field, form[optional_field])
                self._validated_fields[optional_field] = validated_field

    def _validate_field(self, field, value):
        self._validate_field_length(field, value)
        return self._field_to_validator[field](value)

    def _validate_field_length(self, field, value):
        max_length = self._field_length_limit[field]
        if len(value) > max_length:
            raise UserInputError(f"Kentän {field} maksimipituus on {max_length} merkkiä.")


    def _validate_text(self, value):
        if value and not value.strip():
            raise UserInputError("Kenttä ei voi olla tyhjä.")
        return value.strip()

    def _validate_author(self, value):
        return self._validate_text(value)

    def _validate_title(self, value):
        return self._validate_text(value)

    def _validate_journal(self, value):
        return self._validate_text(value)

    def _validate_year(self, value):
        if not value.isdigit():
            raise UserInputError("Julkaisuvuoden on oltava numeerinen.")

        year = int(value)
        if year > datetime.now().year or year < 0:
            raise UserInputError("Virheellinen julkaisuvuosi.")
        return value

    def _validate_volume(self, value):
        if not value.isdigit():
            raise UserInputError("Vuosikerran on oltava numeerinen.")
        return value

    def _validate_number(self, value):
        if not value.isdigit():
            raise UserInputError("Numeron on oltava numeerinen.")
        return value

    def _validate_pages(self, value):
        sections = []
        for section in value.split(","):
            section = section.strip()
            match = re.fullmatch(r"([0-9]+)(?:\s*--\s*([0-9]+))?", section)

            if not match:
                raise UserInputError("Virheelliset sivunumerot.")

            start, end = match.groups()
            if end is not None and int(start) > int(end):
                raise UserInputError("Virheelliset sivunumerot.")
            sections.append(section)
        return ",".join(sections)

    def _validate_month(self, value):
        if not value.isdigit():
            raise UserInputError("Kuukauden on oltava numeerinen.")

        month = int(value)
        if month < 1 or month > 12:
            raise UserInputError("Virheellinen julkaisukuukausi.")
        return value

    def _validate_note(self, value):
        return  self._validate_text(value)

    def _validate_annote(self, value):
        return self._validate_text(value)

    def _validate_howpublished(self, value):
        return self._validate_text(value)

    def _validate_booktitle(self, value):
        return self._validate_text(value)

    def _validate_editor(self, value):
        return self._validate_text(value)

    def _validate_series(self, value):
        return self._validate_text(value)

    def _validate_address(self, value):
        return self._validate_text(value)

    def _validate_organization(self, value):
        return self._validate_text(value)

    def _validate_publisher(self, value):
        return self._validate_text(value)
