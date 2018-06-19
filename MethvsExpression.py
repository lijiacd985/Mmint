import argparse
import matplotlib
matplotlib.use('Agg')
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import pybedtools as pb
from scipy.stats import pearsonr,spearmanr

def run(parser):
    args = parser.parse_args()
    reffile=args.reference
    if args.reference=='hg19':
        reffile = './hg19.tss.bed'
    elif args.reference=='mm10':
        reffile = './mm10.tss.bed'
    ref = pb.BedTool(reffile)
    meth = pb.BedTool(args.bedfile)
    methtss = ref.window(meth,l=args.upstream,r=args.downstream).groupby(g=[1,2,3,4,5,6],c=10,o=['mean'])
    with open(args.RNAseq) as f:
        lines = f.readlines()
    dic={}
    for line in lines:
        t = line.strip().split()
        dic[t[0]]=[float(t[1])]
    for m in methtss:
        if m[3] in dic:    #postion of genename
            dic[m[3]].append(float(m[-1]))
    #print(dic)
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
    #rexp[np.where(rexp==0)]=0.01
    #low=np.sort(rexp)[len(rexp)//10]
##log transform the gene expression values    
    rexp = np.log(rexp+1)/np.log(10)
    max_exp = np.max(rexp)
    min_exp = np.nanmin(rexp)
    max_mlevel = np.max(mlevel)
    min_mlevel = np.min(mlevel)
    #i#print(low)
    #print(np.where(rexp>low)[0])
#    plt.plot(rexp,mlevel,'b.',alpha=0.2)
    #t = np.arange(len(rexp))
    plt.scatter(mlevel,rexp,c='b',alpha=0.1)
    #plt.colorbar()
#<<<<<<< HEAD
    #plt.xlim(0,15)
    plt.ylim(min_exp*1.03,max_exp*1.03)
    #plt.ylim(-1,1)
    plt.xlim(min_mlevel*1.05,max_mlevel*1.05)
    #plt.xlabel('Gene Expression Level (Log10)')
    #plt.ylabel('Methylation Ratio')
    plt.xlabel(args.xaxislabel)
    plt.ylabel(args.yaxislabel)
#=======
 #   plt.xlim(0,max_exp)
  #  plt.ylim(0,1)
   # plt.xlabel('Gene Expression Level')
   # plt.ylabel('Ratio')
#>>>>>>> ee2d90f8cae2348451a0949bf28b02bc12f2d1ae
#    plt.plot([0,np.max(rexp)],[1,0],'r-')
    spearman,p1 = spearmanr(rexp,mlevel)
    pearson,p2 = pearsonr(rexp,mlevel)
    geneNum = len(rexp)
    #print geneNum

#Decimal(str(r[j])).quantize(Decimal('0.00'))
    from decimal import Decimal
    s1='Spearman correlation Coefficient: '+str(Decimal(str(spearman)).quantize(Decimal('0.000'))) + ' p-value: '+str(Decimal(str(p1)).quantize(Decimal('0.000')))
    s2='Pearson correlation Coefficient: '+str(Decimal(str(pearson)).quantize(Decimal('0.000'))) + ' p-value: '+str(Decimal(str(p2)).quantize(Decimal('0.000')))
    s3='Total Genes:' +str(geneNum)
    #plt.text()
    #plt.text(0,1.1,s2)
    #plt.text(0,1.05,s1)
    plt.text(min_mlevel,max_exp*0.9,s3)
    plt.text(min_mlevel,max_exp*1.1,s2)
    plt.text(min_mlevel,max_exp*1.05,s1)
    plt.savefig(args.output+'.pdf')






if __name__=="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-m','--methfile',help="Bed files describe sample",required=True)
    parser.add_argument('-r','--reference',help="select from hg19/mm10 or the TSS region self defined",required=True)
    parser.add_argument('-u','--upstream',help='TSS upstream (default 1000bp)',type=int,default=1000)
    parser.add_argument('-d','--downstream',help="TSS downstream (default 1000bp)",type=int,default=1000)
    parser.add_argument('-R','--RNAseq',help="result, format(\t==Tab): Genename\tExpression_level",required=True)
    parser.add_argument('-o','--output',help="output file name",required=True)
    parser.add_argument('-ylab','--yaxislabel',help="Yaxis Label",required=True)
    parser.add_argument('-xlab','--xaxislabel',help="Xaxis Label",required=True)
    run(parser)

