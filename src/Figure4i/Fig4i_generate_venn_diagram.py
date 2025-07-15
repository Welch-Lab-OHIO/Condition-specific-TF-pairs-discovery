import matplotlib.pyplot as plt
from matplotlib_venn import venn2, venn3
import matplotlib as mpl
import pandas as pd
import sys

mpl.rcParams['figure.dpi'] = 600

# Take input for 2 or 3 venn
# Take list of files
#   2, 3, or 7
# if 3:
#   generate venn diagram
#   if 7 inputs:
#     calculate significant p-values between each region
#       inputs 8, 9, 10, 11
#       take the intersection of the two/three regions being compared
#     set text on each region with corresponding overlap and number significant p-value
# if 2:
#   generate venn diagram
#   if 3 inputs:
#     calculate significant p-values in middle region
#       input 6
#     set text on middle region with overlap and number significant p-value


def get_intersection(*args: list[pd.DataFrame]) -> set[str]:
    # wt_vs_s3_s3sd_cols = list(set(wt_s3['Feature']).intersection(set(wt_s3sd['Feature'])).difference(set(total_intersection_cols)))
    # for arg in args
    #   remove features that are in both, and that are in all three

    if not len(args) >= 2:
        print('Cannot intersect a set with itself', file=sys.stderr)
        exit(-1)

    intersection_of_indices = set(args[0]).intersection(args[1])
    if len(args) > 2:
        intersection_of_indices &= set(args[2])

    return intersection_of_indices


def count_significant_p_values(file_path:str, features_to_use, alpha: float) -> int:
    comparison = pd.read_csv(file_path, index_col=0)
    comparison = comparison.loc[list(features_to_use), :]
    # return comparison[comparison['Fisher\'s Exact P-value'] <= alpha].shape[0]
    return comparison[round(comparison['Fisher\'s Exact P-value'], 3) <= alpha].shape[0]


def save_region(file_path: str, save_path, features_to_use: set, fg_label: str, alpha: float) -> None:
    """Read the one-vs-rest file (or input file), select features to use, save tf pairs with significant p-value"""
    print(features_to_use)
    print()
    print(len(features_to_use))
    print()    
    comparison = pd.read_csv(file_path, index_col=0)
    comparison = comparison.loc[list(features_to_use), :]
    # comparison.to_csv(f'{save_path}/{fg_label}_significant_region.csv')
    # save_path = '/'.join(file_path.split('/')[:-1])
    # comparison[comparison['Fisher\'s Exact P-value'] <= alpha].to_csv(f'../Output/240502/Pairwise/{fg_label}/{fg_label}_Specific/{fg_label}_significant_region.csv')

    comparison[round(comparison['Fisher\'s Exact P-value'], 3) <= alpha].to_csv(f'{save_path}/{fg_label}_significant_region.csv')

    # print(comparison[comparison['Fisher\'s Exact P-value'] <= alpha])
    # comparison[comparison['Fisher\'s Exact P-value'] <= alpha].to_csv(f'{save_path}/{fg_label}_significant_region.csv')
    

