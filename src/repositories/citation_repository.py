from config import db
from sqlalchemy import text

from entities.citation import Citation

def get_citations():
    result = db.session.execute(text("SELECT id, type, title, author FROM citations"))
    return []

def get_entry_types():
    sql = "SELECT name FROM entry_types"
    result = db.session.execute(text(sql))
    entry_types = result.fetchall()
    return [entry[0] for entry in entry_types]

def create_citation(form):
    sql = """INSERT INTO citations (type, title, author, howpublished,
             year, month, address, publisher, edition, pages)
             VALUES (:type, :title, :author, :howpublished,
             :year, :month, :address, :publisher, :edition, :pages)"""

    db.session.execute(text(sql), form)
    db.session.commit()
