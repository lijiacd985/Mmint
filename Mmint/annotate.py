import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from pybedtools import BedTool
import pybedtools
import os
import subprocess
import subprocess
import argparse
plt.style.use('seaborn-white')

def run(parser):
    args = parser.parse_args()

    bedfile = args.bedfile
    reference = args.reference

    targetbed = pybedtools.BedTool(args.bedfile)
    if args.genome and args.genome!='':
        targetbed.set_chromsizes(args.genome)
    num = []
    shufnum = []
    for i, b in enumerate(reference):
        bed = pybedtools.BedTool(b)
        t = targetbed.intersect(bed, wo=True)
        num.append(len(t))
        t.saveas('intersect'+args.label[i]+'.bed')
        if args.genome and args.genome!='':
            shuf_t = targetbed.randomstats(bed, iterations=100, shuffle_kwargs={'chrom': True})
            shufnum.append(shuf_t['median randomized'])
    
    labels = args.label
    sizes = np.array(num)
    opacity=0.4
    bar_width=0.25
    index=np.arange(len(labels))
    #print(labels, num, index-bar_width/2)
    plt.bar(index-bar_width/2,sizes,bar_width,alpha=opacity,color='b',label="Sample")
    plt.bar(index+bar_width/2,shufnum,bar_width,alpha=opacity,color='orange',label="Random regions")
    plt.xticks(index,labels)
    plt.ylabel('Number of Regions')
    plt.legend(loc="center left", bbox_to_anchor=(1.04,0.5))
    plt.savefig(args.output+".pdf", bbox_inches="tight")


if __name__=="__main__":
    parser = argparse.ArgumentParser() 
    parser.add_argument('-b','--bedfile',help="bedfile to annotate", metavar="FILE")
    parser.add_argument('-r','--reference',help="Bed files as reference to annotate.",nargs="*")
    parser.add_argument('-g','--genome',help="Version of reference region. Such as: mm10, hg19..")
    parser.add_argument('-o','--output',help="the output file", metavar="FILE")
    parser.add_argument('-l','--label',help="Labels for reference bed files.", nargs='*')
    run(parser)
