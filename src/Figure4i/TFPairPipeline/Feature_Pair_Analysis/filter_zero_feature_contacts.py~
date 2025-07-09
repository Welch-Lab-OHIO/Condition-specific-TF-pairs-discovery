import pandas as pd
import sys

df = pd.read_csv(sys.argv[1],index_col=0)
df = df[(df.T != 0).any()]

out = sys.argv[1].strip('csv')+'filter_zero_feature_contacts.csv'

df.to_csv(out)
#print(fore.T.describe())
