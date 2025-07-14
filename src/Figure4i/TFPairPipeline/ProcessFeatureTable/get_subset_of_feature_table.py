"""
====================================================================================================================
Python script name get_subset_of_feature_table.py
Script written by Michael Cooney, Liam Speakman

Date: July 14, 2025

This script takes in a TF feature table(TF x Window) and selects only TFs from a specified list

Usage example:
>>> python3 get_subset_of_feature_table.py sd.dataset.tfs.csv TF_list.csv sd.dataset_selected.csv

=====================================================================================================================
"""
import pandas as pd
import sys

feature_table = pd.read_csv(sys.argv[1])
selected_tfs = sorted(list(set(pd.read_csv(sys.argv[2])['feature'].to_list())))

def get_set_in_df(tf_list, df):
    selection = []
    for tf in tf_list:
        if tf in df.columns:
            selection.append(tf)
    return selection
tfs_in_file = get_set_in_df(selected_tfs, feature_table)

print("# of TF list:", len(tfs_in_file), "out of", len(selected_tfs))
print('Missing tfs: ')
print(set(selected_tfs) - set(tfs_in_file))
tfs_in_file.insert(0,"name")
feature_table[tfs_in_file].to_csv(sys.argv[3], index=False)