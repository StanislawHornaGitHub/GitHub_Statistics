# GitHub_Statistics
Script to generate Language statistics for GitHub user authenticated with provided token and 
update repository with horizontal bar charts representing used programming languages.

Script uses GitHub API to collect list of repositories ang language stats for each of them.
Authentication for the user account is based on the GitHub Access Token, 
which is also saved locally for further use.

> [!TIP]
> Script can by run manually when you would like to update your profile repository,
> or you can set it up to be automatically executed using CRON or Windows Task Scheduler.

### Here is the result:
<picture>
	<source media="(prefers-color-scheme: dark)" srcset="/LanguageBarCharts/Dark.png" width="100%">
	<source media="(prefers-color-scheme: light)" srcset="/LanguageBarCharts/Light.png" width="100%">
	<img alt="Shows a black text in light color mode and a white one in dark color mode." src="/LanguageBarCharts/Light.png">
</picture>

# Output
As 2 charts are generated (for Light GitHub UI and Dark one) and both of them are pushed to destination repository, here is the MarkDown HTML to display the correct one according to the theme which is currently in use.

	<picture>
		<source media="(prefers-color-scheme: dark)" srcset="/LanguageBarCharts/Dark.png" width="100%">
		<source media="(prefers-color-scheme: light)" srcset="/LanguageBarCharts/Light.png" width="100%">
		<img alt="Shows a black text in light color mode and a white one in dark color mode." src="/Pictures/LanguageBarCharts/Light.png">
	</picture>


# First Run Guide
In order to correctly generate proper Config.json file you need to copy and fill in the JSON structure
The name must be "Config.json" and it must be located in the same directory as script.

### First script run: 
    
    python3 ./Update_GitHub_Lang_Stats.py --Access_Token "<here_paste_your_GitHub_token>"

During first script run you can also use other script input params according to your needs.
It is recommended to use `--Do_Not_Make_Push` param to firstly verify if token is granting enough access
remember that using mentioned param will skip removing directory with cloned repository,
so once the script will end you can verify the results.

# Script inputs
- (-a) --Access_Token - token to be used to authenticate with GitHub API

- (-n) --Always_Create_New_Plot - switch to create new plot file, independently if stats changed or not
    Creating new plot will also trigger readme update
    
- (-d) --Do_Not_Make_Push - switch to prevent cloning destination repository and pushing changes in README

### Config.json
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
                                        ],
            "LANGUAGE_NAME_MAP": {
                                    "<GitHub_Language_Name>": "<Your_custom_name>",
                                    "<GitHub_Language_Name>": "<Your_custom_name>"
                                }
        }

# Required Python Packages
- requests
- matplotlib