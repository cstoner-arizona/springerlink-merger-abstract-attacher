"""
Simple merge script used append csv files from SpringerLink into an output.csv file.
Place in directory with csv files generated from SpringerLink then run with:
`python merge.py`

@author CStoner
@email cstoner@arizona.edu
"""

from functools import reduce
import pandas as pd
import os

# Config dir
csv_dir = os.path.dirname(os.path.realpath(__file__))
raw_dir_files = os.listdir(csv_dir)
csv_files = list()
csv_dfs = list()

for file in raw_dir_files:
    if file.endswith(".csv") and not file.startswith("output"):
        csv_files.append(file)

for file in csv_files:
    full_path = csv_dir + "/" + file
    df = pd.read_csv(full_path)
    csv_dfs.append(df)

df_raw_concat = pd.concat(csv_dfs)
df_filtered = df_raw_concat.sort_values('Item DOI', ascending=False).drop_duplicates('Item Title').drop_duplicates('Item DOI').drop_duplicates('URL').sort_index()
df_filtered = df_filtered[df_filtered["Content Type"] != 'Book']

df_raw_concat.to_csv('output_raw.csv', index=False)
df_filtered.to_csv('output.csv', index=False)