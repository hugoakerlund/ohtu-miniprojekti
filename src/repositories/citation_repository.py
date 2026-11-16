from config import db
from sqlalchemy import text

from entities.citation import Citation

def get_citations():
    result = db.session.execute(text("SELECT id, type, title, author FROM citations"))
    return []

def create_citation(form):
    print("creating citation")
    sql = """INSERT INTO citations (type, title, author, howpublished,
             year, month, address, publisher, edition, pages)
             VALUES (:type, :title, :author, :howpublished,
                     :year, :month, :address, :publisher, :edition, :pages)"""

    db.session.execute(text(sql), form)
    db.session.commit()

