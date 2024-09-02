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
    GitHub Repository:  https://github.com/StanislawHornaGitHub/GitHub_Statistics
    Creation Date:      18-Feb-2024
    ChangeLog:

    Date            Who                     What
    2024-02-20      Stanisław Horna         Basic logs implemented
    2024-03-03      Stanisław Horna         Language name translation implemented.
    
"""
from Dependencies.Class_Log import Log
import json

def calculateLanguageUsage(config: dict, repositoryDetailedList: list[dict[str, str | dict]], Logger: Log) -> dict[str, int | dict[str, int]]:
    
    Logger.writeLog("info","calculateLanguageUsage started")
    
    # init dict for languages, sum variable extract languages to exclude from calculation
    languages = {}
    overallSum = 0
    excludedLangs = config["LANGUAGES_TO_BE_SKIPPED"]
    Logger.writeLog("info",f"excluded languages: {', '.join(excludedLangs)}")
    
    # loop through each repository
    for repo in repositoryDetailedList:

        # loop through each language in current repository
        for currentLang in repo["Languages"]:
            
            # Check if mapping for current language is defined,
            # if not use the default name
            if currentLang in config["LANGUAGE_NAME_MAP"]:
                langToDisplay = config["LANGUAGE_NAME_MAP"][currentLang]
            else:
                langToDisplay = currentLang
                
            # skip iteration if current language is excluded
            if currentLang in excludedLangs or langToDisplay in excludedLangs:
                continue
                
            # cast current value to int
            currentValue = int(repo["Languages"][currentLang])
            
            # sum current value with overall sum
            overallSum += currentValue
            
            # if currently processing language exists in languages dict,
            # sum existing value with currently processing one,
            # otherwise create new entry for not existing lang so far and assign value
            if langToDisplay in languages:
                languages[langToDisplay] += currentValue
            else:
                languages[langToDisplay] = currentValue
    
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

def checkIfPlotUpdateIsRequired(NewStatsPath: str, OldStatsPath: str, Logger: Log) -> bool:
    
    Logger.writeLog("info", "Loading Lang stats files")
    
    # try to read newly calculated lang stats,
    # if it is impossible it may indicate that something went wrong in previous steps,
    # so raise an Exception
    try:
        with open(NewStatsPath, "r") as newStatsFile:
            new = json.loads("\n".join(list(newStatsFile.readlines())))
    except:
        Logger.writeLog("error", "Failed to load new Lang stats file is corrupted")
        raise Exception("New Lang stats file is corrupted")
    
    # try to read old lang stats downloaded from repository to update,
    # if it is impossible it may not exist or be corrupted,
    # in such case return True, as plot update is required
    try:
        with open(OldStatsPath, "r") as oldStatsFile:
            old = json.loads("\n".join(list(oldStatsFile.readlines())))
    except:
        Logger.writeLog("error", "Failed to load old Lang stats. file is corrupted or does not exist")
        Logger.writeLog("info", "Plot update is required")
        return True
    
    # loop through all languages in new data set
    for language in new:
        
        # check if current lang exist in old set, if not return True, as update is required
        if language in list(old.keys()):
            
            # if values are different between sets, stats has been changed and update is required 
            if new[language] != old[language]:
                Logger.writeLog("info", f"{language} has different values (new: {new[language]} ; old: {old[language]})")
                Logger.writeLog("info", "Plot update is required")
                return True
            
        # if language does not exist in old set, stats has been changed and update is required 
        else:
            return True
    
    # loop through all languages in old data set
    for language in old:
        
        # check if current lang exist in new set, if not return True, as update is required
        if language in list(new.keys()):
            if old[language] != new[language]:
                Logger.writeLog("info", f"{language} has different values (old: {old[language]} ; new: {new[language]})")
                Logger.writeLog("info", "Plot update is required")
                return True
            
        # if language does not exist in new set, stats has been changed and update is required 
        else:
            return True
    
    Logger.writeLog("info", "Plot update is not required")
    
    # if no condition to return this function was met before it means that nothing changed,
    # as a result it is not required to updated the plots
    return False
