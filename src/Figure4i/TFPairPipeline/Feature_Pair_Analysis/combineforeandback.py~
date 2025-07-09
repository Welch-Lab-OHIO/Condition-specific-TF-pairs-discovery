
# coding: utf-8



import pandas as pd
import numpy as np
import sys

def comblist(f,b):
    f['class'] = 1.0
    b['class'] = -1.0
    f = f.append(back)
    return f

fore = pd.read_csv(sys.argv[1],index_col=0)
back = pd.read_csv(sys.argv[2],index_col=0)
comb = comblist(fore,back)

##generate train set and test set
#test = comb.sample(frac = 0.33,random_state=np.random.randint(10))
#train = comb.drop(test.index)
#train.to_csv('../data/train.csv')
#test.to_csv('../data/test.csv')
comb.to_csv(sys.argv[3]+'.csv') 
