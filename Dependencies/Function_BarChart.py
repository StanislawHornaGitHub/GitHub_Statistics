"""
.DESCRIPTION
    Module of functions to work with charts.

    saveBarChart
        Generates and saves BarChart with transparent background.
        Input params:
            - stats <- dict with statistical information to represent
            - filePath <- path for destination file
            - plotTitle <- title to be displayed in the result file above the chart
            - labelsTextColor <- the color of all labels in the chart
    
    saveBarChartData
        saves raw source data for bar chart as JSON file

.NOTES

    Version:            1.2
    Author:             Stanisław Horna
    Mail:               stanislawhorna@outlook.com
    GitHub Repository:  https://github.com/StanislawHornaGitHub/GitHub_Statistics
    Creation Date:      19-Feb-2024
    ChangeLog:

    Date            Who                     What
    2024-02-20      Stanisław Horna         Basic logs implemented
    2024-03-01      Stanisław Horna         saveBarChartData moved from main file
    
"""
import json

import matplotlib.pyplot as plt
import matplotlib.ticker as mtick

from Dependencies.Class_Log import Log


def saveBarChart(
    stats: dict[str, float],
    Logger: Log,
    filePath: str = "bar_chart.png",
    plotTitle: str = "Top Used Languages",
    labelsTextColor: str = 'black'
) -> None:

    # create local variables for better visibility
    langs = list(stats.keys())
    values = list(stats.values())

    Logger.writeLog(
        "info",
        f"Creating BarChart to save as {filePath}"
    )
    Logger.writeLog(
        "info",
        f"plotTitle: {plotTitle}, labelsTextColor: {labelsTextColor}"
    )
    # create plot with fixed width and hight related to the number of langs to display
    fig, ax = plt.subplots(figsize=(10, int(len(langs)/2)))

    # provide values to chart with different colors for each bar
    bars = ax.barh(langs, values, color=plt.cm.get_cmap('tab10_r').colors)
    Logger.writeLog("info", f"Chart created with provided values")
    # set Language names in bold
    ax.set_yticks(langs)
    ax.set_yticklabels(langs, fontweight='bold', color=labelsTextColor)

    ax.set_title(plotTitle, fontweight='bold', color=labelsTextColor)

    # set x axis scale as percentage and disable displaying X axis
    ax.xaxis.set_major_formatter(mtick.PercentFormatter(1.0))
    ax.xaxis.set_visible(False)
    Logger.writeLog(
        "info", f"title, axis labels and scale set, X axis formatted as percentage")
    # Display label with exact value for each bar
    _, xmax = ax.get_xlim()
    _, ymax = ax.get_ylim()
    valueIterator = 0
    for bar in bars:
        # format value label to display
        label_to_display = f'{values[valueIterator]*100:.2f}%'
        # get the Y position of the bar and center it inside it
        label_y_pos = (bar.get_y() + bar.get_height() / 2) - ymax * 0.004

        # get X end position of bar
        label_x_pos = bar.get_width()
        # Check if bar is longer than 20% of the whole chart
        if label_x_pos / xmax > 0.20:
            # if yes correct the position to center the label
            label_x_pos /= 2
            label_x_pos -= xmax * 0.05
        else:
            # if not offset the position of label from end of the bar
            label_x_pos += xmax * 0.01

        # set the value label
        ax.text(label_x_pos, label_y_pos, label_to_display,
                va='center', weight='bold', color=labelsTextColor)
        valueIterator += 1

    Logger.writeLog("info", f"Value labels for each bar set")

    # Remove frame around bars
    for spine in ax.spines.values():
        spine.set_visible(False)
    Logger.writeLog("info", f"Plot surrounding disabled")

    # prevent cutting off longer language names
    plt.tight_layout()
    Logger.writeLog("info", f"Layout to prevent cutting off labels is set")

    # save plot as file
    plt.savefig(filePath, dpi=300, transparent=True)
    Logger.writeLog("info", f"Generated plot is saved as {filePath}")

    return None


def saveBarChartData(stats: dict[str, float], filePath: str, Logger: Log) -> None:

    Logger.writeLog("info", f"File path to save Bar Chart data: {filePath}")
    # try to save data to plot as json file
    try:
        with open(filePath, "w") as cache:
            cache.write(json.dumps(stats))
    except:
        Logger.writeLog("error", f"Failed to save Bar Chart data")

    Logger.writeLog("info", f"Bar Chart data is saved")

    return None
