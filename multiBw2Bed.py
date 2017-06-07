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
parser.add_argument('-bw','--bigwig',help="bigwig for the computeMatrix", nargs="*",metavar="FILE")
parser.add_argument('-bed','--bed',help="the regions to plot", metavar="FILE")
parser.add_argument('-after','--dnregions',help="downstream regions to plot",metavar="FILE")
parser.add_argument('-before','--upregions',help="upstream regions to plot",metavar="FILE")
parser.add_argument('-bs','--binsize',help="bins size to use", metavar="FILE")
parser.add_argument('-m','--scaleregion',help="scale the input bed regions to certain length(bp)",metavar="FILE")
parser.add_argument('-o','--outFile',help="output file name",nargs="*",metavar="FILE")
parser.add_argument('-L','--rowlabels',nargs="*",help="row labels for samples", metavar="FILE")
parser.add_argument('-n','--pdfName',help="name for pdf", metavar="FILE")
'''
def run(parser):
    args = parser.parse_args()


    ##need to install computeMatrix and add it to your ~/.bashrc file
    ##pass the python variables to subprocess

<<<<<<< HEAD:multiBw2bed.py
    ##iterate multiple input files
    for i in range(len(args.bigwig)):

        subprocess.call("computeMatrix scale-regions -S %s -R %s -a %s -b %s -bs %s -m %s -o %s" % (args.bigwig[i],args.bed,args.dnregions,args.upregions,args.binsize,args.scaleregion, args.outFile[i]),shell=True)
=======
##need to install computeMatrix and add it to your ~/.bashrc file
##pass the python variables to subprocess
subprocess.call("rm merge.ave.txt", shell=True)
##iterate multiple input files
for i in range(len(args.bigwig)):
    
    subprocess.call("computeMatrix scale-regions -S %s -R %s -a %s -b %s -bs %s -m %s -o %s" % (args.bigwig[i],args.bed,args.dnregions,args.upregions,args.binsize,args.scaleregion, args.outFile[i]),shell=True)
>>>>>>> upstream/master:multiBw2Bed.py


    for i in range(len(args.bigwig)):
        subprocess.call("gunzip -f %s" % args.outFile[i], shell=True)

<<<<<<< HEAD:multiBw2bed.py
    #for i in range(len(args.bigwig)):
    #    subprocess.call("sh format.sh %s" % args.outFile[i],shell=True)
    subprocess.call("sh format.meth.sh %s" % args.outFile[0],shell=True)
    #subprocess.call("sh format.sh %s" % args.outFile[0],shell=True)
    subprocess.call("sh format.sh %s" % args.outFile[1],shell=True)


    dt = pd.read_table("merge.ave.txt",header=None)

    array= dt.as_matrix(columns=dt.columns[0:])
    #print len(array)

    y=array
    x=np.arange((int(args.upregions)+int(args.scaleregion)+int(args.dnregions))/int(args.binsize))
    fig,ax1 = plt.subplots()
    ax2 = ax1.twinx()

    ax1.grid(False)
    ax2.grid(False)
    ax1.plot(x,y[0],color="red",linewidth=4)
    ax1.set_xlabel('Peaks')
    ax1.set_ylabel('Methylation Ratio',color="red")
    ax1.set_ylim((0,1))

    ax2.plot(x,y[1],color="dodgerblue",linewidth=4)
    ax2.set_ylabel('Chip-seq Signal',color="dodgerblue")
    ax2.set_ylim((0,(max(y[1])+0.1)))

    ax1.set_xticks([0,int(args.upregions)/int(args.binsize),(int(args.upregions)+int(args.scaleregion))/int(args.binsize),(int(args.upregions)+int(args.scaleregion)+int(args.dnregions))/int(args.binsize)])
    ax1.set_xticklabels(['-'+str(int(args.upregions)/1000)+' kp','Start','END',str(int(args.dnregions)/1000)+' kb'])
    fig.savefig(str(args.pdfName) + '.pdf')
    #fig.savefig("curveTest.pdf")
    #plt.show()

    ##python curvePlot3.py -bw 5hmC.norm.bw CTCF.bigWig -bed CTCFpeaks.bed -after 1000 -before 1000 -bs 20 -m 1000 -o test1.gz test2.gz -L 5hmC CTCF -n CTCF.5hmC
=======
for i in range(len(args.bigwig)):
    subprocess.call("sh format.sh %s" % args.outFile[i],shell=True)
#subprocess.call("rm merge.ave.txt", shell=True)
dt = pd.read_table("merge.ave.txt",header=None)
#data = np.random.rand(7,24)
#row_labels = ['5hmc','K4m1','K27ac','K4m3','K27m3','FAIRE','GRO','GRO']
row_labels = [a for a in args.rowlabels]

array= dt.as_matrix(columns=dt.columns[0:])
print len(array)

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
for i in range(len(array)):
    plt.plot(x,y[i],colours[i],linewidth=3,label=args.rowlabels[i])
    #plt.legend(args.rowlabels[i],loc="upper left")
    plt.legend(loc="upper left")
    #print args.rowlabels[i]
    #ax=fig.get_figure()
ax.set_xticks([0,int(args.upregions)/int(args.binsize),(int(args.upregions)+int(args.scaleregion))/int(args.binsize),(int(args.upregions)+int(args.scaleregion)+int(args.dnregions))/int(args.binsize)])
ax.set_xticklabels(['-'+str(int(args.upregions)/1000)+' kp','Start','END',str(int(args.dnregions)/1000)+' kb'])
#plt.title(args.rowlabels[i])
plt.xlabel('Regions Relative Positions')
plt.ylabel('Signals')
#fig.savefig(str(args.rowlabels[i])+".pdf")
#fig.savefig("curveTest2.pdf")
fig.savefig(args.pdfName +".pdf")
#plt.show()


>>>>>>> upstream/master:multiBw2Bed.py
