#!/usr/bin/env python


import numpy as np
import os,sys
import argparse
from io import StringIO
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
import itertools
import pandas as pd
from math import log
import seaborn as sns
import subprocess


#sns.set(font_scale=1.5)


#ratio=[]
#cov=[]
#sum=[]
if __name__=="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-m','--methfile',help="The output from mcall: *.G.bed",nargs="*", metavar="FILE")
    parser.add_argument('-l','--label',help="The labels",nargs="*", metavar="FILE")
    parser.add_argument('-o','--output',help="The output file",nargs="*", metavar="FILE")
    run(parser)
#args = parser.parse_args()
#print args.methfile


'''
try:
	methfile=open(args.methfile,'r')
except IOError:
        print >>sys.stderr, 'cannot open', filename
        raise SystemExit
next(methfile)


with open("tmp", "w") as outfile:
    for i in range(len(args.methfile)):
        subprocess.call("cut -f1-5 %s| sed '1d'" % args.methfile[i], shell=True,stdout=outfile)

#for i in range(len(args.methfile)):
    methfile=open("tmp",'r')
    next(methfile)
    for line1 in methfile:
	rows1=line1.strip().split("\t")
	ratio.append(float(rows1[3]))
	#cov.append(int(rows1[4]))

    ax=sns.kdeplot(np.array(ratio),shade=False,color=c[i],label=args.label[i])
    plt.xlabel('Methylation Ratio')
    plt.ylabel('Density')
    plt.xlim(0,1)
    fig = ax.get_figure()
    ratio=[]

subprocess.call("rm tmp", shell=True)

fig.savefig(args.output[0]+"-Ratio.pdf")
'''
def run(parser):
    args = parser.parse_args()
    sns.set(font_scale=1.5)
    ratio=[]
    cov=[]
    sum=[]
    c=['r','b','g','y','k','c','m']
    fig,ax = plt.subplots()
    plt.xlim(0,11)
    t=[]
    #with open("tmp", "w") as outfile:
    for i in range(len(args.methfile)):
        with open("tmp", "w") as outfile:
            subprocess.call("cut -f1-5 %s | sed '1d'" % args.methfile[i], shell=True,stdout=outfile)
        methfile=open("tmp",'r')
        next(methfile)
        for line1 in methfile:
            rows1=line1.strip().split("\t")
            #ratio.append(float(rows1[3]))
            cov.append(int(rows1[4]))
        #a=[1,2,3,4,5,6]
        b=[]
        s=[]
        S=0
        St=0

        #print cov
        for n in range(10):
            for x in cov:
	        St+=x
                if (x>=2**n):
                    S+=x
            #print St
            #print S
            s.append(int(S)/float(St)*100)
            St = 0
        #   print b
            S=0
        t.append(s)
        cov=[]
        s=[]
        subprocess.call("rm tmp", shell=True)


#print t[1]

    for i in range(len(args.methfile)):
        xaxis=[1,2,3,4,5,6,7,8,9,10]
        labels=[1,2,4,8,16,32,64,128,256,512]
        plt.plot(xaxis,t[i],'-o',color=c[i],label=args.label[i])
        plt.legend(loc="lower left")
    plt.axvline(x=100,color='red',linewidth=2,linestyle='dashed')
    plt.xticks(xaxis, labels)
    plt.xlabel('Coverage (>=)')
    plt.ylabel('Wig sum for selected CpGs (Percentage)')

    fig.savefig(args.output[0]+"-Cov.pdf")
