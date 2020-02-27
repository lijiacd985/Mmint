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
import pandas as pd
plt.style.use('ggplot')
#from Format import formdata
import seaborn as sns
import pybedtools
sns.set(color_codes=True)
    
    
    
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
    peak_f = pybedtools.BedTool(args.DMRs)
    methy_f = pybedtools.BedTool(args.DiffHistPeaks)
    inter_f = peak_f.intersect(methy_f, wo=True, stream=True)
    d = inter_f.groupby(g=[1,2,3,4], c=[8,9], o=['mean', 'sum'])
    
    arrayx, arrayy, arrayz= [], [], []
    for line in d:
        arrayx.append(float(line[3]))
        arrayy.append(np.log2(float(line[4])))
        arrayz.append(float(line[5])/(float(line[2])-float(line[1])))

        
    
    #subprocess.call("bedtools intersect -a  %s -b %s -wo |grep -v e|bedtools groupby -i - -g 1,2,3,4 -c 8,9 -o mean,sum |awk '{print $1,$2,$3,$4,$5,$6/($3-$2)}'| sed 's/ /\t/g' > DMRs-Histone.diff" % (args.DMRs,args.DiffHistPeaks),shell=True)
    '''
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
    '''
    mean_x= np.mean(arrayx)
    mean_y= np.mean(arrayy)
    mean_z= np.mean(arrayz)
    
    
    
    fig = plt.figure()
    ax = Axes3D(fig)
    ax.scatter(arrayx, arrayy, arrayz, c='b', marker='^')
    ax.scatter(arrayx, arrayy, zs=0,marker='x',c='r', zdir='z')
    ax.scatter(arrayx, arrayz, zs=4.5,marker='x',c='k', zdir='y')
    ax.scatter(arrayy, arrayz, zs=-1,marker='x',c='g', zdir='x')
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
    
    
    ax.set_xlabel('mCG/CG')
    ax.set_ylabel('Signal(log2)')
    ax.set_zlabel('Overlap Ratio')
    fig.savefig(args.outFile+".pdf", bbox_inches="tight")

if __name__=="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-DMRs','--DMRs',help="the file include DMRs and diff mCG/CG value",metavar="FILE")
    parser.add_argument('-histRs','--DiffHistPeaks',help="the file include diff histone peaks and fold change",metavar="FILE")
    parser.add_argument('-o','--outFile',help="output file name",metavar="FILE")
    run(parser)