if __name__ == '__main__':

    # significant p-value 
    # alpha = 4.2677581998012655e-08
    # alpha = 5.0548315484214585e-12
    # alpha = 0.05
    alpha = float(sys.argv[13])
    alpha_0 = 0.05

    arglen = len(sys.argv)
    if arglen < 2:
        # print('Not enough arguments', file=sys.stderr)
        print('Help: Input should be one of the following')
        print('generate_venn_diagram.py 3 label_1 label_2 label_3 file_1 file_2 file_3 comparison_1_2 comparison_2_3 comparison_1_3 comparison_1_2_3 output_dir')
        print('generate_venn_diagram.py 3 label_1 label_2 label_3 file_1 file_2 file_3 output_dir')
        print('generate_venn_diagram.py 2 label_1 label_2 file_1 file_2 comparison_1_2 output_dir')
        print('generate_venn_diagram.py 2 label_1 label_2 file_1 file_2 output_dir')
        exit(-1)

    # two or three comparisons 
    venn_type = int(sys.argv[1])
    foreground_label = sys.argv[2].split('_')[0].upper()

    # if venn_type == 2:
    #     if arglen != 7 and arglen != 8:
    #         print(f'Not enough arguments for 2 comparisons. This script requires either 7 or 8 inputs, you gave {arglen}', file=sys.stderr)
    #         exit(-1)

    #     cond1 = pd.read_csv(sys.argv[4], index_col=0)
    #     cond2 = pd.read_csv(sys.argv[5], index_col=0)

    #     cond1 = cond1[cond1['Fisher\'s Exact P-value'] <= alpha]
    #     cond2 = cond2[cond2['Fisher\'s Exact P-value'] <= alpha]

    #     figure = venn2([set(cond1.index), set(cond2.index)], (sys.argv[2], sys.argv[3]))

    #     if arglen == 8:
    #         cond1_2 = get_intersection(cond1.index, cond2.index)
    #         sig_p_value_count = count_significant_p_values(sys.argv[6], cond1_2, alpha)
    #         figure.get_label_by_id('11').set_text(f'{len(cond1_2)}\n{sig_p_value_count} <= alpha')
    #         plt.savefig(f'{sys.argv[7]}/{sys.argv[2]}_vs_{sys.argv[3]}_venn.png')

    #     else:
    #         plt.savefig(f'{sys.argv[6]}/{sys.argv[2]}_vs_{sys.argv[3]}_venn.png')

    # elif venn_type == 3:
    if venn_type == 3:
        if arglen != 10 and arglen != 14:
            print(f'Not enough arguments for 3 comparisons. This script requires either 9 or 13 inputs, you gave {arglen}', file=sys.stderr)
            exit(-1)

        cond1 = pd.read_csv(sys.argv[5], index_col=0)
        cond2 = pd.read_csv(sys.argv[6], index_col=0)
        cond3 = pd.read_csv(sys.argv[7], index_col=0)

        cond1 = cond1[cond1['Fisher\'s Exact P-value'] <= alpha_0]
        cond2 = cond2[cond2['Fisher\'s Exact P-value'] <= alpha_0]
        cond3 = cond3[cond3['Fisher\'s Exact P-value'] <= alpha_0]
        
        figure = venn3([set(cond1.index), set(cond2.index), set(cond3.index)], (sys.argv[2], sys.argv[3], sys.argv[4]))
        
        if arglen == 14:
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
            # figure.get_label_by_id('011').set_text(f'\n{len(cond2_3)}\n{sig_p_value_counts[1]} <= {alpha:0.3e}')
            # figure.get_label_by_id('101').set_text(f'\n{len(cond1_3)}\n{sig_p_value_counts[2]} <= {alpha:0.3e}')
            figure.get_label_by_id('011').set_text(f'\n{len(cond2_3)}\n{sig_p_value_counts[1]} <= {alpha:0.3e}')
            figure.get_label_by_id('101').set_text(f'\n{len(cond1_3)}\n{sig_p_value_counts[2]} <= {alpha:0.3e}')
            figure.get_label_by_id('111').set_text(f'{len(cond1_2_3)}\n{sig_p_value_counts[3]} <= {alpha:0.3e}')

            # figure.get_label_by_id('110').set_text(f'{len(cond1_2)}')
            # figure.get_label_by_id('011').set_text(f'{len(cond2_3)}')
            # figure.get_label_by_id('101').set_text(f'{len(cond1_3)}')
            # figure.get_label_by_id('111').set_text(f'{len(cond1_2_3)}')


            plt.savefig(f'{sys.argv[12]}/{sys.argv[2]}_vs_{sys.argv[3]}_vs_{sys.argv[4]}_venn.pdf')
        else:
            plt.savefig(f'{sys.argv[8]}/{sys.argv[2]}_vs_{sys.argv[3]}_vs_{sys.argv[4]}_venn.pdf')

    else:
        print('Venn diagram type must be either two or three comparisons\nPlease try again', file=sys.stderr)
