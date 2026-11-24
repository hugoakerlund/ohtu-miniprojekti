from datetime import datetime
from util import UserInputError

MAX_FIELD_LENGTH = 100

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
        self._required_fields = required_fields
        self._optional_fields = optional_fields
        self._validated_fields = {field: "" for field in self._field_to_validator.keys()}

    def validate(self, form):
        self._validate_field_lengths(form)
        self._validate_required_fields(form)
        self._validate_optional_fields(form)

    def get_validated_fields(self):
        return self._validated_fields

    def _validate_field_lengths(self, form):
        for key, value in form.items():
            if value and len(value) > MAX_FIELD_LENGTH:
                raise UserInputError(f"Kentän {key} maksimipituus on {MAX_FIELD_LENGTH} merkkiä.")


    def _validate_required_fields(self, form):
        for required_field in self._required_fields:
            if not form[required_field]:
                raise UserInputError(f"Kenttä {required_field} on pakollinen.")
            self._validate_field(required_field, form[required_field])
            self._validated_fields[required_field] = form[required_field]

    def _validate_optional_fields(self, form):
        for optional_field in self._optional_fields:
            if form[optional_field]:
                self._validate_field(optional_field, form[optional_field])
            self._validated_fields[optional_field] = form[optional_field]

    def _validate_field(self, field, value):
        self._field_to_validator[field](value)

    def _validate_text(self, value):
        if not value.strip():
            raise UserInputError("Kenttä ei voi olla tyhjä.")

    def _validate_author(self, value):
        self._validate_text(value)

    def _validate_title(self, value):
        self._validate_text(value)

    def _validate_journal(self, value):
        self._validate_text(value)

    def _validate_year(self, value):
        if not value.isdigit():
            raise UserInputError("Julkaisuvuoden on oltava numeerinen.")

        year = int(value)
        if year > datetime.now().year or year < 0:
            raise UserInputError("Virheellinen julkaisuvuosi.")

    def _validate_volume(self, value):
        if not value.isdigit():
            raise UserInputError("Vuosikerran on oltava numeerinen.")

    def _validate_number(self, value):
        if not value.isdigit():
            raise UserInputError("Numeron on oltava numeerinen.")

    def _validate_pages(self, value):
        pages = value.split("-")
        if not len(pages) == 2 or not pages[0].isdigit() or not pages[1].isdigit() \
                or int(pages[0]) > int(pages[1]):
            raise UserInputError("Virheelliset sivunumerot.")

    def _validate_month(self, value):
        if not value.isdigit():
            raise UserInputError("Kuukauden on oltava numeerinen.")

        month = int(value)
        if month < 1 or month > 12:
            raise UserInputError("Virheellinen julkaisukuukausi.")

    def _validate_note(self, value):
        self._validate_text(value)

    def _validate_annote(self, value):
        self._validate_text(value)

    def _validate_howpublished(self, value):
        self._validate_text(value)

    def _validate_booktitle(self, value):
        self._validate_text(value)

    def _validate_editor(self, value):
        self._validate_text(value)

    def _validate_series(self, value):
        self._validate_text(value)

    def _validate_address(self, value):
        self._validate_text(value)

    def _validate_organization(self, value):
        self._validate_text(value)

    def _validate_howpublished(self, value):
        self._validate_text(value)

    def _validate_publisher(self, value):
        self._validate_text(value)
