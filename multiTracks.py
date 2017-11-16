#!/usr/bin/env python

import numpy as np
import os,sys
import argparse
import subprocess
from io import StringIO
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
import itertools
import pandas as pd
plt.style.use('ggplot')
from collections import defaultdict
import scipy
from scipy.interpolate import spline
import matplotlib.ticker as ticker
from pylab import *


'''
parser = argparse.ArgumentParser()
parser.add_argument('-b','--bigwig',help="input file (bw format)",nargs="*", metavar="FILE")
parser.add_argument('-labels','--labels',help="labels for the input files",nargs="*", metavar="FILE")
parser.add_argument('-c','--color',help="colors for the input file tracks",nargs="*", metavar="FILE")
parser.add_argument('-bs','--binsize',help="bins size",metavar="FILE")
parser.add_argument('-out','--out',help="output",nargs="*",metavar="FILE")
parser.add_argument('-outRawCounts','--RawCounts',help="Raw counts output",nargs="*",metavar="FILE")
parser.add_argument('-r','--regions',help="regions to plot",metavar="FILE")
parser.add_argument('-f','--file',help="file include all the regions to plot",metavar="FILE")
parser.add_argument('-M','--meth',help="If bw file is methylation file, use -M.",action="store_true")
'''
def run(parser):
    args = parser.parse_args()
    print args.bigwig
    print args.file
    FILE = open(args.file,'r')
    array1 = []
    array2 = []
    ymax=[]
    out=[]
    RawCounts=[]
    for label in args.labels:
        out.append(label+'.npz')
        RawCounts.append(label+'.tab')
    for line in FILE:
        line=line.strip().split('\t')
        chr,start,end = line[0].split(':')
        start = str(int(start)-args.upstream)
        end = str(int(end)+args.downstream)
        array1.append(chr+':'+start+':'+end)
        array2.append(line[1])
    for k in range(len(array1)):
        for i in range(len(args.bigwig)):
            subprocess.call("multiBigwigSummary bins -bs %s -r %s -b %s --labels %s -out %s --outRawCounts %s" % (args.binsize, array1[k],args.bigwig[i],args.labels[i],out[i],RawCounts[i]),shell=True)
        for i in range(len(args.bigwig)):
    	    subprocess.call("sed -i 's/nan/0/g' %s" % RawCounts[i], shell=True)
        for i in range(len(args.bigwig)):
            subprocess.call("sh format.shareX.sh %s" % RawCounts[i],shell=True)
        dt = pd.read_table("merge.clean",header=1)
        x_sub_flat = dt.as_matrix(columns=dt.columns[2:3])
        print 'A'
        x_trans = map(list,zip(*x_sub_flat))
        
        y_sub = [a for a in dt.as_matrix(columns = dt.columns[3:dt.shape[1]])]
        y_trans = map(list,zip(*y_sub))
        plt.close('all')
        x_smooth = np.linspace(min(x_trans[0]), max(x_trans[0]), 1000)
        y_smooth=[]
        print len(y_trans)
        for i in range(len(y_trans)):
            y_smooth.append(spline(x_trans[0], y_trans[i], x_smooth))
            ymax.append(max(y_trans[i]))
        fig,ax1 = plt.subplots(figsize=(15,10))

        mmax=np.zeros(len(args.labels)//args.replicate)
        for i in range(len(args.labels)//args.replicate):
            for j in range(args.replicate):
                mmax[i] = max(mmax[i],np.max(y_smooth[i*args.replicate+j]))
        print mmax
        for i,v in enumerate(xrange(len(y_trans))):
            
            v=v+1
            ax1 = subplot(len(y_trans),1,v)
            ax1.plot(x_smooth,y_smooth[i],color='white',linewidth=0.1)
            print i,v
            if args.meth:
                ax1.set_ylim(0,1.1)
            else:
                ax1.set_ylim(0,mmax[i//args.replicate])
            plt.ylabel(args.labels[i],rotation=90,fontsize=12)
            plt.axvline(x_trans[0][0]+args.upstream,color='red',linewidth=2,linestyle='dashed')
            plt.axvline(x_trans[0][-1]-args.downstream,color='red',linewidth=2,linestyle='dashed')
            d = scipy.zeros(1000)
            ax1.fill_between(x_smooth,y_smooth[i],where=y_smooth[i]>=d,interpolate=True,color=args.color[i])
            ax1.spines['top'].set_visible(False)
            ax1.spines['right'].set_visible(False)
            ax1.spines['bottom'].set_visible(False)
            #ax1.set_ylim(0,max(ymax))
            ax1.yaxis.set_major_formatter(ticker.FormatStrFormatter('%0.1f'))
            ax1.yaxis.set_ticks_position('left')
            ax1.xaxis.set_ticks_position('none')
            subplots_adjust(hspace=0.05)
            plt.setp(ax1.get_xticklabels(), visible=False)
        plt.setp(ax1.get_xticklabels(), visible=True)
        plt.xlabel(array2[k]+" "+str(array1[k]))
        ymax=[]
        fig.savefig(str(array2[k])+'.pdf')



if __name__=="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-b','--bigwig',help="input file (bw format)",nargs="*", metavar="FILE")
    parser.add_argument('-labels','--labels',help="labels for the input files",nargs="*", metavar="FILE")
    parser.add_argument('-c','--color',help="colors for the input file tracks",nargs="*", metavar="FILE")
    parser.add_argument('-bs','--binsize',help="bins size",metavar="FILE")
    parser.add_argument('-after','--downstream',help="downstream regions to plot",metavar="FILE")
    parser.add_argument('-before','--upstream',help="upstream regions to plot",metavar="FILE")
    parser.add_argument('-r','--regions',help="regions to plot",metavar="FILE")
    parser.add_argument('-f','--file',help="file include all the regions to plot",metavar="FILE")
    parser.add_argument('-M','--meth',help="If bw file is methylation file, use -M.",action="store_true")
    multiTracks(parser) 
