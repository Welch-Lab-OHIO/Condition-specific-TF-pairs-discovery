
# coding: utf-8



import pandas as pd
import numpy as np
import sys

def comblist(f,b):
    f['class'] = 1.0
    b['class'] = -1.0
    f = pd.concat([f,back])
    return f

fore = pd.read_csv(sys.argv[1],index_col=0)
back = pd.read_csv(sys.argv[2],index_col=0)
comb = comblist(fore,back)

comb.to_csv(sys.argv[3]+'.csv') 
