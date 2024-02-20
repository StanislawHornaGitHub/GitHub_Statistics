"""
.DESCRIPTION
    Program to download Language usage stats for GitHub repositories, 
    calculate the average for each not excluded language,
    generate 2 versions of plots to be included in GitHub profile README:
        - plot for Light GitHub theme
        - plot for Dark GitHub theme

.NOTES

    Version:            1.1
    Author:             Stanisław Horna
    Mail:               stanislawhorna@outlook.com
    GitHub Repository:  https://github.com/StanislawHornaGitHub/GitHub_Statistics
    Creation Date:      19-Feb-2024
    ChangeLog:

    Date            Who                     What
    20-02-2024      Stanisław Horna         Basic logs implemented

"""
import json
import argparse
from Dependencies.Function_GitHubAPI import getRepositoryList, getRepositoryLanguageStats
from Dependencies.Function_Config import setCorrectPath, getConfiguration
from Dependencies.Function_Stats import calculateLanguageUsage, calculateLanguagePercentage
from Dependencies.Function_BarChart import saveBarChart
from Dependencies.Function_Logs import Log

programSynopsis = """
Program to download Language usage stats for GitHub repositories, 
calculate the average for each not excluded language,
generate 2 versions of plots to be included in GitHub profile
"""

parser = argparse.ArgumentParser(description=programSynopsis)

parser.add_argument(
    "-l",
    "--logs_File_Path",
    action="store",
    help="path to the log file",
)

def main(options):
    
    setCorrectPath(),
    Logger = Log(options.logs_File_Path)

    configuration = getConfiguration()

    repositories = getRepositoryList(configuration, Logger)
    repositories = getRepositoryLanguageStats(repositories, Logger)
    stats = calculateLanguageUsage(configuration, repositories, Logger)

    stats = calculateLanguagePercentage(stats, Logger)
    
    saveBarChartData(stats["Percentage"],
                     configuration["LANGUAGE_TEMP_FILE_PATH"],
                     Logger
                     )

    saveBarChart(stats=stats["Percentage"],
                 filePath=f"{configuration["PLOTS_DIR_NAME"]}/Light.png",
                 plotTitle=configuration["PLOT_TITLE"],
                 Logger=Logger
                 )

    saveBarChart(stats=stats["Percentage"],
                 filePath=f"{configuration["PLOTS_DIR_NAME"]}/Dark.png",
                 plotTitle=configuration["PLOT_TITLE"],
                 labelsTextColor='white',
                 Logger=Logger
                 )
    exit(0)


def saveBarChartData(percentageStats: dict[str, float], fileName: str, Logger: Log) -> None:
    fileName = fileName.replace("./", "")
    with open(fileName, "w") as cache:
        cache.write(json.dumps(percentageStats))
    Logger.writeLog("info",f"BarChart data is saved under the file: {fileName}")
    return


if __name__ == "__main__":
    main(parser.parse_args())
