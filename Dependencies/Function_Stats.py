"""
.DESCRIPTION
    Module of functions to perform calculation on retrieved stats data
        
    calculateLanguageUsage
        sums values for each language which is not excluded and the overall sum for all repos
        
    calculateLanguagePercentage
        calculates average usage of each language
        
.NOTES

    Version:            1.1
    Author:             Stanisław Horna
    Mail:               stanislawhorna@outlook.com
    GitHub Repository:  https://github.com/StanislawHornaGitHub/Investment_fund_Analyzer
    Creation Date:      18-Feb-2024
    ChangeLog:

    Date            Who                     What
    20-02-2024      Stanisław Horna         Basic logs implemented
"""
from Dependencies.Function_Logs import Log

def calculateLanguageUsage(config: dict, repositoryDetailedList: list[dict[str, str | dict]], Logger: Log) -> dict[str, int | dict[str, int]]:
    Logger.writeLog("info",f"calculateLanguageUsage started")
    # init dict for languages, sum variable extract languages to exclude from calculation
    languages = {}
    overallSum = 0
    excludedLangs = config["LANGUAGES_TO_BE_SKIPPED"]
    Logger.writeLog("info",f"excluded languages: {', '.join(excludedLangs)}")
    # loop through each repository
    for repo in repositoryDetailedList:

        # loop through each language in current repository
        for currentLang in repo["Languages"]:

            
            if currentLang not in excludedLangs:
                
                # cast current value to int
                currentValue = int(repo["Languages"][currentLang])
                # sum current value with overall sum
                overallSum += currentValue
                
                # if currently processing language exists in languages dict,
                # sum existing value with currently processing one,
                # otherwise create new entry for not existing lang so far and assign value
                if currentLang in languages:
                    languages[currentLang] += currentValue
                else:
                    languages[currentLang] = currentValue
    
    Logger.writeLog("info",f"Found languages after exclusion: {', '.join(list(languages.keys()))}")
    # return dict with calculated values
    return {
        "OverallSum": overallSum,
        "Languages": languages
    }

def calculateLanguagePercentage(langUsage: dict[str, int | dict[str, int]], Logger: Log) -> dict[str, int | dict[str, int]]:

    # init dict for new key in langUsage
    langUsage["Percentage"] = {}

    # loop through each language
    # divide current language value by overall sum for all repos,
    # round the result with precision to 4 decimal places
    for lang in langUsage["Languages"]:
        langUsage["Percentage"][lang] = round(
            (langUsage["Languages"][lang] / langUsage["OverallSum"]) , 4)
        Logger.writeLog("info",f"Calculated average for {lang}: {langUsage['Percentage'][lang] * 100}%")
    
    # sort averages in dict where key is lang name and value is its average
    langUsage["Percentage"] = dict(sorted(langUsage["Percentage"].items(), key=lambda item: item[1]))
    Logger.writeLog("info","Percentage output sorted")
    # return calculated data
    return langUsage
