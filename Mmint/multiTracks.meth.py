#!/usr/bin/env python

import numpy as np
import os,sys
import matplotlib
matplotlib.use('Agg')
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



parser = argparse.ArgumentParser()
parser.add_argument('-b','--bigwig',help="input file (bw format)",nargs="*", metavar="FILE")
parser.add_argument('-labels','--labels',help="labels for the input files",nargs="*", metavar="FILE")
parser.add_argument('-c','--color',help="colors for the input file tracks",nargs="*", metavar="FILE")
parser.add_argument('-bs','--binsize',help="bins size",metavar="FILE")
parser.add_argument('-out','--out',help="output",nargs="*",metavar="FILE")
parser.add_argument('-outRawCounts','--RawCounts',help="Raw counts output",nargs="*",metavar="FILE")
parser.add_argument('-r','--regions',help="regions to plot",metavar="FILE")
parser.add_argument('-f','--file',help="file include all the regions to plot",metavar="FILE")
args = parser.parse_args()
print(args.bigwig)
print(args.file)

FILE = open(args.file,'r')
array1 = []
array2 = []
for line in FILE:
	line=line.strip().split('\t')
	array1.append(line[0])
	array2.append(line[1])
for k in range(len(array1)):
#	print array1[k]

	for i in range(len(args.bigwig)):
	#	subprocess.call("multiBigwigSummary bins -bs %s -r chr1:907000:910000 -b d01.bam.norm2.bw d03.bam.norm.bw d14.bam.norm.bw --labels %s -out %s --outRawCounts %s" % (args.binsize,args.labels,args.out,args.RawCounts),shell=False)
    		subprocess.call("multiBigwigSummary bins -bs %s -r %s -b %s --labels %s -out %s --outRawCounts %s" % (args.binsize, array1[k],args.bigwig[i],args.labels[i],args.out[i],args.RawCounts[i]),shell=True)

	for i in range(len(args.bigwig)):
    		subprocess.call("sed -i 's/nan/0/g' %s" % args.RawCounts[i], shell=True)

	for i in range(len(args.bigwig)):
    		subprocess.call("sh format.shareX.sh %s" % args.RawCounts[i],shell=True)


	dt = pd.read_table("merge.clean",header=1)
#print dt.as_matrix(columns=dt.columns[2:])
	x_sub_flat = dt.as_matrix(columns=dt.columns[2:3])
	x_trans = list(map(list,list(zip(*x_sub_flat))))
	#print x_trans
	#print dt.shape[1]
	y_sub = [a for a in dt.as_matrix(columns = dt.columns[3:dt.shape[1]])]
	y_trans = list(map(list,list(zip(*y_sub))))
	#print len(y_trans)

	plt.close('all')


#smooth the lines
#	x_smooth = np.linspace(min(x_trans[0]), max(x_trans[0]), 300)
#	y_smooth=[]
#	for i in range(len(y_trans)):
#    		y_smooth.append (spline(x_trans[0], y_trans[i], x_smooth))
	#print y_smooth
#plot
#	y_smooth2 = spline(x_trans[0], y_trans[1], x_smooth)
	fig,ax1 = plt.subplots(figsize=(15,10))
	#ax1.set_title(array[k])
	#print x_trans[0][0]
	#print x_trans[0][-1]
	for i,v in enumerate(range(len(y_trans))):
    	    #ax1.set_title(array[k])
	    v=v+1
    	    ax1 = subplot(len(y_trans),1,v)   
    	    #ax1.plot(x_trans[0],y_trans[i],color='red',linewidth=0.5)
    #ax1.set_title(args.label[i])
	    plt.axvline(x_trans[0][0]+5000,color='red',linewidth=2,linestyle='dashed')
            plt.axvline(x_trans[0][-1]-5000,color='red',linewidth=2,linestyle='dashed')
	    ax1.vlines(x_trans[0], [0], y_trans[i],color='blue',linewidth=0.5)
	    #ax1.acorr(x_trans[0],y_trans[i],usevlines=True,maxlags=50,lw=1)
            #plt.axvline((x,ymin=0,ymax=y_trans[i],color='blue',linewidth=0.8) for x in x_trans[0])
	    #plt.axvline((x,y==y_trans[i],color=='blue',linewidth==0.8) for x in x_trans[0])
            plt.ylabel(args.labels[i],rotation=90,fontsize=12)
    	    d = scipy.zeros(300)
            ax1.set_ylim(0, 1.1)
     	    #ax1.fill_between(x_trans[0],y_trans[i],where=y_smooth[i]>=d,interpolate=True,color=args.color[i])
    	    #ax1.spines['top'].set_visible(False)
    	    #ax1.spines['right'].set_visible(False)
    	    #ax1.spines['bottom'].set_visible(False)
            #print max(y_smooth[i])
#    	    ax1.yaxis.set_ticks(np.arange(0, max(y_trans[i])+max(y_trans[i])/3, max(y_trans[i])/3))
            ax1.yaxis.set_major_formatter(ticker.FormatStrFormatter('%0.1f'))
            ax1.yaxis.set_ticks_position('left')
    	    ax1.xaxis.set_ticks_position('none')
    	    #ax1.set_ylim([0,max(y_smooth[i])+0.2])
    	    ax1.ticklabel_format(axis='x', style='sci', scilimits=(0,100),fontsize=14)
	    subplots_adjust(hspace=0)
    	    plt.setp(ax1.get_xticklabels(), visible=False)
#ax1.fill_between(x_smooth,y_smooth2,where=y_smooth2>=d,interpolate=True,color="r")
	plt.setp(ax1.get_xticklabels(), visible=True)
	#ax1.ticklabel_format(axis='x', style='sci', scilimits=(1,8))
#plt.setp([a.get_xticklabels() for a in axes[:-1]], visible=False)
	plt.xlabel(array2[k]+" "+str(array1[k]))
	fig.savefig(str(array2[k])+'.pdf')
        #plt.show()

