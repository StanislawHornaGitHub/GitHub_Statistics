"""
.DESCRIPTION
    Program to download Language usage stats for GitHub repositories, 
    calculate the average for each not excluded language,
    generate 2 versions of plots to be included in GitHub profile README:
        - plot for Light GitHub theme
        - plot for Dark GitHub theme

.NOTES

    Version:            1.0
    Author:             Stanisław Horna
    Mail:               stanislawhorna@outlook.com
    GitHub Repository:  https://github.com/StanislawHornaGitHub/GitHub_Statistics
    Creation Date:      19-Feb-2024
    ChangeLog:

    Date            Who                     What

"""
import json
from Dependencies.Function_GitHubAPI import getRepositoryList, getRepositoryLanguageStats
from Dependencies.Function_Config import setCorrectPath, getConfiguration
from Dependencies.Function_Stats import calculateLanguageUsage, calculateLanguagePercentage
from Dependencies.Function_BarChart import saveBarChart


def main():

    setCorrectPath(),

    configuration = getConfiguration()

    repositories = getRepositoryList(configuration)
    repositories = getRepositoryLanguageStats(repositories)
    stats = calculateLanguageUsage(configuration, repositories)

    stats = calculateLanguagePercentage(stats)
    
    saveBarChartData(stats["Percentage"],
                     configuration["LANGUAGE_TEMP_FILE_PATH"]
                     )

    saveBarChart(stats=stats["Percentage"],
                 filePath=f"{configuration["PLOTS_DIR_NAME"]}/Light.png",
                 plotTitle=configuration["PLOT_TITLE"]
                 )

    saveBarChart(stats=stats["Percentage"],
                 filePath=f"{configuration["PLOTS_DIR_NAME"]}/Dark.png",
                 plotTitle=configuration["PLOT_TITLE"],
                 labelsTextColor='white'
                 )
    
    exit(0)


def saveBarChartData(percentageStats: dict[str, float], fileName: str) -> None:
    fileName = fileName.replace("./", "")
    with open(fileName, "w") as cache:
        cache.write(json.dumps(percentageStats))
    return


if __name__ == "__main__":
    main()
