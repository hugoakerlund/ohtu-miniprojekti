import os
from entities.citation import Citation
from repositories.citation_repository import get_citation_by_id

def export_citations(citations, path):
    bibtex_contents = []
    for citation_id in citations:
        form = get_citation_by_id(citation_id)
        citation = Citation(form)
        bibtex = citation.generate_bibtex()
        bibtex_contents.append(bibtex)

    file_contents = "\n\n".join(bibtex_contents) + "\n"
    write_to_file(path, file_contents)

def write_to_file(path, contents):
    parts = path.split("/")
    directory = "/".join(parts[0:-1])
    os.makedirs(directory, exist_ok=True)
    with open(path, "w", encoding="utf-8") as file:
        file.write(contents)
