import pandas as pd
import sys

# use sum(axis=1) instead of taking transpose
# use to_csv(mode='a', header=False) to write to the csv
# use read_csv(skiprows, nrows) in a generator function to read csv



# def get_rows(file):
#      ...:     start=0
#      ...:     end=2
#      ...:     with open(file) as f:
#      ...:         while True:
#      ...:             data = f.readline()
#      ...:             if not data:
#      ...:                 break
#      ...:             data = data.split(',')
#      ...:             yield data
#      ...:             start = end
#      ...:             end += 2


# for i in get_rows('240222/Output/intermediate_output/S3_contacts.feature_pair.csv'):
#      ...:     if counter == 0:
#      ...:         counter += 1
#      ...:         continue
#      ...:     else:
#      ...:         i = list(map(int, i[1:]))
#      ...:         print(any(i))



 # counter = 0
 #     ...: with open('testing3.csv', mode='w') as out:
 #     ...:     for i in get_rows('testing.csv'):
 #     ...:         if counter == 0:
 #     ...:             counter += 1
 #     ...:             out.write(','.join(i))
 #     ...:             continue
 #     ...:         else:
 #     ...:             if any(list(map(int, i[1:]))):
 #     ...:                 out.write(','.join(i))


def csv_generator(file_path):
    with open(file_path) as f:
        while True:
            data = f.readline()
            if not data:
                break
            data = data.split(',')
            yield data
    f.close()


out_file = sys.argv[1].strip('csv')+'filter_zero_feature_contacts.csv'

counter = 0
with open(out_file, mode='w') as out:
    for line in csv_generator(sys.argv[1]):
        if counter == 0:
            # write columns to csv
            out.write(','.join(line))
            counter += 1
            continue
        else:
            # line_data = list(map(int, line[1:]))
            if any(map(int, line[1:])):
                out.write(','.join(line))
                # write line to csv

out.close()
# df = pd.read_csv(sys.argv[1],index_col=0)
# df = df[(df.T != 0).any()]

# out = sys.argv[1].strip('csv')+'filter_zero_feature_contacts.csv'

# df.to_csv(out)
# #print(fore.T.describe())
