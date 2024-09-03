import os
import time
import requests


class Github:

    __api_base_url: str = "https://api.github.com"
    __items_per_page: int = 100
    __delay_unit_ms: int = 300
    __retry_timeout_ms: int = 1000

    @staticmethod
    def get(path: str, params: dict = {}, accept: str = "application/vnd.github+json"):
        url: str = Github.__get_url(path)
        headers: dict = Github.__get_headers(accept)

        response = requests.get(
            url=url,
            params=params,
            headers=headers
        )

        counter: int = 1
        while (
            response.status_code not in range(200, 300)
            and response.status_code != 401
            and Github.__delay_unit_ms * counter < Github.__retry_timeout_ms
        ):
            time.sleep((counter * Github.__delay_unit_ms) / 1000)
            response = requests.get(
                url=url,
                params=params,
                headers=headers
            )
            
        return response.json()

    @staticmethod
    def __get_url(path: str):
        return "{base_url}{api_path}".format(
            base_url=Github.__api_base_url,
            api_path=path
        )
    @staticmethod
    def __get_headers(accept: str = "application/vnd.github+json"):
        return {
            "Accept": accept,
            "Authorization": "Bearer {token}".format(token=os.getenv("GH_TOKEN")),
            "X-GitHub-Api-Version": "2022-11-28",
        }
