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

    FIRST RUN INSTRUCTION
        In order to correctly generate proper Config.json file you need to copy and fill in JSON structure
    presented in INPUTS section. The name must be "Config.json" and it must be located in the same directory as script

    First script run: ./Get-GitHubStats.ps1 -AccessToken "<here_paste_your_GitHub_token>"

    During first script run you can also use other script input params according to your needs.
    It is reccomended to use -DoNotMakePush param to firstly verify if token is granting enough access
        remember that using -DoNotMakePush param will skip clone of REPO_URL_TO_UPDATE


.INPUTS
    SCRIPT INPUTS
        - AccessToken - token to be used to authenticate with GitHub API
        - AlwaysCreateNewPlot - switch to create new plot file, independently if stats changed or not
            Creating new plot will also trigger readme update
        -DoNotMakePush - switch to prevent cloning destination repository and pushing changes in README

    CONFIG FILE (Config.json)
        {
            "README_FILE_PATH":         <README_relative_path_in_repository_to_update>,
            "REPO_URL_TO_UPDATE":       <URL_to_repository_where_readme_meant_to_be_updated>,
            "PNG_LOCATION_IN_REPO"      <location_of_plot_result_directory_for_PNGs>
            "COMMIT_MESSAGE":           <commit_message_in_plot_update>,
            "REPO_DIRECTORY":           <relative_path_to_directory_where_destination_repo_will_be_stored>,
            "PLOTS_DIR_NAME":           <relative_path_to_directory_where_plots_will_be_saved>
            "PLOT_TITLE":               <plot_title>,
            "LANGUAGE_TEMP_FILE_PATH":  <relative_file_path_to_temp_lang_file>,
            "LANGUAGES_TO_BE_SKIPPED": [
                                        <list_of>,
                                        <languages>,
                                        <to_skip>,
                                        <from>,
                                        <plot>
                                        ]
        }


.OUTPUTS

    Commit to the repository set in REPO_URL_TO_UPDATE with updated languages plot

.NOTES

    Version:            3.1
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
    23-01-2024      Stanislaw Horna         Configuration moved to the Config.json
    19-02-2024      Stanisław Horna         Requesting GitHub API, average calculation and generating plots
                                            moved to python script in order to generate bar char using matplotlib.pyplot
                                            and save it as PNG file in 2 separate versions:
                                                - dedicated for Light GitHub theme
                                                - dedicated for Dark GitHub theme
    20-02-2024      Stanisław Horna         Basic logs implemented
#>

param(
    [string]$AccessToken,
    [switch]$AlwaysCreateNewPlot,
    [switch]$DoNotMakePush
)

### USER EDITABLE SCRIPT VARIABLES ###
New-Variable -Name 'CONFIG_PATH' -Value "./Config.json" -Scope Script -Force

### INTERNAL SCRIPT VARIABLES ###
New-Variable -Name 'PLOT_UPDATE_REQUIRED' -Value $true -Scope Script -Force
New-Variable -Name 'LOGS_CACHE' -Value $(New-Object System.Collections.ArrayList) -Scope Script -Force
New-Variable -Name 'LOGS_FILE_CREATED' -Value $false -Scope Script -Force

New-Variable -Name 'LIST_VARIABLE' -Value @(
    "LANGUAGES_TO_BE_SKIPPED"
) -Scope Script -Force

New-Variable -Name 'DEFAULT_PARAMS' -Value @{
    'REPO_URL_TO_UPDATE'          = $null
    'PNG_LOCATION_IN_REPO'        = $null
    'COMMIT_MESSAGE'              = "AutoUpdate Top Used Languages"
    'REPO_DIRECTORY'              = "./Repository_to_update"
    'PLOTS_DIR_NAME'              = "./LanguageBarCharts"
    'PLOT_TITLE'                  = "Top Used Languages (including private repositories)"
    'LANGUAGE_TEMP_FILE_PATH'     = "./LanguageStats.json"
    'LOGS_DIR'                    = "./Log"
    'NUMBER_OF_LOG_FILES_TO_KEEP' = 10
    'LANGUAGES_TO_BE_SKIPPED'     = @("HTML", "CSS", "C#", "CMake", "JavaScript", "Assembly")
    'GITHUB_TOKEN'                = $null
} -Scope Script -Force

