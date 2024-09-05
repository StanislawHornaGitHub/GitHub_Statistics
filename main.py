from dotenv import load_dotenv
from src.GitHub import GitHub
from src.UsedLanguages import UsedLanguages
from src.BarChart import BarChart


def main():
    repositories = GitHub.get_repo_list()
    print(
        "Found {num_of_repos} repositories".format(
            num_of_repos=len(repositories)
        )
    )

    language_stats = UsedLanguages()
    language_stats.print_config()
    
    for repo in repositories:
        language_stats.add(GitHub.get_repo_language(repo.full_name))
        print(
            "Processed {repo_full_name}".format(
                repo_full_name=repo.full_name
            )
        )

    BarChart.save_plot(language_stats, dark_theme=True)
    print("Plot for dark theme saved")
    BarChart.save_plot(language_stats, dark_theme=False)
    print("Plot for light theme saved")


if __name__ == "__main__":
    load_dotenv() 
    main()
