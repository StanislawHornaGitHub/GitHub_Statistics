<#
.SYNOPSIS
    Script to generate Language statistics for GitHub user authenticated with provided token and 
    update the .md file with the results in selected repository
        (it can be different than the one where the script is located)

.DESCRIPTION
    Script will collect from the user the auth token from user and will use it to collect the data from GitHub API.
    Token will be also saved to file for future use.
    Script connects to the GitHub API and collects list of all repositories for the authenticated user.
    For each repository it will call the API to collect the data regarding the language used.
    After that it will calculate percentage of each language used and will save the data to the file.

.INPUTS
    SCRIPT INPUTS
        - AccessToken - token to be used to authenticate with GitHub API
        - ReturnResultVariable - switch to return the result as a variable
        - AlwaysCreateNewPlot - switch to create new plot file, independently if stats changed or not
            Creating new plot will also trigger readme update

    SCRIPT VARIABLES
        - GITHUB_TOKEN_FILE_PATH - path to the file where the token will be saved
        - LIST_REPOS_URL - url to the GitHub API to collect the list of repositories
        - STRING_TO_BE_REPLACED_LIST_REPOS - string to be replaced in LIST_REPOS_URL
        - REPO_STATS_PAGE_COUNTER - counter for the page number to be used in LIST_REPOS_URL
        - REPOS_LANG_STATS_URL - url to the GitHub API to collect the data regarding the language used
        - STRING_TO_BE_REPLACED_LANG_STATS - string to be replaced in REPOS_LANG_STATS_URL
        - PLOT_FILE_PATH - path to the file where the data will be saved
        - PLOT_WIDTH - width of the plot
        - PLOT_TITLE - title of the plot
        - LANGUAGES_TO_BE_SKIPPED - list of languages to be skipped

.OUTPUTS
    Markdown file - the plot with the data regarding the language used.
    Result variable - if ReturnResultVariable switch is used.

.NOTES

    Version:            1.1
    Author:             Stanisław Horna
    Mail:               stanislawhorna@outlook.com
    GitHub Repository:  https://github.com/StanislawHornaGitHub/GitHub_Statistics
    Creation Date:      17-Jan-2024
    ChangeLog:

    Date            Who                     What
    18-01-2024      Stanislaw Horna         Verification if stats changed since last execution.
                                            Update README.md file in separate repo implemented.
    19-01-2024      Stanislaw Horna         DoNotMakePush parameter implemented, to generate plot,
                                            without pushing it to the repository.
#>

param(
    [string]$AccessToken,
    [switch]$ReturnResultVariable,
    [switch]$AlwaysCreateNewPlot,
    [switch]$DoNotMakePush
)

New-Variable -Name 'README_FILE_PATH' -Value "./README.md" -Scope Script -Force -Option ReadOnly
New-Variable -Name 'REPO_URL_TO_UPDATE' -Value "https://github.com/StanislawHornaGitHub/Test_profile_repo" -Scope Script -Force -Option ReadOnly
New-Variable -Name 'COMMIT_MESSASGE' -Value "AutoUpdate Top Used Languages" -Scope Script -Force -Option ReadOnly
New-Variable -Name 'REPO_DIRECTORY' -Value "./TEST" -Scope Script -Force -Option ReadOnly
New-Variable -Name 'GITHUB_TOKEN_FILE_PATH' -Value "./Token.txt" -Scope Script -Force -Option ReadOnly
New-Variable -Name 'LIST_REPOS_URL' -Value "https://api.github.com/user/repos?per_page=100&page=PAGE_NUMBER_TO_BE_REPLACED&type=owner" -Scope Script -Force
New-Variable -Name 'STRING_TO_BE_REPLACED_LIST_REPOS' -Value "PAGE_NUMBER_TO_BE_REPLACED" -Scope Script -Force -Option ReadOnly
New-Variable -Name 'REPO_STATS_PAGE_COUNTER' -Value 1 -Scope Script -Force
New-Variable -Name 'REPOS_LANG_STATS_URL' -Value "https://api.github.com/repos/REPOSITORY_FULL_NAME_TO_BE_REPLACED/languages" -Scope Script -Force
New-Variable -Name 'STRING_TO_BE_REPLACED_LANG_STATS' -Value "REPOSITORY_FULL_NAME_TO_BE_REPLACED" -Scope Script -Force -Option ReadOnly
New-Variable -Name 'PLOT_FILE_PATH' -Value "./plot.md" -Scope Script -Force -Option ReadOnly
New-Variable -Name 'PLOT_WIDTH' -Value 100 -Scope Script -Force -Option ReadOnly
New-Variable -Name 'PLOT_TITLE' -Value "Top Used Languages (including private repositories)" -Scope Script -Force -Option ReadOnly
New-Variable -Name 'PLOT_UPDATE_REQUIRED' -Value $true -Scope Script -Force
New-Variable -Name 'LANGUAGE_TEMP_FILE_PATH' -Value "./LanguageStats.json" -Scope Script -Force -Option ReadOnly
New-Variable -Name 'LANGUAGES_TO_BE_SKIPPED' -Value @{
    "HTML"       = ""
    "CSS"        = ""
    "C#"         = ""
    "CMake"      = ""
    "JavaScript" = ""
    "Assembly"   = ""
} -Scope Script -Force -Option ReadOnly
New-Variable -Name 'RESULT' -Value @{
    "Repositories"      = @{}
    "Languages"         = @{}
    "OverallSum"        = 0
    "PercentageSummary" = @{}
} -Scope Script -Force