Function Invoke-main {
    $ErrorActionPreference = 'Stop'
    $EXIT_CODE = 0
    try {
        Out-Log -Type "info" -Message "Script started"
        Set-ScriptVariables
        New-LogFile
        $oldCache = Import-LangStatsCache
        Invoke-PythonGeneratePlot
        $newCache = Import-LangStatsCache
        Invoke-ComparisonCurrentValuesWithPrevious -old $oldCache -new $newCache
        Invoke-RepositoryClone
        Invoke-CommitAndPush
    }
    catch {
        Write-Host  $_ -ForegroundColor Red
        $EXIT_CODE = 1
    }
    
    Out-Log -Type "info" -Message "Script completed with code $EXIT_CODE"
    exit $EXIT_CODE
}

function Set-ScriptVariables {
    Out-Log -Type "info" -Message "Set script variable started"
    if (-not $(Test-Path -Path $CONFIG_PATH)) {
        Out-Log -Type "warning" -Message "Config does not found"
        Get-AccessToken
        $DEFAULT_PARAMS | ConvertTo-Json | Out-File -FilePath $CONFIG_PATH
        Out-Log -Type "info" -Message "Config file created using default value"
    }
    $JSONconfig = Get-Content -Path $CONFIG_PATH | ConvertFrom-Json -AsHashtable
    # If script is invoked with access token, save it to the file
    if (-not $([string]::IsNullOrEmpty($AccessToken))) {
        $JSONconfig.GITHUB_TOKEN = $([System.Convert]::ToBase64String([System.Text.Encoding]::UTF8.GetBytes($AccessToken)))
        $JSONconfig | ConvertTo-Json | Out-File -FilePath $CONFIG_PATH
        Out-Log -Type "info" -Message "Encoded GitHub Access token saved to config file"
    }
    # Create a variable for each defined param,
    # If it exists in JSON config use the value from file
    # Otherwise use default value
    foreach ($var in $DEFAULT_PARAMS.Keys) {
        if ($JSONconfig.ContainsKey($var)) {
            New-Variable -Name $var -Value $($JSONconfig.$var) -Scope Script -Force
            Out-Log -Type "info" -Message "Variable $var created with value from config file assigned"
        }
        else {
            New-Variable -Name $var -Value $($DEFAULT_PARAMS.$var) -Scope Script -Force
            Out-Log -Type "info" -Message "Variable $var created with default value assigned"
        }
    }
    
    foreach ($var in $LIST_VARIABLE) {
        $TempHash = @{}
        foreach ($item in $JSONconfig.$var) {
            $TempHash.Add($item, "")
            Out-Log -Type "info" -Message "List Variable $var updated with $item value"
        }
        New-Variable -Name $var -Value $($TempHash) -Scope Script -Force
    }
    $Script:GITHUB_TOKEN = [System.Text.Encoding]::UTF8.GetString(([System.Convert]::FromBase64String(($($Script:GITHUB_TOKEN)))))
    Out-Log -Type "info" -Message "Github Token Decoded"
}

function Get-AccessToken {
    Out-Log -Type "info" -Message "Get access token started"
    # If AccessToken is not provided, ask for it,
    # if AccessToken is provided, use it
    if ([string]::IsNullOrEmpty($AccessToken)) {
        $AccessToken = Read-Host -Prompt "Enter your GitHub Personal Access Token"
        Out-Log -Type "info" -Message "User provided GitHub Access Token"
    }
    # Add coded token to the default hash table in order to save it as config
    $DEFAULT_PARAMS.Add(
        'GITHUB_TOKEN', 
        $([System.Convert]::ToBase64String([System.Text.Encoding]::UTF8.GetBytes($AccessToken))) 
    ) 
}

