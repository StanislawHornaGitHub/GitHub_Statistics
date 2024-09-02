"""
.DESCRIPTION
    Module of functions to perform basic operations on GitHub repositories
        
    clone
        clones repository to directory passed as an argument using AccessToken
        
    commit
        adds to stage all new files and commits them
        
    push
        pushes all repository changes
        
    copyNewPlotsToRepo
        copiers newly created plots to dir, where repo to update is stored
        
    cleanUpTempFiles
        removes directory recursively
        
.NOTES

    Version:            1.0
    Author:             Stanisław Horna
    Mail:               stanislawhorna@outlook.com
    GitHub Repository:  https://github.com/StanislawHornaGitHub/GitHub_Statistics
    Creation Date:      18-Feb-2024
    ChangeLog:

    Date            Who                     What

"""
import os
import base64
import shutil
from Dependencies.Class_Log import Log

def clone(repoURL: str, destinationDirectory: str, AccessToken: str, Logger: Log) -> None:
    
    # create URL with access token
    repoURLwithToken = repoURL.replace(
        "https://",
        f"https://oauth2:{base64.b64decode(AccessToken).decode('utf-8')}@"
    )
    
    # create absolute path to destination directory
    destinationDirectory = os.path.join(
        os.getcwd(),
        destinationDirectory
    )
    
    # if destination directory exist remove it
    cleanUpTempFiles(destinationDirectory, Logger)
    
    # build command to perform git clone
    commandToCall = f"git clone {repoURLwithToken} '{destinationDirectory}' -q"
    Logger.writeLog("info",f"Cloning repository {repoURL} to {destinationDirectory}")
    
    # call clone command if output is different than 0 it means that command failed, raise an exception
    if os.system(commandToCall) != 0:
        Logger.writeLog("error","Repository clone failed")
        raise Exception("Repository clone failed")
    
    return None

def commit(repoDirectory: str, commitMessage: str, Logger: Log) -> None:
    
    # save current working dir and switch to repository directory
    currentDir = os.getcwd()
    os.chdir(repoDirectory)
    
    Logger.writeLog("info","Adding files to stage")
    # call git command to add change files to stage,
    # if output is different than 0 it means that command failed, raise an exception
    if os.system("git add .") != 0:
        Logger.writeLog("error","Failed to add files to stage")
        os.chdir(currentDir)
        raise Exception("Failed to add files to stage")
    
    Logger.writeLog("info","Committing added files")
    # commit staged files
    # if output is different than 0 it means that command failed, raise an exception
    if os.system(f"git commit -m '{commitMessage}' -q") != 0:
        Logger.writeLog("error","Failed to commit added files")
        os.chdir(currentDir)
        raise Exception("Failed to commit added files")
    
    # set previous working directory
    os.chdir(currentDir)
    return None

def push(repoDirectory: str, Logger: Log) -> None:
    
    # save current working dir and switch to repository directory
    currentDir = os.getcwd()
    os.chdir(repoDirectory)
    
    Logger.writeLog("info","Pushing repository")
    # call git command to push committed files
    # if output is different than 0 it means that command failed, raise an exception
    if os.system("git push -q") != 0:
        Logger.writeLog("error","Failed to push files to repository")
        os.chdir(currentDir)
        raise Exception("Failed to push files to repository")
    
    # set previous working directory
    os.chdir(currentDir)
    
    return None
    
def copyNewPlotsToRepo(sourceDirectory: str, destinationPath, Logger: Log) -> None:
    
    # check if directory for plots already exist in destination repo
    # if yes remove dir
    if os.path.isdir(destinationPath):
        Logger.writeLog("info","Directory for plots in destination repository found")
        shutil.rmtree(destinationPath)
        Logger.writeLog("info","Directory for plots removed from destination repository")
    
    # copy new directory with plots
    shutil.copytree(sourceDirectory,destinationPath)
    Logger.writeLog("info","Directory with newly created plots copied")
    
    return None
    
def cleanUpTempFiles(repoDirectory: str, Logger: Log) -> None:
    
    # check if directory for destination repository exist,
    # if yes remove it
    if os.path.isdir(repoDirectory):
        Logger.writeLog("info","Directory with repository clone found")
        shutil.rmtree(repoDirectory)
        Logger.writeLog("info","Directory with repository clone removed")
        
    return None