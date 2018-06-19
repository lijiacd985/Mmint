#!/usr/bin/env python


import numpy as np
import os,sys
import argparse
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
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
def run(parser):
    args = parser.parse_args()
    for i in range(len(args.methfile)):
        subprocess.call("sed -n '27,48p' %s | cut -f1,3,8 | sed 's/NA/0/g'| sed 's/(genome)//g' | sed '1,2d'> %s\.cov" % (args.methfile[i],args.methfile[i]), shell=True)


    linestyles = ['-', '--', '-.', ':']

    color=iter(cm.rainbow(np.linspace(0,1,len(args.methfile))))
    fig,ax1 = plt.subplots()
    for i in range(len(args.methfile)):
        m=pd.read_table(args.methfile[i]+".cov",header=None)
        c=next(color)
        ax2 = ax1.twinx()
        ax1.plot(m[0],m[2],c=c,label=args.label[i],marker="^")
        #ax2.plot(m[0],m[1]/28217448*100,marker="^",linestyle=linestyles[1],c=c)
        ax2.plot(m[0],m[1]/1000000,marker="P",linestyle=linestyles[2],c=c)
    	#ax2.plot(m[0],m[1],linestyle=linestyles[1],c=c)
        #ax1.legend(loc="center right",fontsize=10)
        #ax2.yaxis.set_visible(False)
        ax2.set_ylim([0,30])#ax2.legend()
    #	legend.append(args.label[i])
    #ax1.text(18, 1.0, 'Total CpG sites : 28217448',verticalalignment='top', horizontalalignment='right',transform=ax.transAxes,color='red', fontsize=15)
    #ax2.yaxis.set_ticks_position('none')
    #ax2.yaxis.set_visible(False)
    #plt.legend(n,legend,ncol=1,loc='upper right')
    #ax2.set_yticklabels([])
    ax1.legend(loc="center right",fontsize=10)
    #ax1.text(10, 0.95, 'Total CpG sites (hg19) : 28217448',color='black', fontsize=10)
    ax1.set_ylim([0,1])
    ax1.set_xlim([-1,26])
    #ax2.set_ylim([0,100])
    #ax2.set_yticklabels(["1000","90","80","70","60","50","40","30","20","10"])
    ax1.set_ylabel('Mean CpG Meth Ratio(-)')
    ax2.set_ylabel('Million of CpG sites(---)')
    ax1.set_xlabel('Depth')
    #ax2.yaxis.set_visible(False)
    #plt.show()
    plt.savefig(args.output)
