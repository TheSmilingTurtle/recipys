from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from bs4 import BeautifulSoup
import requests


ERROR_MESSAGE: Dict[str, List[str]] = {
    "ERROR": [
        (
            "HTTP request error. "
            "Please check your internet connection and try again"
        )
    ]
}


@dataclass
class HtmlSearchTarget:
    """Search target for HTML elements and their values"""

    name: str
    search_element_named: str
    search_element_with_value: str
    target_element: Optional[str] = None  # If none, inner HTML is returned


@dataclass
class ScraperSearchTerms:
    """Search terms for scraper within HTML page"""

    target: HtmlSearchTarget
    return_multiple: bool = False  # If False, only first match is returned


@dataclass
class Scraper:
    """Scrapes content from website"""

    url: str
    search_terms: List[ScraperSearchTerms]
    # _http_response: Optional[requests.Response] = None

    def get(self) -> Dict[str, List[str]]:
        """Return found data as requested by search parameters"""
        self._http_response = requests.get(self.url)

        try:
            self._check_http_response_status()
        except ConnectionRefusedError:
            return ERROR_MESSAGE

        self._html = self._http_response.text
        return self._parse()

    def _check_http_response_status(self) -> None:
        """Check response of http GET request
        - Raises: ConnectionRefusedError if request's status is invalid"""
        try:
            self._http_response.raise_for_status()
        except requests.exceptions.HTTPError:
            raise ConnectionRefusedError

    def _parse(self) -> Dict[str, List[str]]:
        """Return Dict with findings in HTML file according to search terms"""
        parsed_results: Dict[str, List[str]] = {}

        soup = BeautifulSoup(self._html, "html.parser")

        for search in self.search_terms:
            results: List[str] = []
            limit_hits: int = 20 if search.return_multiple else 1

            tags = soup.find_all(
                attrs={
                    search.target.search_element_named,
                    search.target.search_element_with_value,
                },
                limit=limit_hits,
            )

            for tag in tags:
                if search.target.target_element:
                    # Specific tag of element is searched
                    att_value = tag.attrs.get(search.target.target_element, None)
                    if att_value:
                        results.append(att_value)
                else:
                    # Inner HTML is searched
                    results.append(tag.text)

            parsed_results.setdefault(search.target.name, results)

        return parsed_results
