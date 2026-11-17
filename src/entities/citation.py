class Citation:
    def __init__(self, fields):
        self.id = fields['id']
        self.type = fields['type']
        self.title = fields['title']
        self.author = fields['author']
        self.howpublished = fields['howpublished']
        self.year = fields['year']
        self.month = fields['month']
        self.address = fields['address']
        self.publisher = fields['publisher']
        self.edition = fields['edition']
        self.pages = fields['pages']

    def __str__(self):
        return f"{self.title} by {self.author}"
