from flask import redirect, render_template, request, jsonify, flash, send_file
from db_helper import reset_db
from repositories.citation_repository import get_citations, get_entry_types, \
     create_citation, delete_citation, find_citation
from config import app, test_env, export_dir
from util import UserInputError, get_citation_form
from export import export_citations
from entities.citation import Citation

@app.route("/")
def index():
    citations = get_citations()
    return render_template("index.html", citations=citations)

@app.route("/new_citation")
def new_citation():
    entry_types = get_entry_types()
    return render_template("new_citation.html", entry_types=entry_types)

@app.route("/choose_citation_type", methods=["POST"])
def choose_citation_type():
    citation_type = request.form["entry_type"]
    return render_template(f"new_{citation_type}.html")

@app.route("/create_citation", methods=["POST"])
def citation_creation():
    form = get_citation_form(request)
    try:
        citation = Citation(form)
        create_citation(citation.get_fields())
        flash("Viite luotu.", "success")
        return redirect("/")
    except UserInputError as error:
        flash(str(error), "error")
        return render_template(f"/new_{form['entry_type']}.html")

@app.route("/delete_citations", methods=["POST"])
def citation_deletion():
    citations = list(request.form)
    if len(citations) > 0:
        for citation in citations:
            delete_citation(citation)
        flash(f"Poistettu onnistuneesti {len(citations)} viitettä.", "success")
    return redirect("/")

@app.route("/export_citations", methods=["POST"])
def citation_export():
    citations = list(request.form)
    file_name = "citations.bibtex"
    path = export_dir + "/" + file_name
    try:
        export_citations(citations, path)
        return send_file(path, as_attachment=True)
    except UserInputError as error:
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
