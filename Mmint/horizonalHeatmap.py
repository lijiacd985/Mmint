#!/usr/bin/env python

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import colors
from matplotlib.colors import ListedColormap
import os,sys
import subprocess
import argparse
from scipy import stats

'''
parser = argparse.ArgumentParser()
parser.add_argument('-bw','--bigwig',help="bigwig for the computeMatrix", nargs="*",metavar="FILE")
parser.add_argument('-bed','--bed',help="the regions to plot", metavar="FILE")
parser.add_argument('-after','--dnregions',help="downstream regions to plot",metavar="FILE")
parser.add_argument('-before','--upregions',help="upstream regions to plot",metavar="FILE")
parser.add_argument('-bs','--binsize',help="bins size to use", metavar="FILE")
parser.add_argument('-m','--scaleregion',help="scale the input bed regions to certain length(bp)",metavar="FILE")
parser.add_argument('-o','--outFile',help="output file name",nargs="*",metavar="FILE")
parser.add_argument('-L','--rowlabels',nargs="*",help="row labels for samples", metavar="FILE")
parser.add_argument('-n','--name',help="name for picture", metavar="FILE")
'''

#args.outFile should be *.gz!!!!!!!!!!!!!!!!!!!!!!!

def run(parser):
    args = parser.parse_args()
    out=[]
    for label in args.rowlabels:
        out.append(label+'.gz')

    ##need to install computeMatrix and add it to your ~/.bashrc file
    ##pass the python variables to subprocess

    subprocess.call("rm merge.ave.txt",shell=True)

    ##iterate multiple input files
    for i in range(len(args.bigwig)):

        subprocess.call("computeMatrix scale-regions -S %s -R %s -a %s -b %s -bs %s -m %s -o %s" % (args.bigwig[i],args.bed,args.dnregions,args.upregions,args.binsize,args.scaleregion, out[i]),shell=True)


    for i in range(len(args.bigwig)):
        subprocess.call("gunzip -f %s" % out[i], shell=True)

    for i in range(len(args.bigwig)):
        subprocess.call("sh format.sh %s" % out[i],shell=True)
        #subprocess.call("sh format.meth.sh %s" % outFile[i],shell=True)
    ##plot horizon heatmap
    dt = pd.read_table("merge.ave.txt",header=None)
    row_labels = [a for a in args.rowlabels]
    #
    array= dt.as_matrix(columns=dt.columns[0:])
    fig,ax = plt.subplots()
    cmap = plt.cm.get_cmap('YlOrRd')

    #cmap=ListedColormap('YlOrRd')
    #heatmap=ax.pcolor(stats.zscore(array,axis=1),cmap=cmap)
    heatmap=ax.pcolor(array,cmap=cmap,vmin=0,vmax=2)
    #cbar = plt.colorbar(heatmap)
    #cbar.ax.set_yticklabels(['0','1','2','3','4','5','6','7','8'])
    #heatmap.set_clim(vmin=-1,vmax=4)
    ax.set_yticks(np.arange(array.shape[0])+0.5, minor=False)
    ax.set_yticklabels(row_labels, minor=False)
    ax.set_xticks([0,int(args.upregions)/int(args.binsize),(int(args.upregions)+int(args.scaleregion))/int(args.binsize),(int(args.upregions)+int(args.scaleregion)+int(args.dnregions))/int(args.binsize)])
    #ax.set_xticklabels(['-'+str(int(args.upregions)/1000)+' kp','Start','END',str(int(args.dnregions)/1000)+' kb'])
    ax.set_xticklabels(['-'+str(int(args.upregions)/1)+' bp','Start','END',str(int(args.dnregions)/1)+' bp'])
    ax.set_xlim(0, array.shape[1])
    #ax.set_ylim(0,10)
    fig.colorbar(heatmap)
    ax.invert_yaxis()
    #plt.show()
    fig.savefig(str(args.name)+'.pdf')
    #fig.savefig("d01.Top5000.correlation.pdf")
    subprocess.call("rm merge.ave.txt",shell=True)
