# Solution structure

This project is a small web application for storing and searching citations.
The application is built with Flask and uses SQLite as its database.

## What happens when the application runs?

`src/index.py` starts the Flask web server. Flask receives a browser request
and chooses a function in `src/app.py` to handle it. That function either
loads data, saves data, or renders an HTML page from `src/templates/`.

For example, the normal page-loading flow is:

1. The browser requests `/`.
2. The route in `src/app.py` calls `get_citations()`.
3. `get_citations()` in `src/repositories/citation_repository.py` sends a
   `SELECT` query to the database.
4. The returned rows are passed to `templates/index.html`.
5. Flask sends the rendered HTML back to the browser.

The create-citation flow is similar, but `src/util.py` first reads and
validates the submitted form before the repository inserts anything.

## Important modules

- **`src/index.py`** is the program entry point. Running it starts Flask on
  port 5001.
- **`src/app.py`** contains the web routes. It connects URLs to Python
  functions, calls other modules, and chooses which HTML template to show.
- **`src/config.py`** creates the Flask application and configures the
  database connection from `DATABASE_URL`.
- **Flask** is the web framework. It handles HTTP requests and responses,
  routing, templates, redirects, and flash messages.
- **SQLAlchemy** is a Python library for communicating with databases. It
  manages database connections and database sessions, so Python code can
  execute SQL without opening a new connection for every query.
- **Flask-SQLAlchemy** connects SQLAlchemy to Flask. In this project,
  `db.session` is the object used to execute queries and commit changes.
  The project uses SQLAlchemy mainly to run written SQL statements; it does
  not define a separate Python class for every database table.
- **`src/repositories/citation_repository.py`** is the main data-access
  module. It reads citations and entry types and inserts new citations.
  Keeping these queries here means that routes do not need to contain SQL.
- **`src/citations.py`** contains the search query. It searches citation
  titles, authors, and publishers with SQL `LIKE`.
- **`src/db_helper.py`** initializes and maintains the database. It can create
  the tables, fill `entry_types`, list tables, read all citations, or clear
  citation rows.
- **`src/schema.sql`** describes the two tables: `citations` and
  `entry_types`.
- **`src/entities/citation.py`** contains a `Citation` class for representing
  one citation. The current queries return dictionaries directly, so this
  class is not required by the current route flow.
- **`src/templates/`** contains the HTML pages and **`src/static/`** contains
  CSS.
- **`src/tests/`** contains unit tests and **`src/story_tests/`** contains
  Robot Framework acceptance tests.

## Which parts use the database?

The database is configured in `src/config.py` using `DATABASE_URL`. In local
development it is normally the SQLite file
`src/instance/database.db`. SQLite is convenient because the database is one
file and does not require a separate database server to be running.

These modules use `db.session` and therefore interact with the database:

- `src/repositories/citation_repository.py`
  - `SELECT`s citations and entry types
  - `INSERT`s new citations
  - calls `commit()` to save changes
- `src/citations.py`
  - `SELECT`s citations matching a search term
- `src/db_helper.py`
  - reads table names
  - drops and creates tables using `schema.sql`
  - deletes citation rows
  - inserts the allowed entry types

`src/app.py` itself does not contain SQL. Its routes call the repository and
helper functions instead. `src/util.py` also does not use the database; it
only checks the form data before it is sent to the repository.

## `util.py` in plain language

`src/util.py` is the boundary between the browser form and the rest of the
program.

- `get_citation(request)` reads the form fields, removes whitespace, and
  changes empty strings to `None`.
- `validate_citation(form)` runs all validation checks and raises
  `UserInputError` when the form is invalid.
- The checks require a title, citation type, and author.
- The citation type must be one of the allowed BibTeX types.
- Every non-empty field can be at most 100 characters.
- The year must be numeric and cannot be in the future.
- The month must be between 1 and 12.
- Pages must look like an ordered range such as `10-15`.

The create route catches the validation error, shows an error message, and
does not call the database insert when validation fails.

## Using the database without running Flask

The web server is not required for database administration or for reading
rows. The database is a file, and a separate Python process can open it.

### Create or reset the local database

From the repository root, run:

```text
uv run python src/db_helper.py
```

This reads `src/schema.sql`, creates both tables, and seeds the entry types.
It **drops existing tables first**, so running this command deletes existing
data. Use it when setting up a new database or when deliberately recreating
the schema.