function Import-LangStatsCache {
    Out-Log -Type "info" -Message "Language cache file imported"
    return $(Get-Content -Path $LANGUAGE_TEMP_FILE_PATH | ConvertFrom-Json -Depth 3 -AsHashtable)
}

function Invoke-PythonGeneratePlot {
    Out-Log -Type "info" -Message "Starting Python script"
    
    $null = python3 ./Generate_Plot.py -l "$($Script:LOG_PATH)"
    
    Out-Log -Type "info" -Message "Python script exited with code $LASTEXITCODE"
    
    if ($LASTEXITCODE -ne 0){
        throw "Python script did not completed successfully"
    }
}

function Invoke-ComparisonCurrentValuesWithPrevious {
    param(
        $old,
        $new
    )
    Out-Log -Type "info" -Message "Language Stats comparison started"
    # Skip verification if AlwaysCreateNewPlot is set to true
    if ($AlwaysCreateNewPlot) {
        Out-Log -Type "info" -Message "Comparison skiped due to AlwaysCreateNewPlot param usage"
        return
    }
    # Loop through each language in old hash table
    foreach ($lang in $new.Keys) {
        # Check if value for particular language did not change
        if ($new.$lang -ne $old.$lang) {
            Out-Log -Type "info" -Message "$lang has different value (old: $($old.$lang) ; new: $($new.$lang))"
            return
        }
    }
    foreach ($lang in $old.Keys) {
        # Check if value for particular language did not change
        if ($old.$lang -ne $new.$lang) {
            Out-Log -Type "info" -Message "$lang has different value (old: $($old.$lang) ; new: $($new.$lang))"
            return
        }
    }
    # If all checks passed without exiting, no changes were detected
    # So, no plot update is required
    $Script:PLOT_UPDATE_REQUIRED = $false
    Out-Log -Type "info" -Message "Plot update is not required"
}

function Invoke-RepositoryClone {
    Out-Log -Type "info" -Message "Repository clone started"
    # Skip execution if Plot Update is not required or DoNotMakePush script input is set to true
    if ((-not $PLOT_UPDATE_REQUIRED) -or $DoNotMakePush -or $($null -eq $Script:REPO_URL_TO_UPDATE)) {
        Out-Log -Type "info" `
            -Message "Repository clone skipped (PLOT_UPDATE_REQUIRED: $PLOT_UPDATE_REQUIRED, DoNotMakePush: $DoNotMakePush, REPO_URL_TO_UPDATE is null: $($null -eq $Script:REPO_URL_TO_UPDATE))"
        return
    }
    # Clone git repository to update using GitHub token
    try {
        git clone $($REPO_URL_TO_UPDATE.Replace("https://", "https://oauth2:$GITHUB_TOKEN@")) $REPO_DIRECTORY -q
        Out-Log -Type "info" -Message "Repository to update cloned ($REPO_URL_TO_UPDATE)"
    }
    catch {
        Out-Log -Type "error" -Message "Failed to clone repository due to error: $_"
        throw $_.Exception.Message
    }
    
    
    # Copy Plot file to Repository directory
    New-Variable -Name "PLOT_UPDATE_REPO_PATH" `
        -Value "$($PNG_LOCATION_IN_REPO)/$($PLOTS_DIR_NAME.replace('./',''))" `
        -Scope Global -Force
    try {
        Remove-Item -Path "$REPO_DIRECTORY/$PLOT_UPDATE_REPO_PATH" -Recurse -Force
    }
    catch {
        Out-Log -Type "warning" -Message "Failed to remove old plot directory due to error: $_"
    }
    
    Copy-Item -Path $PLOTS_DIR_NAME -Destination "$REPO_DIRECTORY/$PLOT_UPDATE_REPO_PATH" -Recurse -Force
    Out-Log -Type "info" -Message "Plots copied to new repository"
    # Change directory to repository directory
    Set-Location $REPO_DIRECTORY
}

function Invoke-CommitAndPush {
    Out-Log -Type "info" -Message "Commit and push started"
    # Skip execution if Plot Update is not required or DoNotMakePush script input is set to true
    if ((-not $PLOT_UPDATE_REQUIRED) -or $DoNotMakePush -or $($null -eq $Script:REPO_URL_TO_UPDATE)) {
        Out-Log -Type "info" `
            -Message "Repository commit and push skipped (PLOT_UPDATE_REQUIRED: $PLOT_UPDATE_REQUIRED, DoNotMakePush: $DoNotMakePush, REPO_URL_TO_UPDATE is null: $($null -eq $Script:REPO_URL_TO_UPDATE))"
        return
    }
    $date = (Get-Date).ToString("yyyy-MM-dd HH:mm")
    # Add plot file to stage
    try {
        git add .
        Out-Log -Type "info" -Message "Files successfully added to stage"
    }
    catch {
        Out-Log -Type "error" -Message "Failed to add files to stage due to error: $_"
        throw $_.Exception.Message
    }

    # Commit changes
    git commit -m "$COMMIT_MESSASGE $date" -q
    # Push changes to GitHub
    try {
        git push -q
        Out-Log -Type "info" -Message "Git push completed successfully"
    }
    catch {
        Out-Log -Type "error" -Message "Failed to push stage to repo due to error: $_"
        throw $_.Exception.Message
    }
    # Change directory back to parent directory
    Set-Location ..
    # Remove repository directory
    Remove-Item -Path $REPO_DIRECTORY -Recurse -Force
    Out-Log -Type "info" -Message "Temporary directory for repo to update removed"
}

