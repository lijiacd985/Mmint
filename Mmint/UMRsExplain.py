#!/usr/bin/env python
    
import matplotlib
matplotlib.use('Agg')   
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
import matplotlib.pyplot as plt
plt.style.use('seaborn-deep')
    
    
'''    
    parser = argparse.ArgumentParser()
    parser.add_argument('-i','--UMRsFile',help="UMRs file output from Mmint", metavar="FILE")
    parser.add_argument('-1','--annotateFile1',help="annotate bed file1", metavar="FILE")
    parser.add_argument('-2','--annotateFile2',help="annotate bed file2", metavar="FILE")
    parser.add_argument('-o','--output',help="output file name pre-index", metavar="FILE")
    args = parser.parse_args()
'''
    
def run(parser):
    x1=[]
    y1=[]
    array=[]
    args = parser.parse_args()    
    #subprocess.call("cat %s %s|bedtools sort > tmp0" % (args.UMRsFile,args.annotateFile1),shell=True)
    #subprocess.call("bedtools merge -i tmp0 > merge.UMRs",shell=True)
    subprocess.call("bedtools intersect -a %s -b %s -wao | bedtools groupby -g 1,2,3 -c 10 -o sum > tmp1" % (args.UMRsFile,args.annotateFile1), shell=True)
    
    args1 = ["awk", r'{OFS="\t"; if($7!=".")print $1,$2,$3,$NF/($3-$2)*100;else print $1,$2,$3,0}', "tmp1"]
    
    with open("UMRs1","w") as out1:
        subprocess.call(args1, stdout=out1)
    subprocess.call("bedtools intersect -a %s -b %s -wao | bedtools groupby -g 1,2,3 -c 10 -o sum > tmp2" % (args.UMRsFile,args.annotateFile2), shell=True)
    args2 = ["awk", r'{OFS="\t"; if($7!=".")print $1,$2,$3,$NF/($3-$2)*100;else print $1,$2,$3,0}', "tmp2"]
    with open("UMRs2","w") as out2:
        subprocess.call(args2, stdout=out2)
    subprocess.call("paste UMRs1 UMRs2 |cut -f1-4,8 >UMRs.ratio",shell=True)
    
    try:
       formatfile1=open("UMRs.ratio",'r')
    except IOError:
       print('cannot open', filename, file=sys.stderr)
       raise SystemExit
    for line in formatfile1:
       rows=line.strip().split("\t")
       x1.append(rows[3])
       y1.append(rows[4])
    #print x1
    #array = [[float(z) for z in k] for k in x1]
    #array2=[float(m) for m in y1] 
    x1=[float(m) for m in x1]
    y1=[float(n) for n in y1]
    #print array
    #merge = pd.DataFrame(array,columns=["x","y"])
       #g = sns.jointplot(x="y", y="x", data=merge,  kind="kde", color="m",n_levels=12)
    data = np.vstack([x1,y1]).T
    bins = np.linspace(0,100,25)
    plt.hist(data,bins,alpha=0.5,label=['H3K4me3','H3K27me3'])
    plt.legend(loc='upper center')
    plt.ylabel('Number of UMRs')
    plt.xlabel('% UMRs Explained')
    #plt.savefig("hist.pdf")
    plt.savefig(args.output+".pdf")
    
if __name__=="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-i','--UMRsFile',help="UMRs file output from Mmint", metavar="FILE")
    parser.add_argument('-1','--annotateFile1',help="annotate bed file1", metavar="FILE")
    parser.add_argument('-2','--annotateFile2',help="annotate bed file2", metavar="FILE")
    parser.add_argument('-o','--output',help="output file name pre-index", metavar="FILE")
    UMRsExplain(parser)

