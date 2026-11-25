"""Import DOI metadata and expose it as a normalized citation object."""

from dataclasses import dataclass
import json
import re
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import quote
from urllib.request import Request, urlopen


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


def import_doi_reference(doi: str) -> Citation:
	"""
	Fetches information from Crossref and returns it as Citation class boject.
	Accepts either a DOI string or DOI URL.
	Raises a bunch of errors if the DOI is invalind of something is fuggy with internet
	"""
	normalized_doi = re.sub(
		r"^https?://(?:dx\.)?doi\.org/", "", doi.strip(), flags=re.IGNORECASE
	)
	if not normalized_doi or not re.match(r"^10\.\d{4,9}/\S+$", normalized_doi):
		raise ValueError("Please provide a valid DOI")

	request = Request(
		"https://api.crossref.org/works/" + quote(normalized_doi, safe="/"),
		headers={"User-Agent": "miniprojekti DOI citation importer/1.0"},
	)
	try:
		with urlopen(request, timeout=15) as response:
			record: dict[str, Any] = json.loads(response.read().decode("utf-8"))["message"]
	except HTTPError as exc:
		if exc.code == 404:
			raise ValueError(f"DOI not found: {normalized_doi}") from exc
		raise RuntimeError(f"Crossref request failed (HTTP {exc.code})") from exc
	except (URLError, TimeoutError) as exc:
		raise RuntimeError("Could not retrieve DOI metadata from Crossref") from exc
	except (json.JSONDecodeError, KeyError) as exc:
		raise RuntimeError("Crossref returned invalid DOI metadata") from exc

	publication = record.get("published-print") or record.get("published-online") or record.get("created", {})
	date_parts = publication.get("date-parts", [[]])
	year = date_parts[0][0] if date_parts and date_parts[0] else None
	authors = [
		" ".join(value for value in (person.get("given"), person.get("family")) if value)
		for person in record.get("author", [])
	]
	# Return a Citation object with the normalized metadata
	return Citation(
		authors=authors,
		title=(record.get("title") or [""])[0],
		journal=(record.get("container-title") or [""])[0],
		year=year,
		volume=record.get("volume"),
		issue=record.get("issue"),
		pages=record.get("page") or record.get("article-number"),
		doi=record.get("DOI", normalized_doi),
		url=record.get("URL"),
	)

if __name__ == "__main__":
    # Example usage: python src/MY_TEST_FEATURE.py 10.1038/s41586-020-2649-2
    test1 = import_doi_reference("10.1038/s41586-020-2649-2")

    # print nicely formatted citation
    print(f"{', '.join(test1.authors)}. {test1.title}. {test1.journal} {test1.year};{test1.volume}({test1.issue}):{test1.pages}. doi:{test1.doi}. URL: {test1.url}")
    
    test2 = import_doi_reference("https://doi.org/10.1016/j.jmatprotec.2006.03.052")
    print(f"{', '.join(test2.authors)}. {test2.title}. {test2.journal} {test2.year};{test2.volume}({test2.issue}):{test2.pages}. doi:{test2.doi}. URL: {test2.url}")