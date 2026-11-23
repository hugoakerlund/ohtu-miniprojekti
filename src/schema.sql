PRAGMA foreign_keys = ON;

CREATE TABLE entry_types (
  name TEXT PRIMARY KEY
);

CREATE TABLE citations (
  id INTEGER PRIMARY KEY,
  entry_type TEXT NOT NULL REFERENCES entry_types(name),
  author TEXT NOT NULL,
  title TEXT NOT NULL,
  journal TEXT,
  year INTEGER,
  volume TEXT,
  number TEXT,
  pages TEXT,
  month TEXT,
  note TEXT,
  annote TEXT,
  howpublished TEXT
);
