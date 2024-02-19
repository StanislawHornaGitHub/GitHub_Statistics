import matplotlib.pyplot as plt
import matplotlib.ticker as mtick

def saveBarChart(stats: dict[str, float], fileName: str = "bar_chart.png", plotTitle: str = "Top Used Languages"):
    # create local variables for better visibility
    langs = list(stats.keys())
    values = list(stats.values())
    
    # create plot with fixed width and hight related to the number of langs to display
    fig, ax = plt.subplots(figsize=(10, int(len(langs)/2)))
    
    # provide values to chart with different colors for each bar
    bars = ax.barh(langs, values, color=plt.cm.get_cmap('tab10_r').colors)

    # set Language names in bold
    ax.set_yticks(langs)
    ax.set_yticklabels(langs, fontweight='bold', backgroundcolor='white')
    
    ax.set_title(plotTitle, fontweight='bold')
    
    # set x axis scale as percentage and disable displaying X axis
    ax.xaxis.set_major_formatter(mtick.PercentFormatter(1.0))
    ax.xaxis.set_visible(False)
    
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
            labelBackgroundColor = 'none'
        else:
            # if not offset the position of label from end of the bar
            label_x_pos += xmax * 0.01
            labelBackgroundColor = 'white'
        
        # set the value label
        ax.text(label_x_pos, label_y_pos, label_to_display, va='center', weight='bold',
                bbox=dict(facecolor=labelBackgroundColor, edgecolor='none', pad=2))
        valueIterator += 1
    
    # Remove frame around bars
    for spine in ax.spines.values():
        spine.set_visible(False)
    
    # prevent cutting off longer language names
    plt.tight_layout()
    
    # save plot as file
    plt.savefig(fileName, dpi=300)