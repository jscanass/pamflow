import pandas as pd
import glob
from utils import merge_annot_files

# Variables
path_annot = '../../../output/birdnet/detections/'
min_conf = 0.8
path_save_spmatrix = '../../../output/birdnet/birdnet_species_matrix_minconf0.8.csv'
path_save_spmatrix_site = '../../../output/birdnet/birdnet_site-species_matrix_minconf0.8.csv'

# Load data a format it as an abundance matrix with files rows
flist = glob.glob(f"{path_annot}/**/*.csv", recursive=True)
df = merge_annot_files(flist, rtype='csv')
df['Confidence'] = (df['Confidence'] >= min_conf).astype(int)
df_clean = df.loc[df.Confidence==1]

# Pivot table to get the desired structure
pivot_table = pd.pivot_table(
    df_clean, index='Fname', columns='Scientific name', 
    values='Confidence', aggfunc='sum', fill_value=0)

#pivot_table.reset_index(inplace=True)
pivot_table.to_csv(path_save_spmatrix)

# Format the table per site
pivot_table['sensor_name'] = pivot_table.index.str.split('_').str[0].values
pivot_table_site = pivot_table.groupby('sensor_name').sum()
pivot_table_site.to_csv(path_save_spmatrix_site)


# Plot species
import matplotlib.pyplot as plt
import seaborn as sns
plt_data = df_clean['Scientific name'].value_counts()
plt_data = plt_data.loc[plt_data>30]
fig, ax = plt.subplots(figsize=(8,15))
bars = ax.barh(plt_data.index, plt_data.values)
# Add text with values for each bar
for bar in bars:
    width = bar.get_width()
    ax.text(width, bar.get_y() + bar.get_height()/2, '{:d}'.format(int(width)),
            va='center', ha='left', fontsize=10)

ax.grid(axis='x', color='white')
plt.tight_layout()
sns.despine(trim=True)