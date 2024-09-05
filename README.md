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

# Output
As 2 charts are generated (for Light GitHub UI and Dark one) and both of them are pushed to destination repository, here is the MarkDown HTML to display the correct one according to the theme which is currently in use.

	<picture>
		<source media="(prefers-color-scheme: dark)" srcset="/Top_Used_Languages-dark.png" width="100%">
		<source media="(prefers-color-scheme: light)" srcset="/Top_Used_Languages-light.png" width="100%">
		<img alt="Shows a black text in light color mode and a white one in dark color mode." src="/Top_Used_Languages-light.png">
	</picture>

# Getting Started



# Required Python Packages
- requests
- matplotlib