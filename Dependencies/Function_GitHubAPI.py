"""
.DESCRIPTION
    Module of:
            - constant values required to correctly request the data
            - functions related to downloading statistical data using GitHub API
            
    getRepositoryList
        gets list of repositories repositories available for the user authenticated with provided token
        Inputs:
            - config <- configuration dict to get the GitHub Access Token

    downloadRepoListPage
        downloads next page of repository list
        
    getRepositoryLanguageStats
        gets the Languages Used stats for repositories passed as argument.
        Inputs:
            - repoList <- dict of repositories collected using getRepositoryList
            
    downloadRepoLangStats
        downloads repository used languages statistical information for repository full name passed as argument
        Inputs:
            - repoFullname <- string with full name of the repository
            
    prepareListURLtoRequest
        gets valid URL to request the repository list page
        
    readEncodedAccessToken
        reads and decodes GitHub access token form configuration dict variable
        
    getHeaders
        creates headers for each web request to GitHub API

.NOTES

    Version:            1.0
    Author:             Stanisław Horna
    Mail:               stanislawhorna@outlook.com
    GitHub Repository:  https://github.com/StanislawHornaGitHub/GitHub_Statistics
    Creation Date:      19-Feb-2024
    ChangeLog:

    Date            Who                     What

"""
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
    # store Token as module global variable
    readEncodedAccessToken(config)
    # init result list
    result = []
    # Loop until downloadRepoListPage result is not none
    while (response := downloadRepoListPage()) != None:
        # for each repository in the received page create an entry in the output list
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
    
    # create a request to GitHub API and extract the content from response
    try:
        response = requests.get(url=prepareListURLtoRequest(),
                                headers=getHeaders()).content
        # increment page counter for next request
        pageCounter += 1
    except:
        return None
    
    # read JSON structure from response
    result = json.loads(response)
    # if there is any data in response return it
    if len(result) > 0:
        return result
    return None


def getRepositoryLanguageStats(repoList: list[dict[str, any]]) -> list[dict[str, str | dict]]:
    # Loop through each repository in the list and download Language stats
    for repo in repoList:
        repo["Languages"] = downloadRepoLangStats(repo["full_name"])

    return repoList


def downloadRepoLangStats(repoFullname: str):
    # prepare URL to request by encoding the full name into the URL 
    requestURL = (GITHUB_API_LANG_STATS
                  .replace("REPOSITORY_FULL_NAME_TO_BE_REPLACED", repoFullname)
                  )
    # create a request to GitHub API and extract the content from response 
    response = requests.get(url=requestURL, headers=getHeaders()).content
    # return read JSON structure from response
    return json.loads(response)


def prepareListURLtoRequest() -> str:
    # encode page number and number repositories per page to the default URL
    return (GITHUB_API_LIST_REPOS
            .replace("PAGE_NUMBER_TO_BE_REPLACED", f"{pageCounter}")
            .replace("NUMBER_OF_REPOS_PER_PAGE_TO_BE_REPLACED", f"{REPOS_PER_PAGE}")
            )


def readEncodedAccessToken(config: dict):
    # Save encoded token from config as global module variable
    global encodedToken
    encodedToken = config["GITHUB_TOKEN"]


def getHeaders() -> dict[str, str]:
    # decode GitHub access token
    # return dict representing required headers
    return {"Authorization": f'Bearer {base64.b64decode(encodedToken).decode("utf-8")}'}