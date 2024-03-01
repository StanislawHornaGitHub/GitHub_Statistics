# Python Dependencies
All `.py` files defined in this directory are mandatory for `Update_GitHub_Lang_Stats.py`.
They provide all required functionalities, 
when the main file which is being called represents basic logic only

# Brief description

## [Function_BarChart.py](/Dependencies/Function_BarChart.py)
    Module of functions to work with charts.
    
    saveBarChart
        Generates and saves BarChart with transparent background.
        Input params:
            - stats <- dict with statistical information to represent
            - filePath <- path for destination file
            - plotTitle <- title to be displayed in the result file above the chart
            - labelsTextColor <- the color of all labels in the chart
    
    saveBarChartData
        saves raw source data for bar chart as JSON file

## [Function_Config.py](/Dependencies/Function_Config.py)
    Module of functions to read out configuration from file
        
    getConfiguration
        reads configuration from JSON file
        
    checkIfConfigFileExists
        checks if config file exists
        
    createFolderIfNotExists
        creates folder if it does not exist
    
    setCorrectPath
        sets correct path to be able to operate on relative paths related to localization of main file
    
## [Function_GitHubAPI.py](/Dependencies/Function_GitHubAPI.py)
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

## [Function_GitHubRepos.py](/Dependencies/Function_GitHubRepos.py)
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

## [Function_Stats.py](/Dependencies/Function_Stats.py)
    Module of functions to perform calculation on retrieved stats data
        
    calculateLanguageUsage
        sums values for each language which is not excluded and the overall sum for all repos
        
    calculateLanguagePercentage
        calculates average usage of each language