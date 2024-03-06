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
        saves raw source data for bar chart as JSON file.

    removeFileIfExist
        removes file under the given path if it exists.
        
    waitUntilFileExist
        waits until file under the given path is created. 
        Implemented along with timeout, so it will not be waiting forever

.NOTES

    Version:            1.4
    Author:             Stanisław Horna
    Mail:               stanislawhorna@outlook.com
    GitHub Repository:  https://github.com/StanislawHornaGitHub/GitHub_Statistics
    Creation Date:      19-Feb-2024
    ChangeLog:

    Date            Who                     What
    2024-02-20      Stanisław Horna         Basic logs implemented.
    2024-03-01      Stanisław Horna         saveBarChartData moved from main file.
    2024-03-06      Stanisław Horna         saveBarChart extended to remove existing file,
                                            before creating new one, as well as function is waiting,
                                            until new file is actually created and saved.
    
"""
import time
import json
import os

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

    # remove existing file
    removeFileIfExist(filePath)
    
    Logger.writeLog("info", f"Creating plot file")
    # save plot as file and wait until file will be created
    plt.savefig(filePath, dpi=300, transparent=True)
    waitUntilFileExist(filePath)
    
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

def removeFileIfExist(filePath: str) -> None:
    
    # check if file exists
    if os.path.isfile(filePath):
        
        # remove existing file 
        os.remove(filePath)

    return None

def waitUntilFileExist(filePath: str, msCheckInterval: int = 200, msTimeout: int = 60000) -> None:
    
    # check if timeout is greater than checks interval
    if msCheckInterval > msTimeout:
        raise Exception("msCheckInterval can not be greater than msTimeout")
    
    # calculate maximum ticks number fo while loop, init the counter
    maxCounter = msTimeout // msCheckInterval
    counter = 0
    
    # loop until file is created or max ticks are reached
    while not os.path.isfile(filePath) and counter < maxCounter:
        
        # invoke sleep for configured time in milliseconds
        time.sleep(msCheckInterval/1000)
        
        # increment ticks counter
        counter += 1
    
    return None