import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# 1
df = pd.read_csv('medical_examination.csv')

# 2
bmi = df['weight'] / ((df['height'] / 100) ** 2)
df['overweight'] = np.where(bmi > 25, 1, 0)

# 3
df['cholesterol'] = np.where(df['cholesterol'] == 1, 0, 1)
df['gluc'] = np.where(df['gluc'] == 1, 0, 1)

# 4
def draw_cat_plot():
    # 5 Unpivot the dataframe from wide to long format with id column cardio
    df_cat = pd.melt(df, id_vars={'cardio'}, value_vars=['cholesterol', 'gluc', 'smoke', 'alco', 'active', 'overweight'])

    # 6 Group by cardio and get the value counts for each feature; sort by features and their values
    df_cat = df_cat.groupby('cardio', as_index=False).value_counts().sort_values(by=['variable', 'value'])
    df_cat.rename(columns={'count':'total'}, inplace=True)

    # 7
    chart = sns.catplot(data=df_cat, x='variable', y='total', kind='bar', hue='value', col='cardio')

    # 8
    fig = chart.figure

    # 9
    fig.savefig('catplot.png')
    return fig


# 10
def draw_heat_map():
    # 11 Clean the data
    df_heat = df[(df['ap_lo'] <= df['ap_hi']) & \
            (df['height'] >= df['height'].quantile(0.025)) & (df['height'] <= df['height'].quantile(0.975)) & \
            (df['weight'] >= df['weight'].quantile(0.025)) & (df['weight'] <= df['weight'].quantile(0.975))]

    # 12 Correlation Matrix
    corr = df_heat.corr()

    # 13 Mask for upper triangel of corr
    mask = np.zeros(corr.shape)
    for i in range(corr.shape[0]):
        for j in range(corr.shape[1]):
            mask[i][j] = 1 if j >= i else 0

    # 14
    fig, ax = plt.subplots(dpi=200)

    # 15
    sns.set_context("paper", font_scale=0.6, rc={'font.size': 6, 'xtick.major.size': 2,'ytick.major.size': 2})
    sns.heatmap(corr, vmin=-0.08, vmax=0.24, center=0, square=True, mask=mask, annot=True, fmt='.1f', linewidth=0.5, ax=ax)

    # 16
    fig.savefig('heatmap.png')
    return fig
