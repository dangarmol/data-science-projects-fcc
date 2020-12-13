import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import numpy as np
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# Import data (Make sure to parse dates. Consider setting index column to 'date'.)
df = pd.read_csv("fcc-forum-pageviews.csv", parse_dates=True)
df.set_index("date", drop=False)

# Clean data
df = df[(df["value"] >= df["value"].quantile(0.025)) & (df["value"] <= df["value"].quantile(0.975))]


def draw_line_plot():
    # Draw line plot
    fig, axis = plt.subplots(1, 1)

    fig.set_figwidth(15)
    fig.set_figheight(5)

    plt.plot(df.index, df["value"], c="#CF0500", lw=.9)  # Set color, line width and antialiasing
    plt.title("Daily freeCodeCamp Forum Page Views 5/2016-12/2019")
    plt.xlabel("Date")
    plt.ylabel("Page Views")

    # Save image and return fig (don't change this part)
    fig.savefig('line_plot.png')
    return fig

def draw_bar_plot():
    # Copy and modify data for monthly bar plot
    # Inspired by https://matplotlib.org/3.1.1/gallery/lines_bars_and_markers/barchart.html
    # I wanted to fiddle around a bit with doing the plots manually rather than using Seaborn.

    months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October",
              "November", "December"]

    df_bar = df.copy()

    df_bar["year"] = pd.DatetimeIndex(df_bar["date"]).year
    df_bar["month"] = pd.DatetimeIndex(df_bar["date"]).month

    df_grouped = df_bar.groupby(["year", "month"]).mean().copy().reset_index()

    group_labels = pd.unique(df_bar["year"])

    means = list()

    for i in range(1, 13):
        means.append(list(df_grouped[(df_grouped["month"] == i)]["value"]))
        if len(means[i - 1]) < 4:
            means[i - 1].insert(0, 0)

    x = np.arange(len(group_labels))  # The year label locations
    width = 0.05  # The width of the bars

    fig, axis = plt.subplots(figsize=(10, 13 * (2 / 3)))

    rects = list()
    size_differential = -11

    for i in range(0, 12):
        rects.append(axis.bar(x + ((size_differential + (2 * i)) / 2) * width, means[i], width, label=months[i]))

    # Add some text for labels, title and custom x-axis tick labels, etc.
    axis.set_xlabel("Years", fontsize=14)
    axis.set_ylabel("Average Page Views", fontsize=14)
    axis.set_xticks(x)
    axis.set_xticklabels(group_labels, rotation=90, ha="center")
    axis.legend(title="Months", title_fontsize="x-large", fontsize="x-large")

    fig.tight_layout()

    # Save image and return fig (don't change this part)
    fig.savefig('bar_plot.png')
    return fig

def draw_box_plot():
    # After the last plot, I realised that not using seaborn was a mistake :)
    df_box = df.copy()

    df_box["year"] = pd.DatetimeIndex(df_box["date"]).year
    df_box["month"] = pd.DatetimeIndex(df_box["date"]).month
    short_months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    df_box["month_text"] = df_box["month"].map(lambda month: short_months[month - 1])

    # Draw box plots (using Seaborn)
    df_box = df_box.sort_values(by="month")

    fig, axis = plt.subplots(1, 2, figsize=(30, 10))
    yearwise = axis[0]
    monthwise = axis[1]

    yearwise = sns.boxplot(x=df_box.year, y=df_box.value, ax=yearwise)
    yearwise.set_title("Year-wise Box Plot (Trend)", fontsize="17")
    yearwise.set_xlabel("Year", fontsize="14")
    yearwise.set_ylabel("Page Views", fontsize="14")
    yearwise.tick_params(labelsize="14")

    monthwise = sns.boxplot(x="month_text", y="value", data=df_box, ax=monthwise)
    monthwise.set_title("Month-wise Box Plot (Seasonality)", fontsize="17")
    monthwise.set_xlabel("Month", fontsize="14")
    monthwise.set_ylabel("Page Views", fontsize="14")
    monthwise.tick_params(labelsize="14")

    # Save image and return fig (don't change this part)
    fig.savefig('box_plot.png')
    return fig
