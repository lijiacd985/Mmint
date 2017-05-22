#!/usr/bin/env python


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


hash={}
chiphash={}
start1=[]
end1=[]
num1=[]
start2=[]
end2=[]
num2=[]
key=[]
value=[]
chipkey=[]
chipvalue=[]
x=[]
y=[]
a=[]
n=[]
total=[]
dic={}
chrlist1=[]
chrlist2=[]


parser = argparse.ArgumentParser()
parser.add_argument('-m','--methfile',help="input methylation Ratio file (the output file from mcall) ", metavar="FILE")
parser.add_argument('-p','--peakfile',help="input peaks signal file (bedgraph format) ", metavar="FILE")
parser.add_argument('-o','--output',help="output file name pre-index", metavar="FILE")
args = parser.parse_args()

'''
The inputs for this script both are bedgraph, one is for meth signals and the other input is for chipseq signals.
This script is mapping the chipseq signals to meth signal based on the sites and generate the scatter with xaxis
represent the meth ratio and yaxis represent the chipseq ratio.

'''


targetbed = pybedtools.BedTool(args.peakfile)
bed1 = pybedtools.BedTool(args.methfile)
#subprocess.call("awk '{if($5!=".")print}' intersect.bed"
targetbed.intersect(bed1,wo=True).saveas('intersect.bed')

with open (args.peakfile + "meth.bed","w") as f:
##Extract the CpGs locate in ChiPSeq peaks regions:	
	subprocess.call('bedtools groupby -i intersect.bed -g 1,2,3 -c 4,8 -o mean,mean',stdout=f,shell=True)
##Calculate the mean methylation ration for each ChIPSeq peaks
with open ("tmp","w") as f2:
       subprocess.call("bedtools groupby -i intersect.bed  -g 1,2,3 -c 4,8 -o mean,mean | awk '{a[$5]+=$4;n[$5]+=1}END{for (b in a){print b,a[b]/n[b]}}'",stdout=f2,shell=True)
try:
	formatfile=open("tmp",'r')
except IOError:
        print >>sys.stderr, 'cannot open', filename
        raise SystemExit


for line in formatfile:
    rows=line.strip().split(" ")
#    for i in np.arange(0,1,0.05):
#        if rows[4] <=i+0.05 and rows[4]>i:
#	    a.append(rows[3])
#    else:
#        a.append(0)
#total.append(a)
#a = []
    x.append(rows[0])
    y.append(rows[1])

try:
        formatfile2=open(args.peakfile + "meth.bed",'r')
except IOError:
        print >>sys.stderr, 'cannot open', filename
        raise SystemExit
for line in formatfile2:
    rows=line.strip().split("\t")
    n.append(rows[4])
##plot
fig,ax1 = plt.subplots()
ax2 = ax1.twinx()

ax1.grid(False)
ax2.grid(False)
#ax1.set_axis_bgcolor('grey')
#plt.patch.set_facecolor('grey')

ax1.hist([float(z) for z in n],facecolor='green',bins=40,bottom=0, weights=np.zeros_like(np.array([float(z) for z in n]))+100./len([float(z) for z in n]),align='mid',alpha=0.9)
ax1.set_xlabel('Methylation Ratio')
ax1.set_ylabel('Frequency',color="green")
ax1.set_xlim((-0.05,1.05))
#ax1.set_ylim((0,16))

d = {m:n for m,n in zip(x,y)}
#d = {}
#for (k,v) in zip(x,y):
#    d.setdefault(k,[]).append(v) #or whatever your function needs to be to combine them

#k = list(zip(x, y))
#print k
#n=[]
#for (x,y) in k:
#    if x in d:
#        n.append(d[x])
#        d[x] = float(d[x]) +float(y) #or whatever your function needs to be to combine them
#        d[x] = float(d[x])/len(n)
#    else:
# #       d[x] = float(y)
#    n=[]
##set 0.05 as step size and store the ChIPSeq signals in each interval to one vector, total 20 vectors.
for i in np.arange(0,1,0.05):
        for key in d.keys():
            if float(key)<i+0.05 and float(key)>=i:
                a.append((float(d[key])))
        else:
             a.append(0)
        total.append(a)	
        a=[]


##calculate the mean ChIPSeq signals for each interval.
m=[]
for i in total:
    m.append(np.mean(i))

rotate90 = zip(*total[::-1])
#print len(rotate90) 
#df = pd.DataFrame(np.random.rand(10, 5), columns=['A', 'B','C','D','E'])
#print (np.random.rand(10,5))

df = pd.DataFrame(rotate90,columns=['5%', '10%','15%','20%','25%','30%','35%','40%','45%','50%','55%','60%','65%','70%','75%','80%','85%','90%','95%','100%'])
#print df.shape[0]
#print df.shape[1]
#df2 = df.mean(axis = 0)
#print df2
x2 = [0.05,0.1,0.15,0.2,0.25,0.3,0.35,0.4,0.45,0.5,0.55,0.6,0.65,0.7,0.75,0.8,0.85,0.9,0.95,1]
#ax2.plot(x2,df2,'-o',color="red")
#plt.show()
#color = dict(boxes='DarkGreen', whiskers='DarkOrange',medians='DarkBlue', caps='Gray')
#plt.show()
##plot curve
ax2.plot(x2,m,'-o',color="red")
ax2.set_ylabel('Chip-seq Signal',color="red")
ax2.set_ylim((0,max(m)+1))
#ax2.set_ylim(0,1)
#plt.show()
#fig=pic.get_figure()
fig.savefig(args.output+".pdf")
#usage: python map_meth2peak.test4.py -m test2 -p chipseqtest
