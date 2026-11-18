from config import db

def find_citation(query):
    sql = """SELECT type, title, author, howpublished, year, month, address, publisher, edition, pages
             FROM citations
             WHERE title LIKE ? OR author LIKE ? OR publisher LIKE ?
             ORDER BY id"""
    like = query
    result = db.session.execute(sql, [like])
    return [row[0:10] for row in result.fetchall()]
