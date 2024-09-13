# GitHub_Statistics
Script to generate Language statistics for GitHub user authenticated with provided token and 
update repository with horizontal bar charts representing used programming languages.

Script uses GitHub API to collect list of repositories ang language stats for each of them.
Authentication for the user account is based on the GitHub Access Token.

> [!TIP]
> Script can by run manually when you would like to update your profile repository,
> or you can set it up to be automatically executed using GitHub Actions.

### Here is the result:
<picture>
	<source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/StanislawHornaGitHub/GitHub_Statistics/BarCharts/Top_Used_Languages-dark.png" width="100%">
	<source media="(prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/StanislawHornaGitHub/GitHub_Statistics/BarCharts/Top_Used_Languages-light.png" width="100%">
	<img alt="Shows a black text in light color mode and a white one in dark color mode." src="https://raw.githubusercontent.com/StanislawHornaGitHub/GitHub_Statistics/BarCharts/Top_Used_Languages-light.png">
</picture>

# Getting Started
As 2 charts are generated (for Light GitHub UI and Dark one) and both of them are pushed to destination repository, here is the MarkDown HTML to display the correct one according to the theme which is currently in use.

	<picture>
		<source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/<your_gh_username>/<forked_repo>/BarCharts/Top_Used_Languages-dark.png" width="100%">
		<source media="(prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/<your_gh_username>/<forked_repo>/BarCharts/Top_Used_Languages-light.png" width="100%">
		<img alt="Shows a black text in light color mode and a white one in dark color mode." src="https://raw.githubusercontent.com/<your_gh_username>/<forked_repo>/BarCharts/Top_Used_Languages-light.png">
	</picture>

## GitHub Actions
1. Configure repository **secrets**:
    - create `GH_TOKEN` secret with token which will provide access to repositories to measure.
2. Configure repository **variables**:
    - create `LANG_NAME_MAP` JSON format dict, which will map GitHub default language names to preferred ones.
        I.e. `{"Shell": "Bash"}` will rename language classified as `Shell` to `Bash` in result charts.
        If you do not want any changes set the value to `{}`
    - create `LANG_TO_EXCLUDE` JSON format list, which will exclude some languages which you do not want to show.
        I.e. `["Jupyter Notebook"]` will exclude language classified as `Jupyter Notebook` from charts.
	- create `SELF_HOSTED` bool variable, which set to true will run GitHub action on runner with `self-hosted` label,
		otherwise the default `ubuntu-latest` will be used.

GitHub Action will be triggered every day at midnight.

## Local run
1. Create `.env` file with following values:
	- `GH_TOKEN` secret with token which will provide access to repositories to measure.
	- `LANG_NAME_MAP` JSON format dict, which will map GitHub default language names to preferred ones.
        I.e. `{"Shell": "Bash"}` will rename language classified as `Shell` to `Bash` in result charts.
	- `LANG_TO_EXCLUDE` JSON format list, which will exclude some languages which you do not want to show.
        I.e. `["Jupyter Notebook"]` will exclude language classified as `Jupyter Notebook` from charts.
2. Install python libraries `pip install -r requirements.txt`
3. Run `main.py`
4. Charts will be saved in `/tmp/` directory

