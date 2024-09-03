import os
import requests
import src.API as API
import src.Models as Model


class GitHub:

    __list_repos: str = "/user/repos"
    __repo_lang: str = "/repos/{full_name}/languages"
    __per_page: int = 100

    @staticmethod
    def get_repo_list(page_num: int = 1) -> list[Model.Repo]:
        result: list[Model.Repo] = []

        response = API.Github.get(
            path=GitHub.__list_repos,
            params={
                "per_page": GitHub.__per_page,
                "page": page_num,
                "type": "collaborator"
            }
        )

        for item in response:
            result.append(
                Model.Repo(
                    **item
                )
            )

        if response:
            result = result + GitHub.get_repo_list(page_num+1)

        return result
    
    @staticmethod
    def get_repo_language(repo_full_name: str):
        response = API.Github.get(
            path=GitHub.__repo_lang.format(
                full_name=repo_full_name
            )
        )
        return response

