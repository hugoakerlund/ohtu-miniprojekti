"""Import DOI metadata and expose it as a normalized citation object."""

from dataclasses import dataclass
import json
import re
from typing import Any, NoReturn
from urllib.error import HTTPError, URLError
from urllib.parse import quote
from urllib.request import Request, urlopen

'''
Hey handsome, this class already exists in the codebase, use that instead.
TODO: src/repositories/citation_repository.py has ALL_FIELDS that can be used to 
create a citation object.
'''

# pylint: disable=too-many-instance-attributes
@dataclass
class Citation:
    """Core bibliographic fields for a DOI reference."""

    authors: list[str]
    title: str
    journal: str
    year: int | None
    volume: str | None
    issue: str | None
    pages: str | None
    doi: str
    url: str | None

# This looks needlessly complex but it simply validates the DOI format and removes the URL part.
def _normalize_doi(doi: str) -> str:
    normalized_doi = re.sub(
        r"^https?://(?:dx\.)?doi\.org/", "", doi.strip(), flags=re.IGNORECASE
    )
    if not normalized_doi or not re.match(r"^10\.\d{4,9}/\S+$", normalized_doi):
        raise ValueError("Please provide a valid DOI")
    return normalized_doi

# Error handling
def _raise_crossref_error(exc: Exception, doi: str) -> NoReturn:
    if isinstance(exc, HTTPError):
        if exc.code == 404:
            raise ValueError(f"DOI not found: {doi}") from exc
        raise RuntimeError(f"Crossref request failed (HTTP {exc.code})") from exc
    if isinstance(exc, (URLError, TimeoutError)):
        raise RuntimeError("Could not retrieve DOI metadata from Crossref") from exc
    raise RuntimeError("Crossref returned invalid DOI metadata") from exc

# Takes care of fetching over network and parsing.
def _fetch_crossref_record(doi: str) -> dict[str, Any]:
    request = Request(
        "https://api.crossref.org/works/" + quote(doi, safe="/"),
        headers={"User-Agent": "miniprojekti DOI citation importer/1.0"},
    )
    try:
        with urlopen(request, timeout=15) as response:
            return json.loads(response.read().decode("utf-8"))["message"]
    except (HTTPError, URLError, TimeoutError, json.JSONDecodeError, KeyError) as exc:
        _raise_crossref_error(exc, doi)

# Creates the Citation object from record and original doi.
# Record is a dict with metadata
# It is used here instead of a normal dictionary because it's what the Crossref API returns.
def _citation_from_record(record: dict[str, Any], doi: str) -> Citation:
    publication = (
        record.get("published-print")
        or record.get("published-online")
        or record.get("created", {})
    )
    date_parts = publication.get("date-parts", [[]])
    year = date_parts[0][0] if date_parts and date_parts[0] else None
    authors = [
        " ".join(value for value in (person.get("given"), person.get("family")) if value)
        for person in record.get("author", [])
    ]
    return Citation(
        authors=authors,
        title=(record.get("title") or [""])[0],
        journal=(record.get("container-title") or [""])[0],
        year=year,
        volume=record.get("volume"),
        issue=record.get("issue"),
        pages=record.get("page") or record.get("article-number"),
        doi=record.get("DOI", doi),
        url=record.get("URL"),
    )

# Main function to be called from other modules
def import_doi_reference(doi: str) -> Citation:
    """
    Fetch metadata from Crossref for a DOI string or DOI URL.

    Raises ValueError for invalid or unknown DOIs and RuntimeError when
    Crossref cannot provide valid metadata.
    """
    # Record is a dict with metadata
    # It is used here instead of a normal dictionary because it's what the Crossref API returns.
    normalized_doi = _normalize_doi(doi)
    record = _fetch_crossref_record(normalized_doi)
    return _citation_from_record(record, normalized_doi)


if __name__ == "__main__":
    # Example usage: python src/doi_import.py 10.1038/s41586-020-2649-2
    citation = import_doi_reference("10.1038/s41586-020-2649-2")
    print(
        f"{', '.join(citation.authors)}. {citation.title}. {citation.journal} "
        f"{citation.year};{citation.volume}({citation.issue}):{citation.pages}. "
        f"doi:{citation.doi}. URL: {citation.url}"
    )

    citation = import_doi_reference(
        "https://doi.org/10.1016/j.jmatprotec.2006.03.052"
    )
    print(
        f"{', '.join(citation.authors)}. {citation.title}. {citation.journal} "
        f"{citation.year};{citation.volume}({citation.issue}):{citation.pages}. "
        f"doi:{citation.doi}. URL: {citation.url}"
    )
