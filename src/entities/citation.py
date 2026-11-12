class Citation:
    def __init__(self, id, type, title, author):
        self.id = id
        self.type = type
        self.title = title
        self.author = author

    def __str__(self):
        return f"{self.title} by {self.author}"
