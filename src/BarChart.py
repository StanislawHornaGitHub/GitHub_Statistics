import matplotlib.pyplot as plt
import matplotlib.ticker as mtick

from src.UsedLanguages import UsedLanguages


class BarChart:

    __plot_title: str = "Top Used Languages"

    __black_labels_text_color: str = "black"
    __white_labels_text_color: str = "white"

    __light_theme_filename_suffix: str = "light"
    __dark_theme_filename_suffix: str = "dark"

    __file_extension: str = ".png"

    @staticmethod
    def save_plot(languages: UsedLanguages, dark_theme: bool = False):

        labels_text_color, file_path = BarChart.__get_theme_config(dark_theme)

        # create local variables for better visibility
        stats = languages.get_percentage_summary()
        langs = list(stats.keys())
        values = list(stats.values())

        # create plot with fixed width and hight related to the number of langs to display
        fig, ax = plt.subplots(figsize=(10, int(len(langs)/2)))

        # provide values to chart with different colors for each bar
        bars = ax.barh(langs, values, color=plt.cm.get_cmap('tab10_r').colors)
        # set Language names in bold
        ax.set_yticks(langs)
        ax.set_yticklabels(langs, fontweight='bold', color=labels_text_color)

        ax.set_title(BarChart.__plot_title, fontweight='bold',color=labels_text_color)

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
            else:
                # if not offset the position of label from end of the bar
                label_x_pos += xmax * 0.01

            # set the value label
            ax.text(label_x_pos, label_y_pos, label_to_display,
                    va='center', weight='bold', color=labels_text_color)
            valueIterator += 1

        # Remove frame around bars
        for spine in ax.spines.values():
            spine.set_visible(False)

        # prevent cutting off longer language names
        plt.tight_layout()

        # save plot as file and wait until file will be created
        plt.savefig(f"./{file_path}", dpi=300, transparent=True)

    @staticmethod
    def __get_theme_config(dark_theme: bool = False):
        if dark_theme:
            return BarChart.__white_labels_text_color, "{title}-{suffix}{ext}".format(
                title=BarChart.__plot_title.replace(" ", "_"),
                suffix=BarChart.__dark_theme_filename_suffix,
                ext=BarChart.__file_extension
            )
        else:
            return BarChart.__black_labels_text_color, "{title}-{suffix}{ext}".format(
                title=BarChart.__plot_title.replace(" ", "_"),
                suffix=BarChart.__light_theme_filename_suffix,
                ext=BarChart.__file_extension
            )
