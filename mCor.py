#!/usr/bin/python

import numpy as np
import os,sys
import argparse
from io import StringIO
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
import itertools
import pandas as pd
from pandas.tools.plotting import scatter_matrix
import pylab
from scipy import stats, integrate
import seaborn as sns
from Format import formdata
def run(parser):
    sns.set(color_codes=True)
    plt.style.use('ggplot')



    #parser = argparse.ArgumentParser()
    #parser.add_argument('-m','--methfile',help="The output from mcall",nargs='*', metavar="FILE")
    #parser.add_argument('-o','--output',help="The output file", metavar="FILE")

    args = parser.parse_args()
    #print args.methfile
    #print(reduce(print, args.methfile))
    #for n in args.methfile:
	#print (n)
    #df_list = [pd.read_table(f,header=None,names=['chr','start','end','ratio']) for f in args.methfile]
    #dfs = [f for f in args.methfile]
    #print df_list
    #dfs=[test3,test3,test1]
    #merge = pd.concat(df_list,axis = 1,join='inner')
    #merge = reduce(lambda x,y:formdata([x,y],args.cov), args.methfile)
    #print merge.ix[:,3:]#extract from the third column to the last column

    #merge.columns = [x for x in args.methfile]
    #merge.rename(columns= lambda x : for x in args.methfile, inplace=True)
    #print merge
    #merge.columns = ['chr', 'start', 'end','s1','s2','s3','s4']
    #merge2 = merge#.ix[:,3:]
    merge2 = pd.DataFrame(formdata(args.methfile,args.cov))
    merge2.columns = [x for x in args.methfile]
    array = merge2.as_matrix(columns=merge2.columns[0:])
    #array = merge.as_matrix(columns=merge.columns[3:])
    #print array
    array2=[[float(y) for y in x] for x in array]
    #print [[float(y) for y in x] for x in array]
    #df = pd.DataFrame(array2, columns=['T2', 'P2', 'P3'])
    df = pd.DataFrame(array2, columns=[f for f in args.methfile]) # set the input file name as the column names
    print (df.corr()) #calculate the correlation bewteen any two columns

#===============================New feature: correlationship heatmap=======================
    labelname=[]
    for name in args.methfile:
        labelname.append(name[name.rfind('/')+1:name.rfind('.')])
    df.columns = labelname
    labelnum=len(labelname)
    col_max=df.corr().values
    plt.style.use('ggplot')
    fig = plt.figure()
    ax = plt.subplot()
    fig.subplots_adjust(left=0.05)
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

    print (df.describe()) #output the basic statistics of each column
    #color = [[x for x in np.arange(0,1,0.1)] for y in np.arange(0,1,0.1)]
    #color =[[0.1,0.2,0.3],[0.1,0.2,0.3]]
    #pic = scatter_matrix(df,c=color,cmap='PuRd', alpha=0.2, figsize=(6, 6), diagonal='kde')
    g = sns.PairGrid(df)
    #g.map_diag(sns.kdeplot)
    np.savetxt('df.txt',df)
    g.set(ylim=(0, 1))
    g.set(xlim=(0,1))
    g.map_diag(plt.hist)
    #g = g.map(plt.scatter)
    #g.map_upper(plt.scatter,s=5)
    #g.map_lower(sns.kdeplot, cmap="Blues_d")
    g.map_offdiag(sns.kdeplot, cmap="OrRd", n_levels=20,shade=True)
    pylab.savefig(args.output+".png")


#usage: python *.py -m input1 input2 input3 ... -o Ratio-Cor
#input format: chr	start	end	methRatio

