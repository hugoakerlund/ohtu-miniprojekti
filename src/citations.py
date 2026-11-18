from sqlalchemy import text
from config import db

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
