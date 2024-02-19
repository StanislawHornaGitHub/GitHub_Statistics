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
    saveBarChartData(stats["Percentage"], configuration["LANGUAGE_TEMP_FILE_PATH"])
    saveBarChart(stats["Percentage"], configuration["PLOT_FILE_PATH"], configuration["PLOT_TITLE"])
    exit(0)


def saveBarChartData(percentageStats: dict[str, float], fileName: str) -> None:
    fileName = fileName.replace("./","")
    with open(fileName, "w") as cache:
        cache.write(json.dumps(percentageStats))
    return


if __name__ == "__main__":
    main()
