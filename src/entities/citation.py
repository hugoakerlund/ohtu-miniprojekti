from enum import Enum

class EntryType(Enum):
    ARTICLE = 1

class Citation:
    def __init__(self, title, author, entry_type):
        self._entry_types = {
                EntryType.ARTICLE: Article(title, author)
                }
        self.entry_type = self._entry_types[entry_type]

    def generate_bibtex(self):
        return self.entry_type.generate_bibtex()

    def __str__(self):
        return str(self.entry_type)



class Article:
    def __init__(self, title, author):
        self.title = title
        self.author = author

    def generate_bibtex(self):
        pass

    def __str__(self):
        return f"{self.title} by {self.author}"
