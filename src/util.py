from datetime import datetime

MAX_FIELD_LENGTH = 100

class UserInputError(Exception):
    pass

def get_citation(request):
    fields = ["title", "type", "author", "howpublished", "year", "month",
              "address", "publisher", "edition", "pages"]
    form= {}
    for field in fields:
        form[field] = request.form.get(field, "").strip() or None
    return form

def validate_citation(form):
    errors = []
    errors.append(validate_required_fields(form))
    errors.append(validate_type(form))
    errors.append(validate_lengths(form))
    errors.append(validate_year(form))
    errors.append(validate_month(form))
    errors.append(validate_pages(form))

    for error in errors:
        if error:
            raise UserInputError(error)

def validate_required_fields(form):
    if not form["title"] or not form["type"] or not form["author"]:
        return UserInputError("Otsikko, viitemerkintätyyppi ja tekijä ovat pakolliset kentät.")
    return None

def validate_type(form):
    entry_types = [
            "article"
            ]
    if form["type"] not in entry_types:
        return UserInputError("Virheellinen viitemerkintätyyppi.")
    return None

def validate_lengths(form):
    for value in form.values():
        if value and len(value) > MAX_FIELD_LENGTH:
            return UserInputError(f"Kenttien maksimipituus on {MAX_FIELD_LENGTH} merkkiä.")
    return None

def validate_year(form):
    if form["year"]:
        if not form["year"].isdigit():
            return UserInputError("Julkaisuvuoden on oltava numeerinen.")

        year = int(form["year"])
        if year > datetime.now().year or year < 0:
            return UserInputError("Virheellinen julkaisuvuosi.")
    return None

def validate_month(form):
    if form["month"]:
        if not form["month"].isdigit():
            return UserInputError("Kuukauden on oltava numeerinen.")

        month = int(form["month"])
        if month < 1 or month > 12:
            return UserInputError("Virheellinen julkaisukuukausi.")
    return None

def validate_pages(form):
    if form["pages"]:
        pages = form["pages"].split("-")
        if not len(pages) == 2 or not pages[0].isdigit() or not pages[1].isdigit() \
                or int(pages[0]) > int(pages[1]):
            return UserInputError("Virheelliset sivunumerot.")
    return None
