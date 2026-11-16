from entities.citation import Citation

class UserInputError(Exception):
    pass

def get_citation(request):
    form= {}
    form["id"] = request.form.get("id", "").strip() or None
    form["type"] = request.form.get("type", "").strip() or None
    form["title"] = request.form.get("title", "").strip() or None
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
    if not form['title'] or not form['type'] or not form['author']:
        raise UserInputError
