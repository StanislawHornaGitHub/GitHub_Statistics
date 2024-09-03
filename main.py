from src.GitHub import GitHub
from src.UsedLanguages import UsedLanguages
from src.BarChart import BarChart

def main():
    repositories = GitHub.get_repo_list()
    language_stats = UsedLanguages()
    for repo in repositories:
        language_stats.add(GitHub.get_repo_language(repo.full_name))

    BarChart.save_plot(language_stats, black_theme=True)
    BarChart.save_plot(language_stats, black_theme=False)


if __name__ == "__main__":
    main()