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

    Version:            1.0
    Author:             Stanisław Horna
    Mail:               stanislawhorna@outlook.com
    GitHub Repository:  https://github.com/StanislawHornaGitHub/Investment_fund_Analyzer
    Creation Date:      18-Feb-2024
    ChangeLog:

    Date            Who                     What

"""
import json
import os

global FundsToCheckURLsKey
global InvestmentsFilePathKey
global configFilePath

FundsToCheckURLsKey = "FundsToCheckURLs"


configFilePath = "Config.json"

def getConfiguration():
    
    checkIfConfigFileExists()
    with open(configFilePath,"r") as configFile:
        configuration = json.loads("\n".join(configFile.readlines()))
    
    createFolderIfNotExists(configuration["PLOTS_DIR_NAME"])

    return configuration

def checkIfConfigFileExists():
    if not os.path.isfile(configFilePath):
        raise Exception("Config file does not exist")

def createFolderIfNotExists(folderPath):    
    if not os.path.exists(folderPath):
        try:
            os.makedirs(folderPath)
        except:
            raise Exception("Cannot create output folder")

def setCorrectPath():
    file_path = os.path.realpath(__file__)
    file_path = "/".join(file_path.split("/")[:-2])
    os.chdir(file_path)