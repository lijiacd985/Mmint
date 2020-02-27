import matplotlib
matplotlib.use('Agg')
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import colors
import os,sys
import argparse
from .utils import format_gz
from scipy import stats
#import seaborn as sns
import matplotlib.cm as cm
import subprocess
import time
plt.style.use('seaborn-white')

def run(parser):
    args = parser.parse_args()

    ## Input parameters checking
    filenum = len(args.bigwig)
    if not(len(args.bed)==1 or len(args.bed)==filenum):
        raise Exception("Number of bed file should either be 1 or be equal to the number of bigwig files.")
    if filenum!=len(args.rowlabels):
        raise Exception("Number of rowlabels should be equal to the number of samples!")
    for bwf in args.bigwig:
        if not os.path.exists(bwf):
            raise Exception("File not exists: "+bwf)
    for bedf in args.bed:
        if not os.path.exists(bedf):
            raise Exception("File not exists: "+bedf)
    if args.marker:
        marker = args.marker
        if len(marker)!=filenum:
            raise Exception("The number of information markers should be the same as the number of bigwig files!")
    else:
        marker = [0] * filenum # Default value for information markers(single base type(0)/region type(1))


    if os.path.exists("merge.ave.txt"):
        os.remove("merge.ave.txt")

    outFile=[ l+'.gz' for l in args.rowlabels]
    
    cm_method = 'scale-regions'
    if args.scaleregion==0:
        cm_method = 'reference-point'

    if len(args.bed)==1:
        outFile = [outFile[0]]
        if args.scaleregion==0:
            cmd = "computeMatrix scale-regions -p 6 -S %s -R %s -a %s -b %s -bs %s -m %s -o %s" % (' '.join(args.bigwig) \
                    ,args.bed[0], args.upregions, args.dnregions, args.binsize, args.scaleregion, outFile[0])
        else:
            cmd = "computeMatrix reference-point --referencePoint center -p 6 -S %s -R %s -a %s -b %s -bs %s -o %s" % (' '.join(args.bigwig) \
                    ,args.bed[0], args.upregions, args.dnregions, args.binsize, outFile[0])
        # print(cmd)
        subprocess.call(cmd, shell=True)

    else:
        for i, bwf in enumerate(args.bigwig):
            if args.scaleregion==0:
                cmd = "computeMatrix scale-regions -p 6 -S %s -R %s -a %s -b %s -bs %s -m %s -o %s" % (args.bigwig[i] \
                        ,args.bed[i], args.upregions, args.dnregions, args.binsize, args.scaleregion, outFile[i])
            else:
                cmd = "computeMatrix reference-point --referencePoint center -p 6 -S %s -R %s -a %s -b %s -bs %s -o %s" % (' '.join(args.bigwig) \
                        ,args.bed[0], args.upregions, args.dnregions, args.binsize, outFile[0])
            subprocess.call(cmd, shell=True)

    for name in outFile:
        subprocess.call("gunzip -f %s" % name, shell=True)

    result = format_gz(outFile, (int(args.upregions)+int(args.scaleregion)+int(args.dnregions))//int(args.binsize),args.marker)     

    ## Plotting
    y=result
    x=np.arange((int(args.upregions)+int(args.scaleregion)+int(args.dnregions))/int(args.binsize))
    temp1 = np.arange(len(args.bigwig))
    colours = cm.rainbow(np.linspace(0, 1, len(args.bigwig)))

    data_type = 0
    for i in args.marker:
        data_type = data_type | (int(i)+1)

    fig,ax1 = plt.subplots()
    if data_type==3:
        ax2 = ax1.twinx()
    plt.xlim(0,len(y[0]))
    # print(data_type, args.marker)
    if data_type!=3:
        for i in range(len(y)):
            ax1.plot(x,y[i],color=colours[i],linewidth=2,label=args.rowlabels[i])
    else:
        for i in range(len(y)):
            # print(i, args.marker[i],args.marker)
            if int(args.marker[i])==0:
                ax1.plot(x,y[i],color=colours[i],linewidth=2,label=args.rowlabels[i],linestyle='-')
            else:
                ax2.plot(x,y[i],color=colours[i],linewidth=2,label=args.rowlabels[i],linestyle=(0, (5, 10)))
    
    if data_type==3:
        plt.legend(loc='center left', bbox_to_anchor=(1.14, 0.5))   
    else:
        plt.legend(loc='center left', bbox_to_anchor=(1.04, 0.5))
    if args.scaleregion!=0:
        ax1.set_xticks([0,int(args.upregions)/int(args.binsize),(int(args.upregions)+int(args.scaleregion))/int(args.binsize), \
                (int(args.upregions)+int(args.scaleregion)+int(args.dnregions))/int(args.binsize)])
        ax1.set_xticklabels(['-'+str(int(args.upregions)/1000)+' kb','Start','END',str(int(args.dnregions)/1000)+' kb'])
    else:
        ax1.set_xticks([0,int(args.upregions)/int(args.binsize), (int(args.upregions)+int(args.dnregions))/int(args.binsize)])
        ax1.set_xticklabels(['-'+str(int(args.upregions)/1000)+' kb','Middle point',str(int(args.dnregions)/1000)+' kb'])

    ax1.yaxis.set_tick_params(labelsize=13)
    ax1.xaxis.set_tick_params(labelsize=13)
    if data_type==3:
        ax2.set_ylabel("Region Signals(--)",fontsize=13)
        ax2.yaxis.set_tick_params(labelsize=13)
    plt.xlabel('Regions Relative Positions',fontsize=13)
    if data_type<=2:
        ax1.set_ylabel('Signals',fontsize=13)
    else:
        ax1.set_ylabel('Single base Signals(-)',fontsize=13)
    fig.savefig(args.output +".pdf", bbox_inches="tight")


    for name in outFile:
        if os.path.exists(name):
            os.remove(name)
        if name[-3:]=='.gz':
            if os.path.exists(name[:-3]):
                os.remove(name[:-3])


if __name__=="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-bw','--bigwig',help="bigwig or bed for the computeMatrix", nargs="*",metavar="FILE")
    parser.add_argument('-bed','--bed',help="the regions to plot", metavar="FILE", nargs="*")
    parser.add_argument('-after','--dnregions',help="downstream regions to plot", default=1000,type=int)
    parser.add_argument('-before','--upregions',help="upstream regions to plot", default=1000,type=int)
    parser.add_argument('-bs','--binsize',help="bins size to use", default=100,type=int)
    parser.add_argument('-m','--scaleregion',help="scale the input bed regions to certain length(bp)", default=1000,type=int)
    parser.add_argument('-g','--genome',help="Genome for transfering bed to bw. Not necessary if there's bed file in -bw. Select from: hg19,hg38,mm9,mm10",default="hg19")
    parser.add_argument('-L','--rowlabels',nargs="*",help="row labels for samples")
    parser.add_argument('-M','--marker',help="Information type of bigwig. Single base resolution(0)/region(1) resolution have different methods to calculate the average. For example: -M 1 0 1 means the first/third are region data. default: all samples are single base data.", nargs="*")
    parser.add_argument('-o','--output',help="Prefix for output pdf file.", metavar="FILE")
    run(parser)
