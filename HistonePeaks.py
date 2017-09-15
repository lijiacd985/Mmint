#!/usr/bin/env python
 
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import colors
import os,sys
import argparse
from scipy import stats
#import seaborn as sns
import subprocess
    
''' 
    parser = argparse.ArgumentParser()
    parser.add_argument('-b1','--bed1',help="the first bedfile",metavar="FILE")
    parser.add_argument('-b2','--bed2',help="the second bedfile",metavar="FILE")
    parser.add_argument('-o1','--out',help="output file name",nargs="*",metavar="FILE")
    parser.add_argument('-o','--outFile',help="output file name",nargs="*",metavar="FILE")
    parser.add_argument('-bw','--bigwig',help="bigwig for the computeMatrix", metavar="FILE")
    #parser.add_argument('-bed','--bed',help="the regions to plot", metavar="FILE")
    parser.add_argument('-after','--dnregions',help="downstream regions to plot",metavar="FILE")
    parser.add_argument('-before','--upregions',help="upstream regions to plot",metavar="FILE")
    parser.add_argument('-bs','--binsize',help="bins size to use", metavar="FILE")
    parser.add_argument('-L','--rowlabels',nargs="*",help="row labels for samples", metavar="FILE")
    parser.add_argument('-n','--pdfName',help="name for pdf", metavar="FILE")
    parser.add_argument('-m','--meth',help="If bw file is methylation file, use -m.",action="store_true")
    args = parser.parse_args()
    
    print args.bed1

'''    

def run(parser):
    args = parser.parse_args()

    subprocess.call("rm merge.ave.txt",shell=True)
    
    subprocess.call("bedops -i %s %s > %s" % (args.bed1,args.bed2,args.out[0]),shell=True)
    subprocess.call("bedops -n 1 %s %s > %s" % (args.bed1,args.bed2,args.out[1]),shell=True)
    subprocess.call("bedops -n 1 %s %s > %s" % (args.bed2,args.bed1,args.out[2]),shell=True)
    subprocess.call("bedops -c %s %s > %s" % (args.bed1,args.bed2,args.out[3]),shell=True) 
    for i in range(len(args.out)):
    	subprocess.call("computeMatrix reference-point --referencePoint center -S %s -R %s -a %s -b %s -bs %s -o %s" % (args.bigwig,args.out[i],args.dnregions,args.upregions,args.binsize,args.outFile[i]),shell=True)
    
    for i in range(len(args.out)):
            subprocess.call("gunzip -f %s" % args.outFile[i], shell=True)
    
    for i in range(len(args.out)):
        if args.meth:
            subprocess.call("sh format.meth.sh %s" % args.outFile[i],shell=True)
        else:
            subprocess.call("sh format.sh %s" % args.outFile[i],shell=True)
    
    dt = pd.read_table("merge.ave.txt",header=None)
    
    row_labels = [a for a in args.rowlabels]
    
    array= dt.as_matrix(columns=dt.columns[0:])
    #    print len(array)
    
    y=array
        #a=np.arange(len(array[0])).reshape(1,len(array[0]))
        #x=np.repeat(a,len(array),axis=0)
    x=np.arange((int(args.upregions)+int(args.dnregions))/int(args.binsize))
    colours=['r','g','b','orange','c','m','orange','violet','lightpink']
        #plt.xlim(0, len(array[2]))
        #for i in range(len(x)):
            #fig=plt.figure()
    fig,ax = plt.subplots()
    plt.xlim(0,len(array[0]))
    plt.xlim(0,100)
    for i in range(len(array)):
        plt.plot(x,y[i],colours[i],linewidth=3,label=args.rowlabels[i])
        #plt.legend(args.rowlabels[i],loc="upper left")
        plt.legend(loc="upper left")
            #print args.rowlabels[i]
            #ax=fig.get_figure()
    ax.set_xticks([0,int(args.upregions)/int(args.binsize),(int(args.upregions)+int(args.dnregions))/int(args.binsize)])
    ax.set_xticklabels(['-'+str(int(args.upregions)/1000)+' kb','Center',str(int(args.dnregions)/1000)+' kb'])
        #plt.title(args.rowlabels[i])
    ax.yaxis.set_tick_params(labelsize=13)
    ax.xaxis.set_tick_params(labelsize=13)
    plt.xlabel('Regions Relative Positions',fontsize=13)
    plt.ylabel('Signals',fontsize=13)
        #fig.savefig(str(args.rowlabels[i])+".pdf")
        #fig.savefig("curveTest2.pdf")
    fig.savefig(args.pdfName +".pdf")
