################################################################################
##
##  Author:  Michael Cooney
##  Purpose: Extract necessary window information from bedpe files to prepare
##            input for feature pair analysis pipeline
##
################################################################################

import pandas as pd
import sys

if __name__ == '__main__':
    if not len(sys.argv) == 5:
        print('Usage: bedpe_to_list.py <bedpe_file> <output_file> <condition_prefix> <z_score_threshold>')
        exit(-1)
    output_filename = sys.argv[2]
    condition_prefix = sys.argv[3]
    zscore_threshold = sys.argv[4]
    condition_zscore = f'{condition_prefix}_zscore'

    extracted_info = pd.read_csv(sys.argv[1], delim_whitespace='\t', usecols=['chrom_x', 'start_x', 'end_x', 'chrom_y', 'start_y', 'end_y', condition_zscore])
    extracted_info.loc[extracted_info[condition_zscore] >= float(zscore_threshold), 'windows_a'] = \
        (extracted_info['chrom_x'] + ':' + extracted_info['start_x'].map(str) + '-' + extracted_info['end_x'].map(str)).astype(str)
    extracted_info.loc[extracted_info[condition_zscore] < float(zscore_threshold), 'windows_a'] = 'drop'

    extracted_info.loc[extracted_info[condition_zscore] >= float(zscore_threshold), 'windows_b'] = \
        (extracted_info['chrom_y'] + ':' + extracted_info['start_y'].map(str) + '-' + extracted_info['end_y'].map(str)).astype(str)
    extracted_info.loc[extracted_info[condition_zscore] < float(zscore_threshold), 'windows_b'] = 'drop'

    extracted_info.drop(['chrom_x', 'start_x', 'end_x', 'chrom_y', 'start_y', 'end_y', condition_zscore], inplace=True, axis=1)

    # these two drop conditions should be the same, but just to be safe we're being redundant
    extracted_info.drop(extracted_info[extracted_info['windows_a'] == 'drop'].index, inplace=True)
    extracted_info.drop(extracted_info[extracted_info['windows_b'] == 'drop'].index, inplace=True)
    extracted_info.to_csv(output_filename, index=False, sep='\t', header=False)
    
