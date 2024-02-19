import requests
import base64
import json


global GITHUB_API_LIST_REPOS
global GITHUB_API_LANG_STATS
global REPOS_PER_PAGE
global pageCounter

GITHUB_API_LIST_REPOS = "https://api.github.com/user/repos?per_page=NUMBER_OF_REPOS_PER_PAGE_TO_BE_REPLACED&page=PAGE_NUMBER_TO_BE_REPLACED&type=owner"
GITHUB_API_LANG_STATS = "https://api.github.com/repos/REPOSITORY_FULL_NAME_TO_BE_REPLACED/languages"
REPOS_PER_PAGE = 100
pageCounter = 1


def getRepositoryList(config: dict) -> list[dict[str, str | dict]]:
    readEncodedAccessToken(config)
    result = []
    while (response := downloadRepoListPage()) != None:
        for repo in response:
            result.append({
                'full_name': repo["full_name"],
                'name': repo["name"],
                'created_at': repo["created_at"],
                'updated_at': repo["updated_at"],
                'pushed_at': repo["pushed_at"],
                'Languages': {}
            })
    return result


def downloadRepoListPage():
    global pageCounter

    response = requests.get(url=prepareListURLtoRequest(),
                            headers=getHeaders()).content
    pageCounter += 1
    result = json.loads(response)
    if len(result) > 0:
        return result
    return None


def getRepositoryLanguageStats(repoList: list[dict[str, any]]) -> list[dict[str, str | dict]]:
    for repo in repoList:
        repo["Languages"] = downloadRepoLangStats(repo["full_name"])

    return repoList


def downloadRepoLangStats(repoFullname: str):
    requestURL = (GITHUB_API_LANG_STATS
                  .replace("REPOSITORY_FULL_NAME_TO_BE_REPLACED", repoFullname)
                  )
    response = requests.get(url=requestURL, headers=getHeaders()).content
    return json.loads(response)


def prepareListURLtoRequest() -> str:
    return (GITHUB_API_LIST_REPOS
            .replace("PAGE_NUMBER_TO_BE_REPLACED", f"{pageCounter}")
            .replace("NUMBER_OF_REPOS_PER_PAGE_TO_BE_REPLACED", f"{REPOS_PER_PAGE}")
            )


def readEncodedAccessToken(config: dict):
    global encodedToken
    encodedToken = config["GITHUB_TOKEN"]


def getHeaders() -> dict[str, str]:
    return {"Authorization": f'Bearer {base64.b64decode(encodedToken).decode("utf-8")}'}
