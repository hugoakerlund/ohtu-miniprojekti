from sqlalchemy import text
from config import db

def get_citation(citation_id):
    sql = text("""SELECT id, type, title, author, howpublished,
                         year, month, address, publisher,
                         edition, pages
                  FROM citations
                  WHERE id LIKE :citation_id""")
    result = db.session.execute(sql, {"citation_id": citation_id})
    return [dict(row) for row in result.mappings().all()]

def find_citation(query):
    sql = text("""SELECT type, title, author, howpublished,
                        year, month, address, publisher,
                        edition, pages
                  FROM citations
                  WHERE title LIKE :query
                  OR author LIKE :query
                  OR publisher LIKE :query
                  ORDER BY id""")
    result = db.session.execute(sql, {"query": f"%{query}%"})
    return [dict(row) for row in result.mappings().all()]
