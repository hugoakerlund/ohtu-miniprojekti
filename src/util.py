class UserInputError(Exception):
    pass

def get_citation_form(request):
    fields = ["entry_type", "author", "title", "journal", "year", "volume",
              "number", "pages", "month", "note", "annote", "howpublished",
              "editor", "series", "address", "organization", "publisher", "booktitle"]
    form = {}
    for field in fields:
        form[field] = request.form.get(field, "").strip() or None
    return form
