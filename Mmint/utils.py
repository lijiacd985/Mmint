import pandas as pd
import numpy as np
from copy import deepcopy

def chip_transfer(data,axis=0):
    d=np.nan_to_num(data)
    #print('chip_transfer')
    return np.mean(d,axis=axis)

def meth_transfer(data,axis=0):
    # print(data)
    d = deepcopy(data)
    #print('meth_transfer')
    return np.nanmean(d,axis=axis)

def format_gz(filename,blocks,methy_marker):
    
    # What if the user need to visualize two different data types: 1. chip 2. methylation

    m = []
    file_data = []
    for fn in filename:
        if fn[-3:]=='.gz':
            fn=fn[:-3]
        d = pd.read_csv(fn,sep="\t",skiprows=1,header=None)
        region_title = d.values[:,:6]
        data = d.values[:,6:].astype(float)
        file_data.append(data)

    for i, marker in enumerate(methy_marker):
        if len(filename)==1:
            data = file_data[0]
            ind = i
        else:
            data = file_data[i]
            ind = 0
        inputdata = data[:,ind*blocks:(ind+1)*blocks]
        if methy_marker[i]:   
            m.append(meth_transfer(inputdata))
        else:
            m.append(chip_transfer(inputdata))
            
    m = np.vstack(m)
    return m
'''
    region_mean = []
    
    for i in range(data.shape[1]//blocks):
        print(i)
        d = data[:,i*blocks:(i+1)*blocks]
        region_mean.append(chip_transfer(d,axis=1).flatten())
    region_mean = np.array(region_mean).T
    #print(region_mean.shape)
    return m.reshape(snum,blocks),region_mean,region_title

def bp_format(filename,snum,blocks):
    d = pd.read_csv(filename,sep="\t",skiprows=1)
    data = d.values[:,6:].astype(float)
    #data = np.nan_to_num(data)
    result=[]
    for i in range(blocks):
        temp=[]
        for j in range(snum):
            arr=[]
            for d in data[:,j*blocks+i]:
               if ~np.isnan(d):
                   arr.append(d)
               #else:
               #    print('nan')
            temp.append(arr)
        result.append(temp)
    #result = np.array(result).reshape(blocks,snum,-1)
    return result

'''



if __name__=="__main__":
    import sys
    filename = sys.argv[1]
    print(format_gz(filename,2,True,True,30))
