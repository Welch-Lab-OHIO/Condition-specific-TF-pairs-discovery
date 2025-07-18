import matplotlib.pyplot as plt
from matplotlib_venn import venn2, venn3
import matplotlib as mpl
import pandas as pd
import sys

"""
================================================================================
FigS10b_generate_venn_diagram.py
Script written by: Michael Cooney

Date: July 15, 2025

Extract condition-specific discriminatory TF pairs in three
condition-condition comparisons

This script generates a 3-set Venn diagram and a spreadsheet of significant
feature pairs using lists of feature pairs and associated p-values.  

Usage examples:
>>> python FigS10b_generate_venn_diagram.py alpha label_1 label_2 label_3 file_1 file_2 file_3 comparison_1_2 comparison_2_3 comparison_1_3 comparison_1_2_3 output_dir

>>> python FigS10b_generate_venn_diagram.py 0.001 WT_WTSD WT_S3 WT_S3SD WT_vs_WTSD.csv WT_vs_S3.csv WT_vs_S3SD.csv WT_vs_WTSD_S3.csv WT_vs_S3_S3SD.csv WT_vs_WTSD_S3SD.csv WT_vs_WTSD_S3_S3SD.csv ./

================================================================================
"""
mpl.rcParams['figure.dpi'] = 600

def get_intersection(*args: list[pd.DataFrame]) -> set[str]:
    # Get the intersection of two or three sets of feature pairs
    if not len(args) >= 2:
        print('Cannot intersect a set with itself', file=sys.stderr)
        exit(-1)

    intersection_of_indices = set(args[0]).intersection(args[1])

    # Check if there is a third set to be intersected
    if len(args) > 2:
        intersection_of_indices &= set(args[2])

    return intersection_of_indices


def count_significant_p_values(file_path:str, features_to_use, alpha: float) -> int:
    # Report how many of the feature pairs in an intersection have a significant p-value
    comparison = pd.read_csv(file_path, index_col=0)
    comparison = comparison.loc[list(features_to_use), :]
    return comparison[round(comparison['Fisher\'s Exact P-value'], 3) <= alpha].shape[0]


def save_region(file_path: str, save_path, features_to_use: set, fg_label: str, alpha: float) -> None:
    # Read the one-vs-rest file, select features to use, save tf pairs with significant p-value
    comparison = pd.read_csv(file_path, index_col=0)
    comparison = comparison.loc[list(features_to_use), :]
    comparison[round(comparison['Fisher\'s Exact P-value'], 3) <= alpha].to_csv(f'{save_path}/{fg_label}_significant_region.csv')

    

if __name__ == '__main__':
    arglen = len(sys.argv)
    if arglen < 13:
        print('Error: not enough arguments', file=sys.stderr)
        print('Usage: Fig4i_generate_venn_diagram.py alpha label_1 label_2 label_3 file_1 file_2 file_3 comparison_1_2 comparison_2_3 comparison_1_3 comparison_1_2_3 output_dir', file=sys.stderr)
        exit(-1)

    # This alpha will be used in the one-vs-all comparison
    alpha = float(sys.argv[1])
    alpha_0 = 0.05

    # Of the form condition1_condition2; will be used to label Venn diagram regions
    foreground_label = sys.argv[2].split('_')[0].upper()

    cond1 = pd.read_csv(sys.argv[5], index_col=0)
    cond2 = pd.read_csv(sys.argv[6], index_col=0)
    cond3 = pd.read_csv(sys.argv[7], index_col=0)
    
    cond1 = cond1[cond1['Fisher\'s Exact P-value'] <= alpha_0]
    cond2 = cond2[cond2['Fisher\'s Exact P-value'] <= alpha_0]
    cond3 = cond3[cond3['Fisher\'s Exact P-value'] <= alpha_0]
    
    figure = venn3([set(cond1.index), set(cond2.index), set(cond3.index)], (sys.argv[2], sys.argv[3], sys.argv[4]))

    cond1_2_3 = get_intersection(cond1.index, cond2.index, cond3.index)
    cond1_2 = get_intersection(cond1.index, cond2.index).difference(cond1_2_3)
    cond2_3 = get_intersection(cond2.index, cond3.index).difference(cond1_2_3)
    cond1_3 = get_intersection(cond1.index, cond3.index).difference(cond1_2_3)
    intersections = [cond1_2, cond2_3, cond1_3, cond1_2_3]
    
    save_region(sys.argv[11], sys.argv[12], cond1_2_3, foreground_label, alpha)
    
    sig_p_value_counts = []
    for i in range(8, 12):
        sig_p_value_counts.append(count_significant_p_values(sys.argv[i], intersections[i-8], alpha))
        
    figure.get_label_by_id('110').set_text(f'{len(cond1_2)}\n{sig_p_value_counts[0]} <= {alpha:0.3e}')
    figure.get_label_by_id('011').set_text(f'\n{len(cond2_3)}\n{sig_p_value_counts[1]} <= {alpha:0.3e}')
    figure.get_label_by_id('101').set_text(f'\n{len(cond1_3)}\n{sig_p_value_counts[2]} <= {alpha:0.3e}')
    figure.get_label_by_id('111').set_text(f'{len(cond1_2_3)}\n{sig_p_value_counts[3]} <= {alpha:0.3e}')
    
    plt.savefig(f'{sys.argv[12]}/{sys.argv[2]}_vs_{sys.argv[3]}_vs_{sys.argv[4]}_venn.pdf')
