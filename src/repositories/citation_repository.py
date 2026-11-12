from config import db
from sqlalchemy import text

from entities.citation import Citation

def get_citations():
    result = db.session.execute(text("SELECT id, type, title, author FROM citations"))
    citations = result.fetchall()
    return [Citation(citation[0], citation[1], citation[2]) for citation in citations]

def create_citation():
    pass
