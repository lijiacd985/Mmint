import argparse
import matplotlib
matplotlib.use('Agg')
import pandas as pd
import numpy as np
import os
from matplotlib import pyplot as plt
import pybedtools as pb
from scipy.stats import pearsonr,spearmanr
plt.style.use('seaborn-white')

def run(parser):
    args = parser.parse_args()
    reffile=args.reference
    path = os.path.abspath(__file__)
    path = path[:path.rfind('/')]+'/BED'
    if args.reference=='hg19':
        reffile = path+'/hg19.tss.bed'
    elif args.reference=='mm10':
        reffile = path+'/mm10.tss.bed'
    elif not os.path.exists(args.reference):
            raise Exception(args.reference+" not exists!")
    ref = pb.BedTool(reffile)
    meth = pb.BedTool(args.methfile)
    methtss = ref.window(meth,l=args.upstream,r=args.downstream).groupby(g=[1,2,3,4,5,6],c=9,o=['mean'])
    with open(args.RNAseq) as f:
        lines = f.readlines()
    dic={}
    for line in lines:
        t = line.strip().split()
        dic[t[0]]=[float(t[1])]
    for m in methtss:
        if m[4] in dic:    #postion of genename
            dic[m[4]].append(float(m[-1]))
    plt.figure()
    rexp=[]
    mlevel=[]
    for d in dic:
        if len(dic[d])!=2: continue
        rexp.append(dic[d][0])
        mlevel.append(dic[d][1])
    rexp = np.array(rexp)
    mlevel = np.array(mlevel)
    pos=np.where(rexp>-100)
    mlevel=mlevel[pos]
    rexp=rexp[pos]
    rexp = np.log(rexp+1)/np.log(10)
    max_exp = np.max(rexp)
    min_exp = np.nanmin(rexp)
    max_mlevel = np.max(mlevel)
    min_mlevel = np.min(mlevel)
    plt.scatter(mlevel,rexp,c='b',alpha=0.1)
    plt.ylim(min_exp*1.03,max_exp*1.03)
    plt.xlim(min_mlevel*1.05,max_mlevel*1.05)
    plt.xlabel(args.xaxislabel)
    plt.ylabel(args.yaxislabel)
    spearman,p1 = spearmanr(rexp,mlevel)
    pearson,p2 = pearsonr(rexp,mlevel)
    geneNum = len(rexp)

    from decimal import Decimal
    s1='Spearman correlation Coefficient: '+str(Decimal(str(spearman)).quantize(Decimal('0.000'))) + ' p-value: '+str(Decimal(str(p1)).quantize(Decimal('0.000')))
    s2='Pearson correlation Coefficient: '+str(Decimal(str(pearson)).quantize(Decimal('0.000'))) + ' p-value: '+str(Decimal(str(p2)).quantize(Decimal('0.000')))
    s3='Total Genes:' +str(geneNum)
    plt.text(min_mlevel,max_exp*0.9,s3)
    plt.text(min_mlevel,max_exp*1.1,s2)
    plt.text(min_mlevel,max_exp*1.05,s1)
    plt.savefig(args.output+'.pdf', bbox_inches="tight")






if __name__=="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-m','--methfile',help="Bed files describe sample",required=True)
    parser.add_argument('-r','--reference',help="select from hg19/mm10 or the TSS region self defined",required=True)
    parser.add_argument('-u','--upstream',help='TSS upstream (default 1000bp)',type=int,default=1000)
    parser.add_argument('-d','--downstream',help="TSS downstream (default 1000bp)",type=int,default=1000)
    parser.add_argument('-R','--RNAseq',help="Expression information, format(\\t==Tab): Genename\\tExpression_level",required=True)
    parser.add_argument('-o','--output',help="output file name",required=True)
    parser.add_argument('-ylab','--yaxislabel',help="Yaxis Label, default='Expression level'",default='Expression level')
    parser.add_argument('-xlab','--xaxislabel',help="Xaxis Label, default='Methylation level'",default='Methylation level')
    run(parser)