Function Invoke-main {
    try {
        Get-AccessToken
        Invoke-DataCollection
        Get-LanguageDetails
        Invoke-LanguageStatsCalculation
        Invoke-ComparisonCurrentValuesWithPrevious
        Invoke-PercentageCalculation
        Convert-PercentageSummary
        New-BarChartForMarkDown
        Export-LanguageStats
        Invoke-RepositoryClone
        Update-READMEfile
        Invoke-CommitAndPush
    }
    catch {
        Write-Error $_
    }
    if ($ReturnResultVariable) {
        return $RESULT
    }
}

function Get-AccessToken {
    # Check if GitHub token file exists
    # If not, ask for GitHub token and save it to file
    if (-not $(Test-Path $GITHUB_TOKEN_FILE_PATH)) {
        # If AccessToken is not provided, ask for it,
        # if AccessToken is provided, use it
        if ([string]::IsNullOrEmpty($AccessToken)) {
            $token = Read-Host -Prompt "Enter your GitHub Personal Access Token"
        }
        else {
            $token = $AccessToken
        }
        # Save GitHub token to file
        $token | Out-File -FilePath $GITHUB_TOKEN_FILE_PATH -Force
    }
    # Read GitHub token from file
    New-Variable -Name 'GITHUB_TOKEN' -Value $(Get-Content $GITHUB_TOKEN_FILE_PATH) -Scope Script -Force -Option ReadOnly    
}

function Invoke-DataCollection {
    # Get list of repositories
    $RepositoryList = Get-ListOfGitHubRepos
    # Each Get-ListOfGitHubRepos call returns 100 repos on current page, next call will return next page of repos
    # Loop until all repos are collected, if returned page is empty, function will return null, which will break the loop
    while ($null -ne $RepositoryList) {
        # Loop through each repo in current page
        foreach ($repo in $RepositoryList) {
            # Add repo to RESULT hash table
            $RESULT.Repositories.Add($repo.name, @{
                    'full_name'  = $repo.full_name
                    'name'       = $repo.name
                    'created_at' = $repo.created_at
                    'updated_at' = $repo.updated_at
                    'pushed_at'  = $repo.pushed_at 
                    'Languages'  = @{}
                })
        }
        # Collect repos from next page before next iteration
        $RepositoryList = Get-ListOfGitHubRepos
    }
}

function Get-LanguageDetails {
    # Create headers for GitHub API call
    $headers = @{
        Authorization = "Bearer $GITHUB_TOKEN"
    }
    # Loop through each repo in RESULT hash table
    foreach ($repo in $RESULT.Repositories.Keys) {
        try {
            # Get URL for GitHub API call regarding current repo
            $URL = $REPOS_LANG_STATS_URL.Replace($STRING_TO_BE_REPLACED_LANG_STATS, $($RESULT.Repositories.$repo.full_name))
        }
        catch {
            throw "Unable to get langauage stats for repo $repo"
        }
        # Invoke GitHub API call
        $LanguageDetails = Invoke-RestMethod -Method Get -Uri $URL -Headers $headers
        # Save formated response in RESULT hash table
        $RESULT.Repositories.$repo.Languages = $LanguageDetails
    }
}

