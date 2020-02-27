import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import colors
import os,sys
import argparse
from scipy import stats
#import seaborn as sns
import subprocess
from .utils import format_gz    
import pybedtools
plt.style.use('seaborn-white')

def run(parser):
    args = parser.parse_args()
    
    if os.path.exists('merge.ave.txt'):
        os.remove('merge.ave.txt')
    if len(args.rowlabels)!=2:
        raise Exception()
    bed1, bed2 = args.bed
    base_str = args.rowlabels[0]+'_vs_'+args.rowlabels[1]
    out = [base_str+'.intersect.bed',base_str+'.'+args.rowlabels[0]+'_only.bed',base_str+'.'+args.rowlabels[1]+'_only.bed',base_str+'.complement.bed']
    subprocess.call("bedops -i %s %s > %s" % (bed1,bed2,out[0]),shell=True)
    subprocess.call("bedops -n 1 %s %s > %s" % (bed1,bed2,out[1]),shell=True)
    subprocess.call("bedops -n 1 %s %s > %s" % (bed2,bed1,out[2]),shell=True)
    subprocess.call("bedops -c %s %s > %s" % (bed1,bed2,out[3]),shell=True) 

    if args.filterbed:
        if not os.path.exists(args.filterbed):
            raise Exception(args.filterbed + "not found !")
        for name in out:
            b1 = pybedtools.BedTool(name)
            b2 = pybedtools.BedTool(args.filterbed)
            b3 = b1.intersect(b2,wa=True)
            b3.saveas(name)

    out_gz = [o[:-4]+'.matrix.gz' for o in out]

    for i in range(len(out)):
    	subprocess.call("computeMatrix reference-point --referencePoint center -p 6 -S %s -R %s -a %s -b %s -bs %s -o %s" % (args.bigwig,out[i],args.dnregions,args.upregions,args.binsize,out_gz[i]),shell=True)
    	subprocess.call("gunzip -f %s" % out_gz[i], shell=True)
    
    result = format_gz(out_gz, (int(args.dnregions)+int(args.upregions))//int(args.binsize), [0]*4)
    
    y=np.array(result)
    x=np.arange((int(args.upregions)+int(args.dnregions))/int(args.binsize))
    colours=['r','g','b','orange','c','m','orange','violet','lightpink']
    fig,ax = plt.subplots()
    plt.xlim(0,x[-1])
    plt.title(base_str)
    for i in range(len(y)):
        label = out[i][:-4]
        label = label.replace('_',' ')
        label = label[label.find('.')+1:]+' regions'
        plt.plot(x,y[i],colours[i],linewidth=3,label=label)
    plt.legend(loc="center left",bbox_to_anchor=(1.04,0.5))
    ax.set_xticks([0,int(args.upregions)/int(args.binsize),(int(args.upregions)+int(args.dnregions))/int(args.binsize)])
    ax.set_xticklabels(['-'+str(int(args.upregions)/1000)+' kb','Center',str(int(args.dnregions)/1000)+' kb'])
    ax.yaxis.set_tick_params(labelsize=13)
    ax.xaxis.set_tick_params(labelsize=13)
    plt.xlabel('Regions Relative Positions',fontsize=13)
    plt.ylabel('Signals',fontsize=13)
    fig.savefig(args.pdfName +".pdf", bbox_inches="tight")
    for o in out_gz:
        if os.path.exists(o[:-3]):
            os.remove(o[:-3])

if __name__=="__main__":
    parser = parser = argparse.ArgumentParser()
    parser.add_argument('-bed','--bed',help="Two bedfiles representing two different histone modification.",nargs='*',metavar="FILE",required=True)
    parser.add_argument('-bw','--bigwig',help="bigwig for the computeMatrix", metavar="FILE",required=True)
    parser.add_argument('-after','--dnregions',help="downstream regions to plot",metavar="FILE",default=1000)
    parser.add_argument('-before','--upregions',help="upstream regions to plot",metavar="FILE",default=1000)
    parser.add_argument('-bs','--binsize',help="bins size to use", metavar="FILE",default=100)
    parser.add_argument('-L','--rowlabels',nargs="*",help="row labels for samples", metavar="FILE")
    parser.add_argument('-M','--methmarker',help="If bw file is methylation file, use -M.",action="store_true")
    parser.add_argument('-fb','--filterbed',help="Only use regions overlapped with given bed.")
    parser.add_argument('-n','--pdfName',help="Prefix for the result PDF file", metavar="FILE")
    run(parser)
