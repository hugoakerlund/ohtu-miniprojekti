CREATE TABLE citations (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  type TEXT REFERENCES entry_types(name),
  title TEXT NOT NULL,
  author TEXT NOT NULL,
  howpublished TEXT,
  year INTEGER,
  month TEXT,
  address TEXT,
  publisher TEXT,
  edition TEXT,
  pages TEXT
);

CREATE TABLE entry_types (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL
);
