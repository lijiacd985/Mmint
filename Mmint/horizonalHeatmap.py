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
from .utils import format_gz
plt.style.use('seaborn-white')

def run(parser):
    args = parser.parse_args()
    out=[]
    out.append(args.rowlabels[0]+'.gz')

    if args.scaleregion>0:
        subprocess.call("computeMatrix scale-regions -p 6 -S %s -R %s -a %s -b %s -bs %s -m %s -o %s" % (' '.join(args.bigwig),args.bed,args.dnregions,args.upregions,args.binsize,args.scaleregion, out[0]),shell=True)
    else:
        subprocess.call("computeMatrix reference-point --referencePoint center -p 6 -S %s -R %s -a %s -b %s -bs %s -o %s" % (' '.join(args.bigwig),args.bed,args.dnregions,args.upregions,args.binsize, out[0]),shell=True)
    subprocess.call("gunzip -f %s" % out[0], shell=True)

    array = format_gz(out,(int(args.upregions)+int(args.scaleregion)+int(args.dnregions))//int(args.binsize),[1]*len(args.rowlabels))
    fig,ax = plt.subplots()
    cmap = plt.cm.get_cmap('YlOrRd')
    heatmap=ax.pcolor(array,cmap=cmap,vmin=0,vmax=2)
    ax.set_yticks(np.arange(array.shape[0])+0.5, minor=False)
    ax.set_yticklabels(args.rowlabels, minor=False)
    if args.scaleregion>0:
        ax.set_xticks([0,int(args.upregions)/int(args.binsize),(int(args.upregions)+int(args.scaleregion))/int(args.binsize),(int(args.upregions)+int(args.scaleregion)+int(args.dnregions))/int(args.binsize)])
        ax.set_xticklabels(['-'+str(int(args.upregions)/1)+' bp','Start','END',str(int(args.dnregions)/1)+' bp'])
    else:
        ax.set_xticks([0,int(args.upregions)/int(args.binsize),(int(args.upregions)+int(args.dnregions))/int(args.binsize)])
        ax.set_xticklabels(['-'+str(int(args.upregions)/1)+' bp','Middle point',str(int(args.dnregions)/1)+' bp'])
    ax.set_xlim(0, array.shape[1])
    fig.colorbar(heatmap)
    ax.invert_yaxis()
    fig.savefig(str(args.output)+'.pdf', bbox_inches="tight")
    if os.path.exists(out[0]):
        os.remove(out[0])
    if os.path.exists(out[0][:-3]):
        os.remove(out[0][:-3])

if __name__=="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-bw','--bigwig',help="bigwig for the computeMatrix", nargs="*",metavar="FILE",required=True)
    parser.add_argument('-bed','--bed',help="the regions to plot", metavar="FILE",required=True)
    parser.add_argument('-after','--dnregions',help="downstream regions to plot",metavar="FILE",default=1000)
    parser.add_argument('-before','--upregions',help="upstream regions to plot",metavar="FILE",default=1000)
    parser.add_argument('-bs','--binsize',help="bins size to use", metavar="FILE",default=100)
    parser.add_argument('-m','--scaleregion',help="scale the input bed regions to certain length(bp)",metavar="FILE",default=1000)
    parser.add_argument('-L','--rowlabels',nargs="*",help="row labels for samples", metavar="FILE",required=True)
    parser.add_argument('-o','--output',help="prefix for the output PDF file", metavar="FILE",required=True)
    run(parser)
