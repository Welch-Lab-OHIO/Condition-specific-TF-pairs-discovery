import matplotlib.pyplot as plt
import matplotlib as mpl
import pandas as pd
import sys

# from upsetplot import plot
from upsetplot import UpSet, from_contents

"""
================================================================================
Fig4i_generate_upset_plots.py
Script written by: Michael Cooney

Date: July 15, 2025

This script generates an upset plot matrix showing the overlap of individual
features across conditions, derived from a 4-set Venn diagram of feature pairs
generated previously.

The input file feature_pair_spreadsheet should be formatted with set names as
columns and a list of feature-pairs listed under each set they belong to, e.g.:

WT   WTSD  S3   S3SD WT_WTSD ...
a_b  b_c   c_d  d_e  e_f     ...
f_g  g_h   h_i  i_j  j_k     ...
...  ...   ...  ...  ...

Member lists for each set can be different lengths, and may be empty.

Usage example:
>>> python Fig4i_generate_upset_plot.py feature_pair_spreadsheet output_folder output_file_name plot_label 

================================================================================
"""

mpl.rcParams['figure.dpi'] = 600

if __name__ == '__main__':
    if len(sys.argv) < 4:
        print('Not enough arguments', file=sys.stderr)
        print('Usage: python generate_upset_plots.py <input_file> <output_dir> <output_file_name>', \
              file=sys.stderr)

    threshold_tfs = pd.read_csv(sys.argv[1])
    if 'Unnamed: 0' in threshold_tfs.columns:
        threshold_tfs.set_index('Unnamed: 0', inplace=True)

    wt = set()
    wtsd = set()
    s3 = set()
    s3sd = set()

    data = {}
    label_data = {}
    
    for label in threshold_tfs.columns:
        label_data[label] = set()
        for i in threshold_tfs.loc[~threshold_tfs[label].isna(), label].values:
            # Modifying beta-catenin motif names so feature pairs can be split by an '_'
            a, b = i.replace('wt_motif1', 'ctnnb1-wt').replace('d4TCF_motif1', 'ctnnb1-d4TCF').split('_')

            # Record 'label' being associated with feature 'a'
            if a in data:
                data[a].add(label)
            else:
                data[a] = {label}

            # Record feature 'a' appearing in set 'label'
            label_data[label].add(a)

            # Record 'label' being associated with feature 'b'
            if b in data:
                data[b].add(label)
            else:
                data[b] = {label}

            # Record feature 'b' appearing in set 'label'
            label_data[label].add(b)

    label_data_sorted = {}
    # Sort data by length here because the upset plot library will do the same
    # and we need to match it later
    for i in sorted(label_data, key=lambda y: len(label_data[y])):
        if len(label_data[i]) == 0:
            continue
        label_data_sorted[i] = label_data[i]

    label_data = label_data_sorted
    del label_data_sorted

    # Black, turquoise, rust/brown, periwinkle, orange, blue, teal, yellow, pink
    color_list = ['#000000', '#03989e', '#a14242', '#6e57d2', '#5d782e', \
                  '#0099ff', '#e00a97', '#ffdf4f', '#d59890', '#bc8dbc', \
                  '#16a541', '#a97819', '#b91282', '#2920d7', '#ff8a22',]

    upset_data = from_contents(data)
    fig, ax = plt.subplots(ncols=1, nrows=1, figsize=(15, 5), layout='constrained')
    upset_plot = UpSet(upset_data, subset_size='count', orientation='vertical')

    # Style the legend labels
    for idx, category in enumerate(label_data):
        if len(label_data[category]) == 0:
            continue
        category_modified = category.replace('_', ' & ')
        upset_plot.style_subsets(\
                                 present=list(label_data[category]), \
                                 absent=(set(data) - label_data[category]), \
                                 facecolor=color_list[idx], \
                                 label=category_modified)

    upset_plot.plot_matrix(ax)

    print(f'Saving figure to {sys.argv[2]}/{sys.argv[3]}')
    plt.suptitle(sys.argv[4])
    plt.savefig(f'{sys.argv[2]}/{sys.argv[3]}')
    plt.show()
    
    print('Done')
