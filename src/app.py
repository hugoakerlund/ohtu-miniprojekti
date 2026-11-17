from flask import redirect, render_template, request, jsonify, flash
from db_helper import reset_db
from repositories.citation_repository import get_citations, get_entry_types, create_citation
from config import app, test_env
from util import validate_citation, get_citation

@app.route("/")
def index():
    citations = get_citations()
    return render_template("index.html", citations=citations)

@app.route("/new_citation")
def new():
    entry_types = get_entry_types()
    return render_template("new_citation.html", entry_types=entry_types)


@app.route("/create_citation", methods=["POST"])
def citaton_creation():
    form = get_citation(request)
    try:
        validate_citation(form)
        create_citation(form)
        return redirect("/")
    except Exception as error:
        print("error", str(error))
        flash(str(error))
        return  redirect("/new_citation")

@app.route("/search")
def search():
    return render_template("search.html")

@app.route("/search", methods=["POST"])
def search_citations():
    return redirect("https://der-fuehrer.org")

# testausta varten oleva reitti
if test_env:
    @app.route("/reset_db")
    def reset_database():
        reset_db()
        return jsonify({ 'message': "db reset" })
