import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# Import data
df = pd.read_csv("https://raw.githubusercontent.com/freeCodeCamp/boilerplate-medical-data-visualizer/master/medical_examination.csv")

# Add 'overweight' column
df["overweight"] = (df["weight"] / ((df["height"] / 100) ** 2) > 25).astype(int)

# Normalize data by making 0 always good and 1 always bad. If the value of 'cholestorol' or 'gluc' is 1, make the value 0. If the value is more than 1, make the value 1.
df["cholesterol"] = (df["cholesterol"] > 1).astype(int)
df["gluc"] = (df["gluc"] > 1).astype(int)

# Draw Categorical Plot
def draw_cat_plot():
    # Create DataFrame for cat plot using `pd.melt` using just the values from 'cholesterol', 'gluc', 'smoke', 'alco', 'active', and 'overweight'.
    long_df = pd.melt(df, id_vars=["cardio"], value_vars=["active", "alco", "cholesterol", "gluc", "overweight", "smoke"])

    # Draw the catplot with 'sns.catplot()'
    fig = sns.catplot(data=long_df, kind="count", x="variable", hue="value", col="cardio")

    # Do not modify the next two lines
    fig.savefig('catplot.png')
    return fig


# Draw Heat Map
def draw_heat_map():
    # Clean the data
    df_heat = df.copy()
    df_heat = df_heat[df_heat["ap_lo"] <= df_heat["ap_hi"]]
    df_heat = df_heat[df_heat["height"] >= df_heat["height"].quantile(0.025)]
    df_heat = df_heat[df_heat["height"] <= df_heat["height"].quantile(0.975)]
    df_heat = df_heat[df_heat["weight"] >= df_heat["weight"].quantile(0.025)]
    df_heat = df_heat[df_heat["weight"] <= df_heat["weight"].quantile(0.975)]

    # Inspired by https://seaborn.pydata.org/examples/many_pairwise_correlations.html example
    corr = df_heat.corr()

    # Generate a mask for the upper triangle
    mask = np.triu(np.ones_like(corr, dtype=bool))

    # Set up the matplotlib figure
    fig, ax = plt.subplots(figsize=(11, 9))

    # Draw the heatmap with the mask and correct aspect ratio
    ax = sns.heatmap(corr, mask=mask, vmax=.3, center=0, square=True, linewidths=.5, cbar_kws={"shrink": .5}, annot=True, fmt=".1f")

    # Do not modify the next two lines
    fig.savefig('heatmap.png')
    return fig
