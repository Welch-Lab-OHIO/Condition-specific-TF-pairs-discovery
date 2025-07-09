import pandas as pd
import sys
import re
if not len(sys.argv) == 3:
    print("extract_windows.py <file_to_extract> <output_file>")
    exit(-1)
def get_start_loc(name, index):
    return re.split('[:-]', name)[index]
out_filename = sys.argv[2]
print(f'FILE: {sys.argv[1]}')
# df = pd.read_csv(sys.argv[1], delim_whitespace="\t", names=["window1", "window2"])
df = pd.read_csv(sys.argv[1], sep='\t', names=['window1', 'window2'])
print(f'DF: {df}')
windows = pd.concat([df['window1'],df['window2']], axis=0, ignore_index=True)
print("Contact List Size: ", df.shape[0])

# this math is not entirely accurate right?  Because if a window x appears in
# window1 and window2, then it will be counted twice, but in unique_windows
# it will only appear once - Michael
print("Unique from window 1 list: ", len(df['window1'].unique()))
print("Unique from window 2 list: ", len(df['window2'].unique()))
unique_windows = windows.unique()
print("Total Joint Unique Windows: ",len(unique_windows))
output_df = pd.DataFrame(unique_windows, columns=["locus"])
output_df["chr"] = output_df.apply(lambda row: get_start_loc(row["locus"],0),axis=1)
output_df["start"] = output_df.apply(lambda row: int(get_start_loc(row["locus"],1)),axis=1)
output_df["stop"] = output_df.apply(lambda row: int(get_start_loc(row["locus"],2)),axis=1)
output_df = output_df[["chr","start", "stop","locus"]][:]
output_df = output_df.sort_values(by=["chr", "start"])
print(output_df)
output_df.to_csv(out_filename, index=False, sep = '\t', header=False)
