import json

global LANGUAGE_CACHE_FILE

LANGUAGE_CACHE_FILE = "LanguageStatsCache.json" 

def calculateLanguageUsage(config: dict, repositoryDetailedList: list[dict[str, str | dict]]) -> dict[str, int | dict[str, int]]:
    languages = {}
    overallSum = 0
    excludedLangs = config["LANGUAGES_TO_BE_SKIPPED"]
    for repo in repositoryDetailedList:

        for currentLang in repo["Languages"]:

            if currentLang not in excludedLangs:
                currentValue = int(repo["Languages"][currentLang])

                overallSum += currentValue
                if currentLang in languages:
                    languages[currentLang] += currentValue
                else:
                    languages[currentLang] = currentValue
    return {
        "OverallSum": overallSum,
        "Languages": languages
    }

def calculateLanguagePercentage(langUsage: dict[str, int | dict[str, int]]) -> dict[str, int | dict[str, int]]:

    langUsage["Percentage"] = {}

    for lang in langUsage["Languages"]:
        langUsage["Percentage"][lang] = round(
            (langUsage["Languages"][lang] / langUsage["OverallSum"]) , 4)
        
    langUsage["Percentage"] = dict(sorted(langUsage["Percentage"].items(), key=lambda item: item[1]))
    return langUsage
