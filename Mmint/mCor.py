#!/usr/bin/python
import time
import numpy as np
import os,sys
import argparse
from io import StringIO
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
import itertools
import pandas as pd
from pandas.plotting import scatter_matrix
import pylab
from scipy import stats, integrate
import seaborn as sns
from .Format import formdata

def run(parser):
    
    args = parser.parse_args()

    if len(args.label)!=len(args.methfile):
        raise("The number of bed files and labels should be the same!")
    sns.set(color_codes=True)
    plt.style.use('ggplot')
    merge2 = pd.DataFrame(formdata(args.methfile,args.cov))
    #merge2.columns = [x for x in args.methfile]
    array2 = merge2.values.astype('float')
    #print(merge2.head())
    #array = merge2.as_matrix(columns=merge2.columns[0:])
    #array2=[[float(y) for y in x] for x in array]
    df = pd.DataFrame(array2, columns=args.label) # set the input file name as the column names
    #print(df.head())
    print((df.corr())) #calculate the correlation bewteen any two columns

#===============================New feature: correlationship heatmap=======================
    #labelname=[]
    #for name in args.methfile:
    #    labelname.append(name[name.rfind('/')+1:name.rfind('.')])
    #df.columns = labelname
    #labelnum=len(labelname)
    labelname, labelnum = args.label, len(args.label)
    col_max=df.corr().values
    plt.style.use('ggplot')
    fig = plt.figure()
    ax = plt.subplot()
    fig.subplots_adjust(left=0.15)
    hm=ax.pcolor(col_max,cmap=plt.cm.OrRd)
    plt.colorbar(hm)
    ax.set_xticks(np.arange(0,labelnum)+0.5)
    ax.set_yticks(np.arange(0,labelnum)+0.5)
    from decimal import Decimal
    for i in np.arange(0,labelnum):
        for j in np.arange(0,labelnum):
            plt.text(i+0.5,j+0.2,str(Decimal(str(col_max[i,j])).quantize(Decimal('0.00'))),ha='center', va='bottom')
    ax.xaxis.tick_bottom()
    ax.yaxis.tick_left()
    ax.set_xticklabels(labelname,minor=False,fontsize=20)
    ax.set_yticklabels(labelname,minor=False,fontsize=20)
    plt.savefig(args.output+'_heatmap.pdf')
#==========================================================================================

    g = sns.PairGrid(df)
    filename = 'df.'+str(time.time())+'.txt'    
    np.savetxt(filename,df)
    g.set(ylim=(0, 1))
    g.set(xlim=(0, 1))
    g.map_diag(plt.hist)
    g.map_offdiag(sns.kdeplot, cmap="OrRd", n_levels=20,shade=True,gridsize=int(args.gridsize))
    pylab.savefig(args.output+".pdf")
    os.system('rm '+filename)

if __name__=="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-m','--methfile',help="The output from mcall",nargs='*', metavar="FILE")
    parser.add_argument('-l','--label',help="Label for methylation files", nargs='*')
    parser.add_argument('-g','--gridsize',help="Size of grid in scatterplot.default=20.",default=20)
    parser.add_argument('-c','--cov',type=int,help="minimal coverage of cpg sites for every sample,default=0",default=0)
    parser.add_argument('-o','--output',help="The output file prefix.", metavar="FILE")
    run(parser)


