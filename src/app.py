from flask import redirect, render_template, request, jsonify, flash
from db_helper import reset_db
from repositories.citation_repository import get_citations, get_entry_types, create_citation, delete_citation, find_citation
from config import app, test_env
from util import validate_citation, get_citation, get_ids_to_delete

@app.route("/")
def index():
    citations = get_citations()
    return render_template("index.html", citations=citations)

@app.route("/new_citation")
def new():
    entry_types = get_entry_types()
    return render_template("new_citation.html", entry_types=entry_types)


@app.route("/create_citation", methods=["POST"])
def citation_creation():
    form = get_citation(request)
    try:
        validate_citation(form)
        create_citation(form)
        flash("Viite luotu.", "success")
        return redirect("/")
    except Exception as error:
        flash(str(error), "error")
        return redirect("/new_citation")

@app.route("/delete_citations", methods=["POST"])
def citation_deletion():
    ids = get_ids_to_delete(request)
    if len(ids) > 0:
        try:
            for id in ids:
                delete_citation(id)
            flash(f"Poistettu onnistuneesti {len(ids)} viitettä.", "success")
        except:
            flash(str(error), "error")
    return redirect("/")

@app.route("/search")
def search():
    query = request.args.get("query")
    if query:
        results = find_citation(query)
    else:
        query = ""
        results = []
    return render_template("search.html", query=query, results=results)

# testausta varten oleva reitti
if test_env:
    @app.route("/reset_db")
    def reset_database():
        reset_db()
        return jsonify({ 'message': "db reset" })

@app.route("/choose_citation_type", methods=["POST"])
def choose_citation_type():
    citation_type = request.form["type"]
    return render_template(f"new_{citation_type}.html")
