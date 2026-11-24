class UserInputError(Exception):
    pass

def get_citation(request):
    fields = ["entry_type", "author", "title", "journal", "year", "volume",
              "number", "pages", "month", "note", "annote", "howpublished"]
    form= {}
    for field in fields:
        form[field] = request.form.get(field, "").strip() or None
    return form
