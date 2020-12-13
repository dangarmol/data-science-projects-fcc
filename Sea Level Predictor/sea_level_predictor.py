import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import linregress

def draw_plot():
    # Read data from file
    df = pd.read_csv('epa-sea-level.csv')

    # Create first line of best fit
    slope1880, intercept1880, x, x, x = linregress(df["Year"], df["CSIRO Adjusted Sea Level"])
    # Create second line of best fit
    slope2000, intercept2000, x, x, x = linregress(df[df["Year"] >= 2000]["Year"],
                                                   df[df["Year"] >= 2000]["CSIRO Adjusted Sea Level"])

    # Add years until 2050
    real_data_limit = df["Year"].max()
    for i in range(real_data_limit - df["Year"].min(), 2050 - df["Year"].min() + 1):
        df.loc[i] = [i + df["Year"].min(), np.nan, np.nan, np.nan, np.nan]
    df["LinReg1880"] = intercept1880 + df["Year"].values * slope1880
    df["LinReg2000"] = intercept2000 + df["Year"].values * slope2000
    df.mask(df["CSIRO Adjusted Sea Level"] > real_data_limit)

    df2 = pd.DataFrame({
        "Since 1880": list(df["LinReg1880"].values),
        "Since 2000": list(df["LinReg2000"].values)
    }, index=list(df["Year"].values))

    # Thanks to: https://stackoverflow.com/questions/42948576/pandas-plot-does-not-overlay
    fig, ax = plt.subplots(figsize=(10, 10))
    # create shared y axes
    ax2 = ax.twiny()
    df2.plot(kind="line", ax=ax, color=['c', 'y'])
    df.plot(kind="scatter", x="Year", y="CSIRO Adjusted Sea Level", ax=ax2)
    # remove upper axis tick labels
    ax2.set_xticklabels([])
    # set the limits of the upper axis to match the lower axis ones
    ax2.set_xlim(df["Year"].min(), df["Year"].max())
    ax.set_title("Rise in Sea Level", fontsize="17")
    ax.set_xlabel("Year", fontsize="14")
    ax.set_ylabel("Sea Level (inches)", fontsize="14")
    ax2.set_xlabel(None)
    # plt.show()
    
    # Save plot and return data for testing (DO NOT MODIFY)
    plt.savefig('sea_level_plot.png')
    return plt.gca()