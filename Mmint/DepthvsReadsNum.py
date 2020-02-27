import numpy as np
import os,sys
import argparse
from io import StringIO
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
import itertools
import pandas as pd
from math import log
import seaborn as sns
from matplotlib.pyplot import cm
import time
plt.style.use('seaborn-white')


def run(parser):
    args = parser.parse_args()
    sns.set(font_scale=1.5)
    ratio=[]
    cov=[]
    sum=[]
    color=iter(cm.rainbow(np.linspace(0,1,len(args.methfile))))
    fig,ax = plt.subplots()
    plt.xlim(0,11)
    t=[]
    for i in range(len(args.methfile)):

        with open(args.methfile[i]) as f:
            for line in f:
                if line[0]=='#': continue
                c = line.strip().split()
                cov.append(int(c[4]))

        s=[]
        S=0
        St=0

        for n in range(10):
            for x in cov:
                St+=x
                if (x>=2**n):
                    S+=x
            s.append(int(S)/float(St)*100)
            St = 0
            S=0
        t.append(s)
        cov=[]
        s=[]

    c=['r','b','g','y','k','c','m','sienna','lightsalmon','darkorange','darkgoldenrod','yellowgreen','skyblue','seagreen','fuchsia','orchid','stateblue','cyan']
    for i in range(len(args.methfile)):
        xaxis=[1,2,3,4,5,6,7,8,9,10]
        labels=[1,2,4,8,16,32,64,128,256,512]
        plt.plot(xaxis,t[i],'-o',color=c[i],label=args.label[i])
    plt.legend(loc="center left", bbox_to_anchor=(1.04, 0.5))
    plt.axvline(x=100,color='red',linewidth=2,linestyle='dashed')
    plt.xticks(xaxis, labels)
    plt.xlabel('Coverage (>=)')
    plt.ylabel('Wig sum for selected CpGs (%)')

    fig.savefig(args.output+".pdf", bbox_inches="tight")

if __name__=="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-m','--methfile',help="The output from mcall: *.G.bed",nargs="*", metavar="FILE")
    parser.add_argument('-l','--label',help="The labels",nargs="*", metavar="FILE")
    parser.add_argument('-o','--output',help="Prefix of output PDF file", metavar="FILE")
    run(parser)



