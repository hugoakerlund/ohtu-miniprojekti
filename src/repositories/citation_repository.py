from sqlalchemy import text
from config import db

ALL_FIELDS = """entry_type, author, title, journal, year,
                volume, number, pages, month, note, annote,
                howpublished"""

ALL_VALUES =  """:entry_type, :author, :title, :journal, :year,
                 :volume, :number, :pages, :month, :note, :annote,
                 :howpublished"""

def get_citations():
    sql = f"""SELECT id, {ALL_FIELDS} FROM citations"""
    result = db.session.execute(text(sql))
    return [dict(row) for row in result.mappings().all()]

def get_entry_types():
    sql = "SELECT name FROM entry_types"
    result = db.session.execute(text(sql))
    entry_types = result.fetchall()
    return [entry[0] for entry in entry_types]

def create_citation(form):
    sql = f"""INSERT INTO citations ({ALL_FIELDS})
             VALUES ({ALL_VALUES})"""
    db.session.execute(text(sql), form)
    db.session.commit()

def delete_citation(citation_id):
    sql = """DELETE FROM citations where id = :id"""
    db.session.execute(text(sql), {"id": citation_id})
    db.session.commit()


def find_citation(query):
    sql = f"""SELECT id, {ALL_FIELDS}
              FROM citations
              WHERE title LIKE :query
                 OR author LIKE :query
                 OR journal LIKE :query
              ORDER BY id"""
    result = db.session.execute(text(sql), {"query": f"%{query}%"})
    return [dict(row) for row in result.mappings().all()]
