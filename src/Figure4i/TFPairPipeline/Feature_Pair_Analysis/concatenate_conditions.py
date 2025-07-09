import pandas as pd
import sys

# this script does not check for overlapping contacts between conditions
# this was checked for manually in the 240327 *.filt.csv data
# you should probably check you data before using this script

if __name__ == '__main__':
    if len(sys.argv) < 4:
        print('Not enough arguments', file=sys.stderr)
        exit(-1)

    print('Reading files')
    cond1 = pd.read_csv(sys.argv[1], index_col=0)
    cond2 = pd.read_csv(sys.argv[1], index_col=0)

    print('Concatenating and writing')
    pd.concat([cond1,cond2]).to_csv(sys.argv[3])

    print('Finished')