function Invoke-LanguageStatsCalculation {
    # Loop through each repo in RESULT hash table
    foreach ($repo in $RESULT.Repositories.Keys) {
        # Get LanguageStats for current repo
        $LanguageStats = $RESULT.Repositories.$repo.Languages
        # Loop through each language in LanguageStats
        # Each language is represented as Note property in LanguageStats, so Get-Member is required
        foreach ($lang in $($LanguageStats | Get-Member -MemberType NoteProperty).Name) {
            # Skip languages that are in LANGUAGES_TO_BE_SKIPPED
            # LANGUAGES_TO_BE_SKIPPED is a hashtable, because it is faster to check if key exists in hasthable,
            # than using array and "-in" operator
            if ($LANGUAGES_TO_BE_SKIPPED.ContainsKey($lang)) {
                continue
            }
            # Check if currnet language already exists in summary key of hash table
            if ($RESULT.Languages.ContainsKey($lang)) {
                # If it exists, add current language's stats to existing language's stats
                $RESULT.Languages.$lang += $LanguageStats.$lang
            }
            else {
                # If it does not exist, add current language's stats to summary key of hash table
                $RESULT.Languages.Add($lang, $LanguageStats.$lang)
            }
            # Add current language's stats to overall sum
            $RESULT.OverallSum += $LanguageStats.$lang
        }
    }
    
}

function Invoke-ComparisonCurrentValuesWithPrevious {
    # Skip verification if AlwaysCreateNewPlot is set to true
    if ($AlwaysCreateNewPlot) {
        return
    }
    # Check if previous summary file exists
    if (-not $(Test-Path -Path $LANGUAGE_TEMP_FILE_PATH)) {
        return
    }
    # Read previous summary file
    $OldLangSummary = Get-Content -Path $LANGUAGE_TEMP_FILE_PATH | ConvertFrom-Json -Depth 3
    # Check if number of languages did not change
    if ($($OldLangSummary.Languages | Get-Member -MemberType NoteProperty).count -ne $($RESULT.Languages.Keys.Count)) {
        return
    }
    # Check if overall sum did not change
    if ($OldLangSummary.OverallSum -ne $RESULT.OverallSum ) {
        return
    }
    # Loop through each language in RESULT hash table
    foreach ($lang in $RESULT.Languages.Keys) {
        # Check if value for particular language did not change
        if ($OldLangSummary.Languages.$lang -ne $RESULT.Languages.$lang) {
            return
        }
    }
    # If all checks passed without exiting, no changes were detected
    # So, no plot update is required
    $Script:PLOT_UPDATE_REQUIRED = $false
    Write-Host "Plot update required: $($Script:PLOT_UPDATE_REQUIRED)"
}

function Convert-PercentageSummary {
    # Create array list, which will allow to sort values
    $Table = New-Object System.Collections.ArrayList
    # Loop through each language in RESULT hash table and add it to array list
    foreach ($lang in $RESULT.PercentageSummary.Keys) {
        $null = $Table.Add([PSCustomObject]@{
                "language"   = $lang
                "percentage" = $RESULT.PercentageSummary.$lang
            })
    }
    # Calculate sum of all percentages values, to correct inaccuracy of [math]::Round method
    $sum = 0
    $Table | ForEach-Object { $sum += $_.percentage }
    $Table = $Table | Sort-Object -Property percentage -Descending
    # Correct inaccuracy of [math]::Round method by substracing the differance from the highest value
    $Table[0].percentage = $Table[0].percentage - ($sum - 100)
    # Assing array list to RESULT hash table
    $RESULT.PercentageSummary = $Table
}

function Invoke-PercentageCalculation {
    # Loop through each language in RESULT hash table
    foreach ($lang in $RESULT.Languages.Keys) {
        # Add current language's percentage to hash table
        $RESULT.PercentageSummary.Add($lang, [math]::Round((($RESULT.Languages.$lang / $RESULT.OverallSum) * 100), 2))
    }
}

function New-BarChartForMarkDown {
    param(
        $plotFilePath = $PLOT_FILE_PATH,
        $PlotWidth = $PLOT_WIDTH
    )
    # Create local variable to simplify code
    $ValTable = $RESULT.PercentageSummary
    # Create new column to output to create legend for barchart
    $ValTable | Add-Member -name 'String_to_chart' -value "" -MemberType NoteProperty
    # Create initial string form and allign it based on number of digits in percentage
    $ValTable | ForEach-Object {
        $AdditionalSpace = ""
        if (([float]$_.percentage) -lt 10) {
            $AdditionalSpace = " "
        }
        $_.String_to_chart = " $($_.language) ($AdditionalSpace $(([float]$_.percentage).ToString("0.00"))% )"
    }
    # Get length of longest string
    $maxLength = $ValTable.String_to_chart | ForEach-Object { $_.Length } | Sort-Object -Descending | Select-Object -First 1
    # Based on the longest string, add spaces to each string in ValTable to allign them to right
    $ValTable | ForEach-Object {
        $requiredSpaces = $maxLength - $_.String_to_chart.Length
        $_.String_to_chart = (" " * $requiredSpaces) + $_.String_to_chart
    }
    # Create array list to store lines of plot
    [System.Collections.ArrayList]$plotMatrix = @()
    # Loop through each row in ValTable and create line of plot
    for ($row = 0; $row -lt $ValTable.Count; $row++) {
        # Add appropriate number of "#" to line of plot that is corresponding with current language's percentage
        $line = $ValTable[$row].String_to_chart + " | " + ("#" * [math]::Round(($PlotWidth / 100) * ($ValTable[$row].percentage), 0))
        # Add line of plot to array list
        $null = $plotMatrix.Add($line)
    }
    # Write plot title to file
    "## $PLOT_TITLE" | Out-File -FilePath $plotFilePath
    # Write plot to file, adding tab sign at the begginig of each line to make it look like code in markdown
    $plotMatrix | ForEach-Object { "`t$($_)" } | Out-File -FilePath $plotFilePath -Append
    
}