function New-LogFile {
    Out-Log -Type "info" -Message "New log file started"
    $date = (Get-Date).ToString("yyyy-MM-dd_HH-mm-ss")
    if (-not $(Test-Path -Path $LOGS_DIR)) {
        try {
            $null = New-Item -Path $LOGS_DIR -ItemType Directory
            Out-Log -Type "info" -Message "Directory for logs created"
        }
        catch {
            Out-Log -Type "error" -Message "Failed to create directory for logs"
            Write-Host $Script:LOGS_CACHE
            throw $_
        }
    }
    Invoke-OldLogsCleanup
    New-Variable -Name "LOG_PATH" -Value "$LOGS_DIR/Execution_$date.log" -Scope Script -Force
    $Script:LOGS_FILE_CREATED = $true
}
function Invoke-OldLogsCleanup {
    if ($NUMBER_OF_LOG_FILES_TO_KEEP -ge 1) {
        $LogsToDelete = Get-ChildItem -Path $LOGS_DIR | `
            Sort-Object { $_.LastWriteTime } -Descending | `
            Select-Object -Skip $($NUMBER_OF_LOG_FILES_TO_KEEP - 1)
    }
    else {
        $LogsToDelete = Get-ChildItem -Path $LOGS_DIR 
    }

    foreach ($file in $LogsToDelete) {
        try {
            Remove-Item -Path $file.FullName -Force
        }
        catch {
            Out-Log -Type "error" -Message "Failed to remove old log file due to error: $_"
        }
    }
}

function Out-Log {
    param(
        $Message,
        $Type
    )
    $date = (Get-Date).ToString("HH:mm:ss.fff")
    $log = "$date - [PowerShell] - [$($Type.toUpper())] - $Message"
    if ($Script:LOGS_FILE_CREATED) {
        if ($null -ne $Script:LOGS_CACHE) {
            foreach ($item in $Script:LOGS_CACHE) {
                $item | Out-File -FilePath $Script:LOG_PATH -Append
            }
            $Script:LOGS_CACHE = $null
            Out-Log -Type "info" -Message "Logs cache variable emptied"
        }
        $log | Out-File -FilePath $Script:LOG_PATH -Append
    }
    else {
        $null = $Script:LOGS_CACHE.add($log)
    }
}

Invoke-main