# GitHub_Statistics
Program to download your GitHub account statistics and generate plots representing programming / scripting languages used the most. 

Project consists of PowerShell and Python scripts:
- PowerShell <- responsible for collecting and encoding Access Token to GitHub, cloning, committing and pushing changes to repository you like to update with newly created plots

- Python <- responsible for requesting GitHub API to collect statistical data, calculate percentages for each language, generate and save plots for Light and Dark layouts.

# Output
As 2 charts are generated (for Light GitHub UI and Dark one) and both of them are pushed to destination repository, here is the MarkDown HTML to display the correct one according to the theme which is currently in use.

	<picture>
		<source media="(prefers-color-scheme: dark)" srcset="/LanguageBarCharts/Dark.png" width="100%">
		<source media="(prefers-color-scheme: light)" srcset="/LanguageBarCharts/Light.png" width="100%">
		<img alt="Shows a black text in light color mode and a white one in dark color mode." src="/Pictures/LanguageBarCharts/Light.png">
	</picture>

### Here is the result:
<picture>
	<source media="(prefers-color-scheme: dark)" srcset="/LanguageBarCharts/Dark.png" width="100%">
	<source media="(prefers-color-scheme: light)" srcset="/LanguageBarCharts/Light.png" width="100%">
	<img alt="Shows a black text in light color mode and a white one in dark color mode." src="/LanguageBarCharts/Light.png">
</picture>

# Configuration
1. Create a file Config.json in the same directory as Get-GitHubStats.ps1 and Generate_Plot.py, or simply run the script with following command:

		./Get-GitHubStats.ps1 -AccessToken "<here_paste_your_GitHub_token>"
	and Config.json will be created automatically with default values.
	Config.json structure: 

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

2. Run PowerShell script using following command if it was not done previously to encode GitHub token in config file. In next runs you will not have to provide access token, it is required only during the first run.

3. Script can by run manually when you would like to update your profile repository or you can set it up to be automatically executed using CRON or Windows Task Scheduler.