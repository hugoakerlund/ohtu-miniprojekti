from datetime import datetime

class UserInputError(Exception):
    pass

def get_citation(request):
    form= {}
    form["title"] = request.form.get("title", "").strip() or None
    form["type"] = request.form.get("type", "").strip() or None
    form["author"] = request.form.get("author", "").strip() or None
    form["howpublished"] = request.form.get("howpublished", "").strip() or None
    form["year"] = request.form.get("year", "").strip() or None
    form["month"] = request.form.get("month", "").strip() or None
    form["address"] = request.form.get("address", "").strip() or None
    form["publisher"] = request.form.get("publisher", "").strip() or None
    form["edition"] = request.form.get("edition", "").strip() or None
    form["pages"] = request.form.get("pages", "").strip() or None
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
        if error: raise UserInputError(error)

def validate_required_fields(form):
    if not form["title"] or not form["type"] or not form["author"]:
        return UserInputError("Otsikko, viitemerkintätyyppi ja tekijä ovat pakolliset kentät.")

def validate_type(form):
    entry_types = [
            "article",
            "book",
            "booklet",
            "conference",
            "inbook",
            "incollection",
            "inproceedings",
            "manual",
            "mastersthesis",
            "misc",
            "phdthesis",
            "proceedings",
            "techreport",
            "unpublished",
            ]

    if form["type"] not in entry_types:
        return UserInputError("Virheellinen viitemerkintätyyppi.")

def validate_lengths(form):
    MAX_LENGTH = 100
    for value in form.values():
        if value and len(value) > MAX_LENGTH:
            return UserInputError(f"Kenttien maksimipituus on {MAX_LENGTH} merkkiä.")

def validate_year(form):
    if form["year"]:
        if not form["year"].isdigit():
            return UserInputError("Julkaisuvuoden on oltava numeerinen.")

        year = int(form["year"])
        if year > datetime.now().year or year < 0:
            return UserInputError("Virheellinen julkaisuvuosi.")

def validate_month(form):
    if form["month"]:
        if not form["month"].isdigit():
            return UserInputError("Kuukauden on oltava numeerinen.")

        month = int(form["month"])
        if month > datetime.now().month or month < 1:
            return UserInputError("Virheellinen julkaisukuukausi.")

def validate_pages(form):
    if form["pages"]:
        pages = form["pages"].split("-")
        if not len(pages) == 2 or not pages[0].isdigit() or not pages[1].isdigit() \
                or int(pages[0]) > int(pages[1]):
            return UserInputError("Virheelliset sivunumerot.")
