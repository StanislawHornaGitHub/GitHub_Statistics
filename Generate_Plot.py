
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
    saveBarChart(stats["Percentage"])
    exit(0)

if __name__ == "__main__":
    main()