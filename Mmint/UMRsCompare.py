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
    parser.add_argument('-1','--UMRsFile1',help="UMRs file output from Mmint", metavar="FILE")
    parser.add_argument('-2','--UMRsFile2',help="UMRs file output from Mmint", metavar="FILE")
    parser.add_argument('-o','--output',help="output file name pre-index", metavar="FILE")
    args = parser.parse_args()
'''
    
def run(parser):
    x1=[]
    y1=[]
    array=[]
    args = parser.parse_args()    
    subprocess.call("cat %s %s|bedtools sort > tmp0" % (args.UMRsFile1,args.UMRsFile2),shell=True)
    subprocess.call("bedtools merge -i tmp0 > merge.UMRs",shell=True)
    subprocess.call("bedtools intersect -a merge.UMRs -b %s -wao|bedtools groupby -i - -g 1,2,3 -c 10 -o sum > tmp1" % (args.UMRsFile1), shell=True)
    
    #tmp1=subprocess.Popen('bedtools intersect -a merge.UMRs -b N.common.canyon -wao ',stdout=subprocess.PIPE,shell=True).communicate()[0]
    args1 = ["awk", r'{OFS="\t"; if($4!=".")print $1,$2,$3,$4/($3-$2)*100;else print $1,$2,$3,0}', "tmp1"]
    with open("mergeUMRsRatio1","w") as out1:
        subprocess.call(args1, stdout=out1)
    #tmp2=subprocess.Popen('bedtools intersect -a merge.UMRs -b T.common.canyon -wao',stdout=subprocess.PIPE,shell=True).communicate()[0]
    subprocess.call("bedtools intersect -a merge.UMRs -b %s -wao |bedtools groupby -i - -g 1,2,3 -c 10 -o sum> tmp2" % (args.UMRsFile2), shell=True)
    args2 = ["awk", r'{OFS="\t"; if($4!=".")print $1,$2,$3,$4/($3-$2)*100;else print $1,$2,$3,0}', "tmp2"]
    with open("mergeUMRsRatio2","w") as out2:
        subprocess.call(args2, stdout=out2)
    #subprocess.call("awk 'OFS="\t"{if($4!=".")print $1,$2,$3,$10/($3-$2)*100;else print $1,$2,$3,0}' tmp2 > merge.UMRs.Nratio",shell=True)
    subprocess.call("paste mergeUMRsRatio1 mergeUMRsRatio2 |cut -f1-4,8 > merge.UMRs.ratio",shell=True)
    
    try:
           formatfile1=open("merge.UMRs.ratio",'r')
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
    plt.hist(data,bins,alpha=0.5,label=[args.UMRsFile1,args.UMRsFile2])
    plt.legend(loc='upper center')
    plt.ylabel('Number of UMRs')
    plt.xlabel('% UMRs Explained')
    #plt.savefig("hist.pdf")
    plt.savefig(args.output+".pdf")
if __name__=="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-1','--UMRsFile1',help="UMRs file1 output from Mmint", metavar="FILE")
    parser.add_argument('-2','--UMRsFile2',help="UMRs file2 output from Mmint", metavar="FILE")
    parser.add_argument('-o','--output',help="output file name pre-index", metavar="FILE")
    UMRsCompare(parser)
