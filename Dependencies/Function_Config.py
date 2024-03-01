"""
.DESCRIPTION
    Module of functions to read out configuration from file
        
    getConfiguration
        reads configuration from JSON file
        
    checkIfConfigFileExists
        checks if config file exists
        
    createFolderIfNotExists
        creates folder if it does not exist
    
    setCorrectPath
        sets correct path to be able to operate on relative paths related to localization of main file
    
.NOTES

    Version:            1.1
    Author:             Stanisław Horna
    Mail:               stanislawhorna@outlook.com
    GitHub Repository:  https://github.com/StanislawHornaGitHub/GitHub_Statistics
    Creation Date:      18-Feb-2024
    ChangeLog:

    Date            Who                     What
    2024-03-01      Stanisław Horna         Handling to overwrite existing Access Token or ask user for a one,
                                            if it does not exist.
                                            Logging implemented. Operations on files to absolute paths
    
"""
import json
import os
import base64
from Dependencies.Class_Log import Log


def getConfiguration(options, Logger: Log, configFilePath: str = "Config.json") -> dict[str, str | int]:

    checkIfConfigFileExists(configFilePath, Logger)
    
    # try to read config file
    try:
        with open(configFilePath, "r") as configFile:
            configuration = json.loads("\n".join(configFile.readlines()))
        Logger.writeLog("info", "Config file loaded successfully")
    except:
        Logger.writeLog("error", "Can not load config file")
        raise Exception("Can not load config file")

    # check if access token was provided as script arg
    # if yes override existing token 
    if options.Access_Token != None:
        Logger.writeLog("info", "Access token provided as script arg")
        accessToken = options.Access_Token
        
        # append config variable with encoded token
        configuration['GITHUB_TOKEN'] = base64.b64encode(
            accessToken.encode("utf-8")
        ).decode("utf-8")
        Logger.writeLog("info", "Access token encoded")

    # check if access token exists in config variable
    # if not ask user to provide tokens
    if "GITHUB_TOKEN" not in list(configuration.keys()):
        Logger.writeLog("info", "Asking user to provide Access token")
        accessToken = input("Provide GitHub Access Token: ")
        
        # append config variable with encoded token
        configuration['GITHUB_TOKEN'] = base64.b64encode(
            accessToken.encode("utf-8")
        ).decode("utf-8")
        Logger.writeLog("info", "Access token encoded")

    # try to save updated config var
    try:
        with open(configFilePath, "w") as configFile:
            configFile.writelines(
                json.dumps(configuration, indent=4)
            )

        Logger.writeLog(
            "info",
            f"Config file successfully saved {configFilePath}"
        )
    except:
        Logger.writeLog("error", "Can not save config file")
        raise Exception("Can not save config file")

    # return config variable
    return configuration


def checkIfConfigFileExists(configFilePath: str, Logger: Log) -> None:
    configFilePath = os.path.join(
        os.getcwd(),
        configFilePath
    )
    Logger.writeLog("info", f"Config file path to check {configFilePath}")
    if not os.path.isfile(configFilePath):
        Logger.writeLog("error", "Config file does not exist")
        raise Exception("Config file does not exist")
    
    return None


def createFolderIfNotExists(folderPath, Logger: Log) -> None:
    folderPath = os.path.join(
        os.getcwd(),
        folderPath
    )
    if not os.path.exists(folderPath):
        Logger.writeLog(
            "info", f"Output directory does not exist ({folderPath})")
        try:
            os.makedirs(folderPath)
            Logger.writeLog("info", f"Output directory created")
        except:
            Logger.writeLog("info", f"Cannot create output directory")
            raise Exception("Cannot create output directory")
        
    return None


def setCorrectPath(Logger: Log) -> None:
    
    # get the absolute path for the main script directory
    file_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
    
    # set working directory to the script's main one
    os.chdir(file_path)
    Logger.writeLog("info", f"Working directory set to {file_path}")
    
    return None
