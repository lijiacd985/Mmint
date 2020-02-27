#!/usr/bin/env python
import numpy as np
import os,sys
import argparse
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
plt.style.use('seaborn-white')
from matplotlib.pyplot import cm
import pandas as pd
import subprocess
'''
parser = argparse.ArgumentParser()
parser.add_argument('-m','--methfile',help="The output *stat.txt from mcall",nargs="*",metavar="FILE")
parser.add_argument('-l','--label',help="Labels for samples",nargs="*",metavar="FILE")
parser.add_argument('-o','--output',help="The output file: *.pdf, *.png...", metavar="FILE")
args = parser.parse_args()
#print args.methfile
#try:
#	methfile=open(args.methfile,'r')
#except IOError:
#        print >>sys.stderr, 'cannot open', filename
#        raise SystemExit
'''

def mdepth_reader(filename):
    with open(filename) as f:
        lines = f.readlines()
    lines = lines[-21:]
    cg_num, cg_ratio = [],[]
    for line in lines:
        c = line.strip().split()
        cg_num.append(int(c[2]))
        if c[7]=='NA':
            cg_ratio.append(0)
        else:
            cg_ratio.append(float(c[7]))
    return np.array(cg_num)/1000000.0, np.array(cg_ratio)

def run(parser):
    args = parser.parse_args()
    linestyles = ['-', '--', '-.', ':']

    color=iter(cm.rainbow(np.linspace(0,1,len(args.methfile))))
    fig,ax1 = plt.subplots()
    x_value = [i for i in range(21)]
    for i, filename in enumerate(args.methfile):
        cg_num, cg_ratio = mdepth_reader(filename)
        c=next(color)
        ax2 = ax1.twinx()
        ax1.plot(x_value,cg_ratio,c=c,label=args.label[i])
        ax2.plot(x_value,cg_num,linestyle=(0, (5, 10)),c=c)
        ax2.set_ylim([0,30])
    ax1.legend(bbox_to_anchor=(1.10,0.5), loc="center left", borderaxespad=0,fontsize=10)
    ax1.set_ylim([0,1])
    ax1.set_xlim([-1,26])
    ax1.set_ylabel('Mean CpG Meth Ratio(-)')
    ax2.set_ylabel('Million of CpG sites(---)')
    ax1.set_xlabel('Depth')
    plt.savefig(args.output+'.pdf', bbox_inches="tight")

if __name__=="__main__":
    argparser = argparse.ArgumentParser()
    argparser.add_argument('-m','--methfile',help="The output *stat.txt from mcall",nargs="*",metavar="FILE")
    argparser.add_argument('-l','--label',help="Labels for samples",nargs="*",metavar="FILE")
    argparser.add_argument('-o','--output',help="The output file: *.pdf, *.png...", metavar="FILE")
    run(argparser)

