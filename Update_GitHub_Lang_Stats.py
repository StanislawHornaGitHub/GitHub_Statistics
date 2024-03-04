"""
.SYNOPSIS
    Script to generate Language statistics for GitHub user authenticated with provided token and 
    update repository with horizontal bar charts representing used programming languages.

.DESCRIPTION
    Program to download Language usage stats for GitHub repositories for user authenticated with provided token, 
    calculate the average for each not excluded language (Config.json),
    generate 2 versions of plots to be included in GitHub profile README:
        - plot for Light GitHub theme
        - plot for Dark GitHub theme
        
    GitHub Access Token will be also saved to file for future use.
    Script uses GitHub API to collect list of repositories ang language stats for each of them.
    
    FIRST RUN INSTRUCTION
        In order to correctly generate proper Config.json file you need to copy and fill in JSON structure
    presented in INPUTS section. The name must be "Config.json" and it must be located in the same directory as script
    
    First script run: python3 ./Update_GitHub_Lang_Stats.py --Access_Token "<here_paste_your_GitHub_token>"
    
    During first script run you can also use other script input params according to your needs.
    It is recommended to use --Do_Not_Make_Push param to firstly verify if token is granting enough access
    remember that using mentioned param will skip removing directory with cloned repository,
    so once the script will end you can verify the results.
    
.INPUTS
    SCRIPT INPUTS
        (-a) --Access_Token - token to be used to authenticate with GitHub API
        
        (-n) --Always_Create_New_Plot - switch to create new plot file, independently if stats changed or not
            Creating new plot will also trigger readme update
            
        (-d) --Do_Not_Make_Push - switch to prevent cloning destination repository and pushing changes in README

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
    
.NOTES

    Version:            2.2
    Author:             Stanisław Horna
    Mail:               stanislawhorna@outlook.com
    GitHub Repository:  https://github.com/StanislawHornaGitHub/GitHub_Statistics
    Creation Date:      19-Feb-2024
    ChangeLog:

    Date            Who                     What
    2024-02-20      Stanisław Horna         Basic logs implemented
    2024-02-21      Stanisław Horna         LanguageStats JSON file added to be pushed to destination repository
    2024-03-01      Stanisław Horna         All operations performed previously in .ps1 moved to .py
    2024-03-03      Stanisław Horna         Language name translation implemented. Changes in Config file.
    2024-03-04      Stanisław Horna         Creating Log instance moved to main function to prevent displaying logs,
                                            while using -h param for help.
                                            Info for the user what was done:
                                            "Destination repository has NOT been updated, because --Do_Not_Make_Push was used."
                                            "Destination repository has NOT been updated, because stats did not change."
                                            "Destination repository has been successfully updated."

"""

import os
import argparse
from datetime import datetime

# Custom modules import
from Dependencies.Function_GitHubAPI import getRepositoryList, getRepositoryLanguageStats
from Dependencies.Function_Config import setCorrectPath, getConfiguration
from Dependencies.Function_Stats import *
from Dependencies.Function_BarChart import *
from Dependencies.Function_GitHubRepos import *
from Dependencies.Class_Log import Log

# argparse configuration section
programSynopsis = '''
Script to generate Language statistics for GitHub user authenticated with provided token and 
update repository with horizontal bar charts representing used programming languages.
'''

parser = argparse.ArgumentParser(description=programSynopsis)
parser.add_argument(
    "-a",
    "--Access_Token",
    action="store",
    help="Access token for GitHub authentication",
)
parser.add_argument(
    "-n",
    "--Always_Create_New_Plot",
    action="store_true",
    help="Force to crate new plot despite ",
)
parser.add_argument(
    "-d",
    "--Do_Not_Make_Push",
    action="store_true",
    help="Prevents committing and pushing changes to repository to update",
)


