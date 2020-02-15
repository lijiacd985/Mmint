#!/usr/bin/env python    
import matplotlib
matplotlib.use('Agg')
from mpl_toolkits.mplot3d import Axes3D
import mpl_toolkits.mplot3d.art3d as a3d
import matplotlib.pyplot as plt
import numpy as np
import os,sys
import argparse
from io import StringIO
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
import itertools
import pandas as pd
plt.style.use('ggplot')
from pybedtools import BedTool
import pybedtools
import subprocess
#from Format import formdata
import seaborn as sns
sns.set(color_codes=True)
    
    
    
    #bedtools intersect -a m24vs3aKO.DMRs -b H3K4me3.m24.3aKO.fold2 -wo |grep -v e|bedtools groupby -i - -g 1,2,3,4 -c 8,9 -o mean,sum |awk 'OFS="\t"{print $1,$2,$3,$4,$5,$6/($3-$2)}' > m24.3aKO.DMRs-H3K4me3
'''    
    parser = argparse.ArgumentParser()
    parser.add_argument('-DMRs','--DMRs',help="the file include DMRs and diff mCG/CG value",metavar="FILE")
    parser.add_argument('-histRs','--DiffHistPeaks',help="the file include diff histone peaks and fold change",metavar="FILE")
    parser.add_argument('-o','--outFile',help="output file name",metavar="FILE")
    args = parser.parse_args()
'''
def run(parser):
    x1=[]
    y1=[]
    z1=[]
    args=parser.parse_args()    
    subprocess.call("bedtools intersect -a  %s -b %s -wo |grep -v e|bedtools groupby -i - -g 1,2,3,4 -c 8,9 -o mean,sum |awk '{print $1,$2,$3,$4,$5,$6/($3-$2)}'| sed 's/ /\t/g' > DMRs-Histone.diff" % (args.DMRs,args.DiffHistPeaks),shell=True)
    
    try:
        formatfile1=open("DMRs-Histone.diff",'r')
    except IOError:
        print('cannot open', filename, file=sys.stderr)
        raise SystemExit
    for line in formatfile1:
        rows=line.strip().split("\t")
        x1.append(rows[3])
        y1.append(rows[4])
        z1.append(rows[5])
    arrayx=[float(m) for m in x1]
    arrayy=[np.log2(float(m)) for m in y1]
    arrayz=[float(m) for m in z1]
    
    mean_x= np.mean(arrayx)
    mean_y= np.mean(arrayy)
    mean_z= np.mean(arrayz)
    
    #print mean_x
    #print mean_y
    #print mean_z
    
    
    fig = plt.figure()
    #ax = fig.gca(projection='3d')
    #for c,m in [('r','o'),('b','^')]:
     #   ax = fig.gca(projection='3d')
    #ax = fig.add_subplot(111, projection='3d')
    ax = Axes3D(fig)
    ax.scatter(arrayx, arrayy, arrayz, c='b', marker='^')
    ax.scatter(arrayx, arrayy, zs=0,marker='x',c='r', zdir='z')
    ax.scatter(arrayx, arrayz, zs=4.5,marker='x',c='k', zdir='y')
    ax.scatter(arrayy, arrayz, zs=-1,marker='x',c='g', zdir='x')
    #ax.plot(arrayx, arrayz, 'r+', zdir='y', zs=4.5)
    ax.plot(arrayy, arrayz, 'g+', zdir='x', zs=-1)
    l1=a3d.Line3D((0,0,0),(4,0,0),(0,0,0),c='k',ls='--')
    l2=a3d.Line3D((0,0,-0.5),(0,0,0),(0,0,0),c='g',ls='--')
    l3=a3d.Line3D((0,0,0),(0,0,0),(0,0.2,0),c='r',ls='--')
    ax.add_line(l1)
    ax.add_line(l2)
    ax.add_line(l3)
    ax.add_line(l3)
    ax.set_xlim([-1, 1])
    ax.set_ylim([-12.5, 4.5])
    ax.set_zlim([0, 1])
    
    
    ax.set_xlabel('mCG/CG(WT-3aKO)')
    ax.set_ylabel('H3K4me3.Log2(WT/3aKO)')
    ax.set_zlabel('Overlap Ratio')
    fig.savefig(args.outFile+".png")
    #plt.show()
if __name__=="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-DMRs','--DMRs',help="the file include DMRs and diff mCG/CG value",metavar="FILE")
    parser.add_argument('-histRs','--DiffHistPeaks',help="the file include diff histone peaks and fold change",metavar="FILE")
    parser.add_argument('-o','--outFile',help="output file name",metavar="FILE")
    scatter3d(parser)
