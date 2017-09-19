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
    parser.add_argument('-tss','--TSS',help="Genes TSS updn 1k bed file",metavar="FILE")
    parser.add_argument('-gene','--GENE',help="Genes bed file",metavar="FILE")
    parser.add_argument('-b1','--bed1',help="the first bedfile",metavar="FILE")
    parser.add_argument('-b2','--bed2',help="the second bedfile",metavar="FILE")
    parser.add_argument('-o1','--out',help="output file name",nargs="*",metavar="FILE")
    parser.add_argument('-o','--outFile',help="output file name",nargs="*",metavar="FILE")
    parser.add_argument('-bw','--bigwig',help="bigwig for the computeMatrix", metavar="FILE")
    #parser.add_argument('-bed','--bed',help="the regions to plot", metavar="FILE")
    parser.add_argument('-m','--scaleregion',help="scale the input bed regions to certain length(bp)",metavar="FILE")
    parser.add_argument('-after','--dnregions',help="downstream regions to plot",metavar="FILE")
    parser.add_argument('-before','--upregions',help="upstream regions to plot",metavar="FILE")
    parser.add_argument('-bs','--binsize',help="bins size to use", metavar="FILE")
    parser.add_argument('-L','--rowlabels',nargs="*",help="row labels for samples", metavar="FILE")
    parser.add_argument('-n','--pdfName',help="name for pdf", metavar="FILE")
    
    args = parser.parse_args()
'''
def run(parser):
    args = parser.parse_args() 
    
    #subprocess.call("bedops -i args.bed1 args.bed2 args.out[1]",shell=True)
    #subprocess.call("awk '{print $1'\t'$2'\t'$2+1}' %s > %s" % (args.GENE,))
    #join -1 4 -2 4 <(sort -k4,4b mm10.tss.bed) <(sort -k4,4b test) |sed 's/ /\t/g' | awk '{print $2"\t"$3"\t"$4"\t"$1}'|sort -u |head
    subprocess.call("bedtools intersect -a  %s -b %s -wo |cut -f1-4|sort -u|sort -k4,4b > tmp" % (args.TSS,args.bed1),shell=True)
    subprocess.call("join -1 4 -2 4 %s tmp |sed 's/ /\t/g' | awk '{print $2,$3,$4,$1}'|sort -u|sed 's/ /\t/g' > tmp1" % (args.GENE),shell=True)
    subprocess.call("bedtools intersect -a  %s -b %s -wo |cut -f1-4|sort -u|sort -k4,4b > tmp" % (args.TSS,args.bed2),shell=True)
    subprocess.call("join -1 4 -2 4  %s  tmp |sed 's/ /\t/g' | awk '{print $2,$3,$4,$1}'|sort -u|sed 's/ /\t/g' > tmp2" % (args.GENE),shell=True)
    ##common
    subprocess.call("bedtools intersect -a tmp1 -b tmp2 -wo |cut -f1-4|sort -u > %s" % (args.out[0]),shell=True)
    ##spec1
    subprocess.call("bedtools intersect -a tmp1 -b tmp2 -wao |grep -P '\t.\t' |cut -f1-3|sort -u > %s" % (args.out[1]),shell=True)
    ##spec2
    subprocess.call("bedtools intersect -a tmp2 -b tmp1 -wao |grep -P '\t.\t' |cut -f1-3|sort -u > %s" % (args.out[2]),shell=True)
    ##NO Histones
    subprocess.call("cat tmp1 tmp2 > merge", shell=True)
    subprocess.call("bedtools intersect -a %s -b merge -wao |grep '\-1' |cut -f1-3|sort -u > %s" % (args.GENE,args.out[3]),shell=True)
    
    
    for i in range(len(args.out)):
    	subprocess.call("computeMatrix scale-regions -S %s -R %s -a %s -b %s -bs %s -m %s -o %s" % (args.bigwig,args.out[i],args.dnregions,args.upregions,args.binsize,args.scaleregion,args.outFile[i]),shell=True)
    
    subprocess.call("rm merge.ave.txt", shell=True)
    
    for i in range(len(args.out)):
            subprocess.call("gunzip -f %s" % args.outFile[i], shell=True)
    
    for i in range(len(args.out)):
            #subprocess.call("sh format.sh %s" % args.outFile[i],shell=True)
            subprocess.call("sh format.meth.sh %s" % args.outFile[i],shell=True)
    
    dt = pd.read_table("merge.ave.txt",header=None)
    
    row_labels = [a for a in args.rowlabels]
    
    array= dt.as_matrix(columns=dt.columns[0:])
    #    print len(array)
    
    y=array
        #a=np.arange(len(array[0])).reshape(1,len(array[0]))
        #x=np.repeat(a,len(array),axis=0)
    x=np.arange((int(args.upregions)+int(args.scaleregion)+int(args.dnregions))/int(args.binsize))
    colours=['r','g','b','orange','c','m','orange','violet','lightpink']
        #plt.xlim(0, len(array[2]))
        #for i in range(len(x)):
            #fig=plt.figure()
    fig,ax = plt.subplots()
    plt.xlim(0,len(array[0]))
    plt.ylim(0,100)
    for i in range(len(array)):
        plt.plot(x,y[i],colours[i],linewidth=3,label=args.rowlabels[i])
        #plt.legend(args.rowlabels[i],loc="upper left")
        plt.legend(loc="lower right")

            #print args.rowlabels[i]
            #ax=fig.get_figure()
    
    ax.set_xticks([0,int(args.upregions)/int(args.binsize),(int(args.upregions)+int(args.scaleregion))/int(args.binsize),(int(args.upregions)+int(args.scaleregion)+int(args.dnregions))/int(args.binsize)])
    ax.set_xticklabels(['-'+str(int(args.upregions)/1000)+' kb','Start','END',str(int(args.dnregions)/1000)+' kb'])
    
    ax.yaxis.set_tick_params(labelsize=13)
    ax.xaxis.set_tick_params(labelsize=13)
    plt.xlabel('Regions Relative Positions',fontsize=13)
    plt.ylabel('Signals',fontsize=13)
        #fig.savefig(str(args.rowlabels[i])+".pdf")
        #fig.savefig("curveTest2.pdf")
    fig.savefig(args.pdfName +".pdf")