def main(options):

    # Init logger and write first message
    Logger = Log()
    Logger.writeLog("info", "Script started")

    # Set correct working directory in order to work with relative paths
    setCorrectPath(Logger),

    # Read config file with required variables
    configuration = getConfiguration(options, Logger)

    # Set proper directory for Log class to write them to file
    # Clean up log directory from outdated files
    Logger.setLogDirectory(configuration["LOGS_DIR"])
    Logger.cleanUpOldLogFiles(configuration["NUMBER_OF_LOG_FILES_TO_KEEP"])

    # Clone repository to update configured in Config.json
    clone(
        configuration["REPO_URL_TO_UPDATE"],
        configuration["REPO_DIRECTORY"],
        configuration["GITHUB_TOKEN"],
        Logger
    )

    # Download list of repositories for user authenticated with provided token in config file
    # Download Language statistics for each repository from the list
    repositories = getRepositoryList(configuration, Logger)
    repositories = getRepositoryLanguageStats(repositories, Logger)

    # Loop through each repository and create a stats summary grouped by programming language
    # Based on created summary calculate percentage for each programming language
    stats = calculateLanguageUsage(configuration, repositories, Logger)
    stats = calculateLanguagePercentage(stats, Logger)

    # Save calculated percentage summary as JSON file in order to have file to compare in next execution
    saveBarChartData(
        stats=stats["Percentage"],
        filePath=os.path.join(
            os.getcwd(),
            configuration['PLOTS_DIR_NAME'],
            configuration['LANGUAGE_TEMP_FILE_NAME']
        ),
        Logger=Logger
    )

    # Check if anything changed by comparing language percentage from now and cloned repository to update
    plotUpdateIsRequired = checkIfPlotUpdateIsRequired(
        NewStatsPath=os.path.join(
            os.getcwd(),
            configuration['PLOTS_DIR_NAME'],
            configuration['LANGUAGE_TEMP_FILE_NAME']
        ),
        OldStatsPath=os.path.join(
            os.getcwd(),
            configuration['REPO_DIRECTORY'],
            configuration['PNG_LOCATION_IN_REPO'],
            configuration['PLOTS_DIR_NAME'],
            configuration['LANGUAGE_TEMP_FILE_NAME']
        ),
        Logger=Logger
    )

    # Create horizontal bar chart if language percentage differs
    # or if script switch --Always_Create_New_Plot was used
    if plotUpdateIsRequired or options.Always_Create_New_Plot:

        # Create PNG file with chart for Light version of GitHub:
        # transparent background and black font color
        saveBarChart(
            stats=stats["Percentage"],
            filePath=os.path.join(
                os.getcwd(),
                configuration['PLOTS_DIR_NAME'],
                "Light.png"
            ),
            plotTitle=configuration["PLOT_TITLE"],
            labelsTextColor='black',
            Logger=Logger
        )

        # Create PNG file with chart for Dark version of GitHub:
        # transparent background and white font color
        saveBarChart(
            stats=stats["Percentage"],
            filePath=os.path.join(
                os.getcwd(),
                configuration['PLOTS_DIR_NAME'],
                "Dark.png"
            ),
            plotTitle=configuration["PLOT_TITLE"],
            labelsTextColor='white',
            Logger=Logger
        )

        # Copy directory containing both versions of bar charts and JSON file with lang percentage,
        # to "repository to update" directory to location defined in config file
        copyNewPlotsToRepo(
            sourceDirectory=os.path.join(
                os.getcwd(),
                configuration['PLOTS_DIR_NAME']
            ),
            destinationPath=os.path.join(
                os.getcwd(),
                configuration['REPO_DIRECTORY'],
                configuration['PNG_LOCATION_IN_REPO'],
                configuration['PLOTS_DIR_NAME']
            ),
            Logger=Logger
        )

        # If --Do_Not_Make_Push switch arg was NOT used enter the section to:
        #   commit changes
        #   push them to repository to update
        #   remove directory where repo clone was saved
        if options.Do_Not_Make_Push:
            print(
                "Destination repository has NOT been updated, because --Do_Not_Make_Push was used.")
        else:

            # Add all changed files to stage,
            # commit them with message from config file with added date and hour
            commit(
                repoDirectory=os.path.join(
                    os.getcwd(),
                    configuration['REPO_DIRECTORY']
                ),
                commitMessage=" ".join([
                    configuration["COMMIT_MESSAGE"],
                    datetime.now().strftime('%Y-%m-%d %H:%M')
                ]),
                Logger=Logger
            )

            # Push committed files to repository to update from config file
            push(
                repoDirectory=os.path.join(
                    os.getcwd(),
                    configuration['REPO_DIRECTORY']
                ),
                Logger=Logger
            )

            # Remove directory where repo clone was saved
            cleanUpTempFiles(
                repoDirectory=os.path.join(
                    os.getcwd(),
                    configuration['REPO_DIRECTORY']
                ),
                Logger=Logger
            )

            print("Destination repository has been successfully updated.")

    # Neither changes in language percentage was found
    # nor script switch --Always_Create_New_Plot was used
    else:

        print("Destination repository has NOT been updated, because stats did not change.")

        # If --Do_Not_Make_Push switch arg was used prevent removing repo to update directory
        if not options.Do_Not_Make_Push:

            # Remove directory where repo clone was saved
            cleanUpTempFiles(
                repoDirectory=os.path.join(
                    os.getcwd(),
                    configuration['REPO_DIRECTORY']
                ),
                Logger=Logger
            )

    # Write completion message
    Logger.writeLog("info", "Script completed")

    return None


# Run only if this file is called
if __name__ == "__main__":

    # invoke main function with parser args
    main(parser.parse_args())
