from config import db, app
from sqlalchemy import text
import os

def reset_db():
    print(f"Clearing contents from table citations")
    sql = text(f"DELETE FROM citations")
    db.session.execute(sql)
    db.session.commit()

def tables():
    """Returns all table names from the database"""
    sql = text(
            "SELECT name FROM sqlite_master "
            "WHERE type = 'table' AND name NOT LIKE 'sqlite_%'"
            )

    result = db.session.execute(sql)
    return [row[0] for row in result.fetchall()]

def get_all_citations():
    """Return every row in the citations table."""
    sql = text("SELECT * FROM citations")
    result = db.session.execute(sql)
    return [dict(row) for row in result.mappings().all()]

def setup_db():
    """
    Creating the database
    If database tables already exist, those are dropped before the creation
    """
    tables_in_db = tables()
    if len(tables_in_db) > 0:
        print(f"Tables exist, dropping: {', '.join(tables_in_db)}")
        for table in tables_in_db:
            sql = text(f"DROP TABLE {table}")
            db.session.execute(sql)
        db.session.commit()

    print("Creating database")

    # Read schema from schema.sql file
    schema_path = os.path.join(os.path.dirname(__file__), 'schema.sql')
    with open(schema_path, 'r') as f:
        schema_sql = f.read().strip()

    for statement in schema_sql.split(";"):
        sql = text(statement)
        db.session.execute(sql)
    db.session.commit()

def seed_table_entry_types():
    entry_types = [
            "article",
            "book",
            "booklet",
            "conference",
            "inbook",
            "incollection",
            "inproceedings",
            "manual",
            "mastersthesis",
            "misc",
            "phdthesis",
            "proceedings",
            "techreport",
            "unpublished",
            ]

    for entry_type in entry_types:
        params = ({"name": entry_type})
        db.session.execute(text("INSERT INTO entry_types (name) VALUES (:name)"), params)
    db.session.commit()


if __name__ == "__main__":
    with app.app_context():
        setup_db()
        seed_table_entry_types()
