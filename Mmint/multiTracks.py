
import numpy as np
import os,sys
import argparse
import subprocess
import matplotlib
matplotlib.use('Agg')
from io import StringIO
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
import itertools
import pandas as pd
plt.style.use('ggplot')
from collections import defaultdict
from scipy.interpolate import interp1d
from scipy.signal import cspline1d
import matplotlib.ticker as ticker
from pylab import *
import scipy

def run(parser):
    args = parser.parse_args()

    args.marker = list(map(lambda x:int(x), args.marker))

    FILE = open(args.file,'r')
    colours = cm.rainbow(np.linspace(0, 1, len(args.labels)))
    ymax=[]
    out=[]
    RawCounts=[]
    for label in args.labels:
        out.append(label+'.npz')
        RawCounts.append(label+'.tab')
    #for line in FILE:
    #    line=line.strip().split('\t')
    #    chr,start,end = line[0].split(':')
    #    start = str(int(start)-args.upstream)
    #    end = str(int(end)+args.downstream)
    #    array1.append(chr+':'+start+':'+end)
    #    array2.append(line[1])
    for k in FILE:
        kk = k.strip().split()
        chr, start, end = kk[:3]
        pos = ':'.join([chr,start,end])
        if len(kk)>3:
            genename = kk[3]
        region_data = []

        start, end = int(start), int(end)
        list_start = start-start%args.binsize

        for i in range(len(args.bigwig)):
            if args.marker[i]==1:
                subprocess.call("multiBigwigSummary bins -bs %s -r %s -b %s --labels %s -out %s --outRawCounts %s" % (args.binsize, pos,args.bigwig[i],args.labels[i] \
                        ,out[i],RawCounts[i]),shell=True)
            else:
                bin_size = '3' 
                subprocess.call("multiBigwigSummary bins -bs %s -r %s -b %s --labels %s -out %s --outRawCounts %s" % (bin_size, pos,args.bigwig[i],args.labels[i] \
                        ,out[i],RawCounts[i]),shell=True)

            if os.path.exists(out[i]):
                os.remove(out[i])
            with open(RawCounts[i]) as f:
                lines = f.readlines()
            os.remove(RawCounts[i])
            d=[]
            for line in lines[1:]:
                c = line.strip().split()
                #print(c)
                num = c[-1]
                if num=='nan':
                    num = 0.0
                    #if args.marker[i]==1:
                    #    num = 0.0
                    #else:
                    #    num = -1
                else:
                    num = float(num)
                d.append(num)
            region_data.append(d)
        x_trans = np.arange(list_start,end,args.binsize)
        #if len(x_trans)<len(d): x_trans.append(end)


        #for i in range(len(args.bigwig)):
    	#    subprocess.call("sed -i 's/nan/0/g' %s" % RawCounts[i], shell=True)
        #for i in range(len(args.bigwig)):
        #    subprocess.call("sh format.shareX.sh %s" % RawCounts[i],shell=True)
        #dt = pd.read_table("merge.clean",header=1)
        #x_sub_flat = dt.as_matrix(columns=dt.columns[2:3])
        #print 'A'
        #x_trans = list(map(list,list(zip(*x_sub_flat))))
        
        #y_sub = [a for a in dt.as_matrix(columns = dt.columns[3:dt.shape[1]])]
        y_trans = np.array(region_data)#list(map(list,list(zip(*y_sub))))
        plt.close('all')
        x_smooth = np.linspace(min(x_trans), max(x_trans), 300)
        #print len(y_trans)
        #print(y_trans)
        #print(x_smooth)
        y_smooth=[]
        for i in range(len(y_trans)):
            #y_smooth.append(splrep(x_trans, y_trans[i]))
            #print(x_trans, y_trans[i], len(x_smooth))
            if args.marker[i]==1:
                func = interp1d(x_trans, y_trans[i])#, fill_value=x_smooth)
                temp = func(x_smooth)
                #print(temp)
                y_smooth.append(temp)
                ymax.append(max(y_trans[i]))
            else:
                y_smooth.append(y_trans[i])#[:300])
                ymax.append(1)  # Methylation maximum value = 1
        fig,ax1 = plt.subplots(figsize=(15,10))
        #print(y_smooth)
        mmax=np.zeros(len(args.labels))
        for i in range(len(args.labels)):
            mmax[i] = max(mmax[i],np.max(y_smooth[i]))
        
        for i,v in enumerate(range(len(y_trans))):
            if args.marker[i]==1:
                x_s = x_smooth 
            else:
                x_s = np.linspace(min(x_trans), max(x_trans), len(y_smooth[i]))
            v=v+1
            ax1 = subplot(len(y_trans),1,v)
            #ax1.plot(x_s,y_smooth[i],color='white',linewidth=0.1)
            #print(i,v)
            #if args.meth:
            #    ax1.set_ylim(0,1.1)
            #else:
            #    ax1.set_ylim(0,mmax[i])
            ax1.set_ylim(0,mmax[i])
            plt.ylabel(args.labels[i],rotation=90,fontsize=12)
            plt.axvline(x_trans[0]+args.upstream,color='red',linewidth=1,linestyle='dashed')
            plt.axvline(x_trans[-1]-args.downstream,color='red',linewidth=1,linestyle='dashed')
            d = np.zeros(300)
            if args.marker[i]==1:
                ax1.plot(x_s,y_smooth[i],color='white',linewidth=0.1)
                ax1.fill_between(x_s,y_smooth[i],where=y_smooth[i]>=d,interpolate=True,color=colours[i])
            else:
                ax1.vlines(x_s,0,y_smooth[i],color=colours[i],linewidth=0.5,facecolors=colours[i])
            ax1.spines['top'].set_visible(False)
            ax1.spines['right'].set_visible(False)
            ax1.spines['bottom'].set_visible(False)
            ax1.yaxis.set_major_formatter(ticker.FormatStrFormatter('%0.1f'))
            ax1.yaxis.set_ticks_position('left')
            ax1.xaxis.set_ticks_position('none')
            subplots_adjust(hspace=0.05)
            plt.setp(ax1.get_xticklabels(), visible=False)
        plt.setp(ax1.get_xticklabels(), visible=True)
        if len(kk)>3:
            plt.xlabel(genename+" "+pos)
        else:
            plt.xlabel(pos)
        fig.tight_layout()
        ymax=[]
        if len(kk)>3:
            fig.savefig(genename+'_'+pos+'.pdf', bbox_inches="tight")
        else:
            fig.savefig(pos+'.pdf', bbox_inches="tight")



if __name__=="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-b','--bigwig',help="input file (bw format)",nargs="*", metavar="FILE")
    parser.add_argument('-labels','--labels',help="labels for the input files",nargs="*", metavar="FILE")
    parser.add_argument('-bs','--binsize',help="bins size",metavar="FILE",default=100)
    parser.add_argument('-after','--downstream',help="downstream regions to plot",metavar="FILE",default=1000)
    parser.add_argument('-before','--upstream',help="upstream regions to plot",metavar="FILE",default=1000)
    parser.add_argument('-f','--file',help="file include all the regions to plot",metavar="FILE")
    parser.add_argument('-M','--marker',help="Information type of bigwig. Single base resolution(0)/region(1) resolution have different methods to calculate the average. For example: -M 1 0 1 means the first/third are region data. default: all samples are single base data.", nargs="*")
    run(parser) 
