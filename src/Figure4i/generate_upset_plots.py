import matplotlib.pyplot as plt
import matplotlib as mpl
import pandas as pd
import sys
# from upsetplot import plot
from upsetplot import UpSet, from_contents

mpl.rcParams['figure.dpi'] = 600

if __name__ == '__main__':
    # input: tf pairs file path,
    #        output file directory
    #        output file name

    # plan:
    # set for each condition
    # for each condition,
    #   split values by the '_', store in a set at that condition
    # create a dictionary with the conditions as keys, and sets as values
    # plot values on plot

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
            a, b = i.replace('wt_motif1', 'ctnnb1-wt').replace('d4TCF_motif1', 'ctnnb1-d4TCF').split('_')

            if a in data:
                data[a].add(label)
            else:
                data[a] = {label}
            label_data[label].add(a)

            if b in data:
                data[b].add(label)
            else:
                data[b] = {label}
            label_data[label].add(b)

    print(data)
    print(len(data))

    label_data_sorted = {}
    for i in sorted(label_data, key=lambda y: len(label_data[y])):
        if len(label_data[i]) == 0:
            continue
        label_data_sorted[i] = label_data[i]

    label_data = label_data_sorted
    del label_data_sorted

    # black, turquoise, rust/brown, periwinkle, orange, blue, teal, yellow, pink
    color_list = ['#000000', '#03989e', '#a14242', '#6e57d2', '#5d782e', \
                  '#0099ff', '#e00a97', '#ffdf4f', '#d59890', '#bc8dbc', \
                  '#16a541', '#a97819', '#b91282', '#2920d7', '#ff8a22',]

    # condition_list = []

    upset_data = from_contents(data)
    # upset_plot = UpSet(data, subset_size='count', orientation='vertical').plot()
    # upset_plot, ax = UpSet(data, subset_size='count', orientation='vertical')
    fig, ax = plt.subplots(ncols=1, nrows=1, figsize=(15, 5), layout='constrained')
    upset_plot = UpSet(upset_data, subset_size='count', orientation='vertical')

    print('--------------------------------------------------------------------------------')

    for idx, category in enumerate(label_data):
        if len(label_data[category]) == 0:
            continue
        category_modified = category.replace('_', ' & ')
        print(idx, color_list[idx], category)
        upset_plot.style_subsets(\
                                 present=list(label_data[category]), \
                                 absent=(set(data) - label_data[category]), \
                                 facecolor=color_list[idx], \
                                 label=category_modified)
        # condition_list.append(category)

    # upset_plot.plot(fig)
    upset_plot.plot_matrix(ax)
    # fig.legend(condition_list)

    print(f'Saving figure to {sys.argv[2]}/{sys.argv[3]}')
    plt.suptitle(sys.argv[4])
    plt.savefig(f'{sys.argv[2]}/{sys.argv[3]}')
    plt.show()
    
    print('Done')



    # for i in threshold_tfs.loc[~threshold_tfs['WT'].isna(), 'WT'].values:
    #     a, b = i.split('_')
    #     if a in data:
    #         data[a].add('WT')
    #     else:
    #         data[a] = {'WT'}

    #     if b in data:
    #         data[b].add('WT')
    #     else:
    #         data[b] = {'WT'}

    #     # wt.add(a)
    #     # wt.add(b)

    # for i in threshold_tfs.loc[~threshold_tfs['WTSD'].isna(), 'WTSD'].values:
    #     a, b = i.split('_')
    #     if a in data:
    #         data[a].add('WTSD')
    #     else:
    #         data[a] = {'WTSD'}

    #     if b in data:
    #         data[b].add('WTSD')
    #     else:
    #         data[b] = {'WTSD'}

    #     # wtsd.add(a)
    #     # wtsd.add(b)

    # for i in threshold_tfs.loc[~threshold_tfs['S3'].isna(), 'S3'].values:
    #     a, b = i.split('_')
    #     if a in data:
    #         data[a].add('S3')
    #     else:
    #         data[a] = {'S3'}

    #     if b in data:
    #         data[b].add('S3')
    #     else:
    #         data[b] = {'S3'}

    #     # s3.add(a)
    #     # s3.add(b)

    # for i in threshold_tfs.loc[~threshold_tfs['S3SD'].isna(), 'S3SD'].values:
    #     a, b = i.split('_')
    #     if a in data:
    #         data[a].add('S3SD')
    #     else:
    #         data[a] = {'S3SD'}

    #     if b in data:
    #         data[b].add('S3SD')
    #     else:
    #         data[b] = {'S3SD'}

    #     # s3sd.add(a)
    #     # s3sd.add(b)


    # print(data)
    # print(len(data))
    # # data = from_contents({'WT': wt, 'WTSD': wtsd, 'S3': s3, 'S3SD': s3sd})
    # data = from_contents(data)
    # print(data)
    # upset_plot = UpSet(data, subset_size='count', orientation='vertical').plot()

    # print(f'Saving figure to {sys.argv[2]}/{sys.argv[3]}')
    # plt.title(sys.argv[4])
    # plt.savefig(f'{sys.argv[2]}/{sys.argv[3]}')
    # plt.show()
    
    # print('Done')
    
    
        
