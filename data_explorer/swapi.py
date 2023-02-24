import os
from enum import StrEnum
from logging import getLogger

import requests

logger = getLogger(__name__)


class WrongAPIError(Exception):
    ...


class ENDPOINTS(StrEnum):
    people = "people/"
    planets = "planets/"


class SWAPI:
    def __init__(self, api_url=""):
        self.api_url: str = self._resolve_api_url(api_url)
        self.health_check()

    def _resolve_api_url(self, api_url) -> str:
        url = api_url or os.getenv("SWAPI_API_URL", None)
        if url is None:
            raise WrongAPIError(
                "API url not provided nor env variable 'SWAPI_API_URL' not set"
            )
        if not url.endswith(r"/") and not url.startswith((r"https://", r"http://")):
            raise WrongAPIError("API url is not correctly formatted")
        return url

    def health_check(self) -> None:
        response = requests.get(self.api_url)
        if response.status_code != 200:
            logger.warning(
                f"API response: {response.status_code} - something went wrong"
            )

    def _get_data(self, endpoint):
        # because of limitations in API (10 objects per request)
        # we need to do heck load of requests to get all data
        result: list = []
        _next: bool = True
        url: str = self.api_url + endpoint
        response = requests.get(url)
        while _next:
            response_body = response.json()
            result.extend(response_body["results"])
            if (next_url := response_body.get("next")) is not None:
                url = next_url
                response = requests.get(url)
            else:
                _next = False
        return result, response.headers.get("etag")

    def get_people(self) -> tuple:
        return self._get_data(ENDPOINTS.people)

    def get_planets(self) -> tuple:
        return self._get_data(ENDPOINTS.planets)
