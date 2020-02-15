#!/usr/bin/env python
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

#parser = argparse.ArgumentParser()
#parser.add_argument('-b','--bedfile',help="bedfile to annotate", metavar="FILE")
#parser.add_argument('-o','--output',help="the output file", metavar="FILE")
def run(parser):
    args = parser.parse_args()
    realpath = os.path.realpath(__file__)
    realpath = realpath[:realpath.rfind('/')+1]
    targetbed = pybedtools.BedTool(args.bedfile)

    genebed = pybedtools.BedTool(realpath+'hg19.gene.bed')# closest gene bed

    bed1 = pybedtools.BedTool(realpath+'hg19.exon.bed')
    bed2 = pybedtools.BedTool(realpath+'hg19.Introns.bed')
    bed3 = pybedtools.BedTool(realpath+'hg19.cpgIsland.bed')
    bed4 = pybedtools.BedTool(realpath+'hg19.5UTR.bed')
    bed5 = pybedtools.BedTool(realpath+'hg19.3UTR.bed')
    bed6 = pybedtools.BedTool(realpath+'hg19.RepeatMask2.bed')
    bed7 = pybedtools.BedTool(realpath+'hg19.intergenic.bed')

    #targetbed closest gene
    targetbed.closest(genebed),saveas('closestGENE.bed')

    targetbed.intersect(bed1,wao=True).saveas('intersectExon.bed',trackline="track name='reads in exons' color=128,0,0")

    peak=[]
    with open("intersectExon.bed") as f:
    	next(f)
    	for line in f:
    		line = line.strip().split()
    		#if int(line[11]) >0:
    		if int(line[-1]) >=1:
    			#w.write(line[3]+'\n')
    			peak.append(line[0]+line[1]+line[2])
    exon_num = len(np.unique(peak))

    targetbed.intersect(bed2,wao=True).saveas('intersectIntrons.bed',trackline="track name='reads in Introns' color=128,0,0")
    peak=[]
    with open("intersectIntrons.bed") as f:
            next(f)
            for line in f:
                    line = line.strip().split()
                    #if int(line[11]) >1:
                    if int(line[-1]) >=1:
    		       #w.write(line[3]+'\n')
                            peak.append(line[0]+line[1]+line[2])
    intron_num = len(np.unique(peak))


    targetbed.intersect(bed3,wao=True).saveas('intersectCpGisland.bed',trackline="track name='reads in cpgIsland' color=128,0,0")
    peak=[]
    with open("intersectCpGisland.bed") as f:
            next(f)
            for line in f:
                line = line.strip().split()
                if int(line[-1]) >1:
                    peak.append(line[0]+line[1]+line[2])
    cpgIsland_num = len(np.unique(peak))

    targetbed.intersect(bed4,wao=True).saveas('intersect5UTR.bed',trackline="track name='reads in 5UTR' color=128,0,0")
    peak=[]
    with open("intersect5UTR.bed") as f:
            next(f)
            for line in f:
                    line = line.strip().split()
                    #if int(line[11]) >=1:
                    if int(line[-1]) >=1:
     		       #w.write(line[3]+'\n')
                            peak.append(line[0]+line[1]+line[2])
    UTR5_num = len(np.unique(peak))


    targetbed.intersect(bed5,wao=True).saveas('intersect3UTR.bed',trackline="track name='reads in 3UTR' color=128,0,0")
    peak=[]
    with open("intersect3UTR.bed") as f:
            next(f)
            for line in f:
                line = line.strip().split()
                if int(line[-1]) >=1:
                    peak.append(line[0]+line[1]+line[2])
    UTR3_num = len(np.unique(peak))

    targetbed.intersect(bed6,wao=True).saveas('intersectRepeatMask.bed',trackline="track name='reads in RepeatMask' color=128,0,0")
    peak=[]
    with open("intersectRepeatMask.bed") as f:
            next(f)
            for line in f:
                line = line.strip().split()
                if int(line[-1]) >=1:
                    peak.append(line[0]+line[1]+line[2])

    RepeatMask_num = len(np.unique(peak))

    targetbed.intersect(bed7,wao=True).saveas('intersectIntergenic.bed',trackline="track name='reads in Intergenic' color=128,0,0")
    peak=[]
    with open("intersectIntergenic.bed") as f:
            next(f)
            for line in f:
                line = line.strip().split()
                if int(line[-1]) >=1:
                    peak.append(line[0]+line[1]+line[2])
    Intergenic_num = len(np.unique(peak))


    labels = 'Exon', 'Intron', 'CpGIsland', '5UTR', '3UTR', 'RepeatMask','Intergenic'
    #sizes = [exon_num, intron_num, cpgIsland_num, UTR5_num, UTR3_num, RepeatMask_num] ##generate an array of percents
    sizes=(exon_num, intron_num, cpgIsland_num, UTR5_num, UTR3_num, RepeatMask_num, Intergenic_num)
    #max = max([float(n) for n in sizes])
    #sizes.index(max)

    #colors = ['gold', 'yellowgreen', 'lightcoral', 'lightskyblue','pink','red']
    #explode = np.empty(6,dtype=float)
    #explode.fill(0)
    #explode[sizes.index(max)] = 0.2
    #plt.pie(sizes, explode=explode, labels=labels, colors=colors,
    #        autopct='%1.1f%%', shadow=True, startangle=140)

    #plt.axis('equal')
    opacity=0.4
    bar_width=0.5
    index=np.arange(1,8)
    plt.bar(index+bar_width/2,sizes,bar_width,alpha=opacity,color='b')
    plt.xticks(index+bar_width/2,('Exon','Intron','CpGIsland','5-UTR','3-UTR','Repeat','Intergenic'))
    plt.ylabel('Number of Regions')
    #plt.show()
    plt.savefig(args.output+".pdf")
