import sys
import pandas as pd

if len(sys.argv) != 3:
    print("Form: fix_column_orientation.py file1 file2")
    exit(-1)

file1 = pd.read_csv(sys.argv[1])
file2 = pd.read_csv(sys.argv[2])
order1 = file1.columns.sort_values()
order2 = file2.columns.sort_values()
intersect = order1.intersection(order2)
file1 = file1[intersect]
file2 = file2[intersect]
file1.to_csv(sys.argv[1], index=False)
file2.to_csv(sys.argv[2], index=False)

