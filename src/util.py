class UserInputError(Exception):
    pass

def validate_citation(citation):
    if not citation.title or not citation.type or not citation.author:
        raise UserInputError