function Export-LanguageStats {
    @{
        Languages  = $($RESULT.Languages)
        OverallSum = $($RESULT.OverallSum)
    } | ConvertTo-Json -Depth 3 | Out-File -FilePath $LANGUAGE_TEMP_FILE_PATH -Force
}

function Update-READMEfile {
    # Skip execution if Plot Update is not required or DoNotMakePush script input is set to true
    if ((-not $PLOT_UPDATE_REQUIRED) -or $DoNotMakePush) {
        return
    }
    # Create temp file of README
    $TempFilePath = "$($README_FILE_PATH).tmp"
    Copy-Item -Path "$README_FILE_PATH" -Destination "$TempFilePath" -Force
    # Read README file line by line
    $titleFound = $false
    Get-Content $TempFilePath | ForEach-Object {
        # If Plot title found, then set variable to skip passing to pipe-out next file lines
        if ($_ -like "*$PLOT_TITLE*") { 
            $titleFound = $true        
        }
        if ($titleFound -eq $false) {
            $_
        }
    } | Out-File -FilePath $README_FILE_PATH  
    # Remove temp file
    Remove-Item -Path $TempFilePath -Force     
    # # Add plot to README file
    Get-Content -Path $PLOT_FILE_PATH | Out-File -FilePath $README_FILE_PATH -Append   
}

function Invoke-RepositoryClone {
    # Skip execution if Plot Update is not required or DoNotMakePush script input is set to true
    if ((-not $PLOT_UPDATE_REQUIRED) -or $DoNotMakePush) {
        return
    }
    # Clone git repository to update using GitHub token
    git clone $($REPO_URL_TO_UPDATE.Replace("https://", "https://oauth2:$GITHUB_TOKEN@")) $REPO_DIRECTORY -q
    # Copy Plot file to Repository directory
    Copy-Item -Path $PLOT_FILE_PATH -Destination "$REPO_DIRECTORY/$((Get-ChildItem -Path $PLOT_FILE_PATH).name)"
    # Change directory to repository directory
    Set-Location $REPO_DIRECTORY
}

function Invoke-CommitAndPush {
    # Skip execution if Plot Update is not required or DoNotMakePush script input is set to true
    if ((-not $PLOT_UPDATE_REQUIRED) -or $DoNotMakePush) {
        return
    }
    # Remove plot file from repository directory
    Remove-Item -Path $PLOT_FILE_PATH -Force
    # Add README file to stage
    git add $README_FILE_PATH
    # Commit changes
    git commit -m "$COMMIT_MESSASGE" -q
    # Push changes to GitHub
    git push -q
    # Change directory back to parent directory
    Set-Location ..
    # Remove repository directory
    Remove-Item -Path $REPO_DIRECTORY -Recurse -Force
}

function Get-ListOfGitHubRepos {
    # Create headers for GitHub API call
    $headers = @{
        Authorization = "Bearer $GITHUB_TOKEN"
    }
    # Replace string in URL with page counter
    $URL = $LIST_REPOS_URL.Replace($STRING_TO_BE_REPLACED_LIST_REPOS, $REPO_STATS_PAGE_COUNTER)
    try {
        # Call GitHub API to get list of repositories
        $RepoList = Invoke-RestMethod -Method Get -Uri $URL -Headers $headers -ErrorAction Stop
    }
    catch {
        throw "Unable to get list of repositories. Error: $_"
    }
    # Increment page counter
    $Script:REPO_STATS_PAGE_COUNTER++
    # Return list of repositories if there are any, otherwise return null
    If ($RepoList.count -gt 0) {
        return $RepoList
    }
    else {
        return $null
    }
}

Invoke-main