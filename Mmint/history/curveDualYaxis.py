import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import colors
from utils import format_gz
import os,sys
import argparse
from scipy import stats
#import seaborn as sns
import subprocess


def run(parser):
    args = parser.parse_args()


    out=[]
    for label in args.rowlabels:
        out.append(label+'.gz')
    for i in range(len(args.bigwig)):
        subprocess.call("computeMatrix scale-regions -p 6 -S %s -R %s -a %s -b %s -bs %s -m %s -o %s" % (args.bigwig[i] \
                ,args.bed,args.dnregions,args.upregions,args.binsize,args.scaleregion, out[i]),shell=True)

    for i in range(len(args.bigwig)):
        subprocess.call("gunzip -f %s" % out[i], shell=True)

    result = format_gz(out, (int(args.upregions)+int(args.scaleregion)+int(args.dnregions))//int(args.binsize),[0,1])



    y=result
    x=np.arange((int(args.upregions)+int(args.scaleregion)+int(args.dnregions))/int(args.binsize))
    fig,ax1 = plt.subplots()
    fig.subplots_adjust(bottom=0.125,right=0.85)
    ax2 = ax1.twinx()

    ax1.grid(False)
    ax2.grid(False)
    ax1.plot(x,y[0],color="red",linewidth=4)
    ax1.set_xlabel('Regions Relative Positions',fontsize=13)
    ax1.set_ylabel(args.rowlabels[0],color="red",fontsize=13)
    
    ax1.set_ylim((0,1))

    ax2.plot(x,y[1],color="dodgerblue",linewidth=4)
    ax2.set_ylabel(args.rowlabels[1],color="dodgerblue",fontsize=13)
    ax2.set_ylim((1,(max(y[1])+1)))
    ax2.yaxis.set_tick_params(labelsize=13)

    ax1.set_xticks([0,int(args.upregions)/int(args.binsize),(int(args.upregions)+int(args.scaleregion))/int(args.binsize),(int(args.upregions)+int(args.scaleregion)+int(args.dnregions))/int(args.binsize)])
    ax1.set_xticklabels(['-'+str(int(args.upregions)/1000)+' kp','Start','END',str(int(args.dnregions)/1000)+' kb'],fontsize=13)
    ax1.yaxis.set_tick_params(labelsize=13)
    fig.savefig(str(args.pdfname) + '.pdf',figsize=(15,12))

if __name__=="__main__":
    parser = argparse.ArgumentParser() 
    parser.add_argument('-bw','--bigwig',help="bigwig for the computeMatrix", nargs="*",metavar="FILE")
    parser.add_argument('-bed','--bed',help="the regions to plot", metavar="FILE")
    parser.add_argument('-after','--dnregions',help="downstream regions to plot",metavar="FILE", default=1000)
    parser.add_argument('-before','--upregions',help="upstream regions to plot",metavar="FILE", default=1000)
    parser.add_argument('-bs','--binsize',help="bins size to use", metavar="FILE", default=100)
    parser.add_argument('-m','--scaleregion',help="scale the input bed regions to certain length(bp)",metavar="FILE", default=1000)
    parser.add_argument('-L','--rowlabels',nargs="*",help="row labels for samples", metavar="FILE",required=True)
    parser.add_argument('-n','--pdfname',help="name for pdf", metavar="FILE", required=True)


    run(parser)
