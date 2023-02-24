import os
from logging import getLogger

import requests

logger = getLogger(__name__)


class SWAPI:
    def __init__(self, api_url=""):
        self.api_url: str = self._resolve_api_url(api_url)
        self._health_check()

    def _resolve_api_url(self, api_url) -> str:
        url = api_url or os.getenv("SWAPI_API_URL", None)
        if url is None:
            raise ValueError(
                "API url not provided nor env variable 'SWAPI_API_URL' not set"
            )
        if not url.endswith(r"/") and not url.startswith((r"https://", r"http://")):
            raise ValueError("API url is not correctly formatted")
        return url

    def update_data(self):
        ...

    def _health_check(self) -> None:
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
        while _next:
            response = requests.get(url).json()
            result.extend(response["results"])
            if (next_url := response.get("next")) is not None:
                url = next_url
            else:
                _next = False
        return result

    def _get_people(self) -> list:
        return self._get_data("people/")

    def _get_planets(self):
        return self._get_data("planets/")

    def resolve_planets(self):
        ...
