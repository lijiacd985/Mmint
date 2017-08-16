import subprocess
from Genome_fasta import get_fasta
from matplotlib import pyplot as plt
import numpy as np

def run(parser):
    args = parser.parse_args()
    bases,chrs = get_fasta(args.genome)
    l={}
    for c in chrs:
        l[c]=len(bases[c])
    chrs = set(chrs)
    p = subprocess.Popen('bamToBed -i '+args.bamfile,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    reads_num=0
    reads_cg_num=[0,0,0] #CG,cg,Cg
    cgnum_per_read=[]

    for line in p.stdout:
        t = line.decode('utf-8').strip().split()
        chr = t[0]
        start=int(t[1])
        end=int(t[2])
        if not chr in chrs: continue
            #raise Exception("Bamfile contains chr which not in genome")
        #if start+length>l[chr]:
        #    raise Exception("Bamfile contains reads not in this genome")
        end=min(end+1,l[chr])
#        read=bases[chr]
#        ls=end-start
        reads_num+=1
        cg=[bases[chr].count('CG',start,end)+bases[chr].count('Cg',start,end),bases[chr].count('cG',start,end)+bases[chr].count('cg',start,end)]
        #print cg
#        for i in range(1,ls):
#            r2=read[i]
#            r1=read[i-1]
#            if 'G'==r2 or 'g'==r2:
#                if 'C'==r1: cg[0]+=1
#                if 'c'==r1: cg[1]+=1

        #count = int(cg[0]>0)+int(cg[1]>0)
        if cg[0]+cg[1]==0: continue
        #print cg
        cgnum_per_read.append(sum(cg))
        if cg[0]>0 and cg[1]>0:
            reads_cg_num[2]+=1
            continue
        if cg[0]>0:
            reads_cg_num[0]+=1
        else: reads_cg_num[1]+=1

    #print reads_cg_num
    #print reads_num

    plt.figure()
    plt.subplot(211)
    labels = ['noCG','NonRepeat CG','Repeat cg','CGcg mix']
    colors = ['r','b','g','y']
    explode=(0.05,0,0,0)
    sizes=[reads_num-sum(reads_cg_num)]+reads_cg_num
    patches,l_text,p_text = plt.pie(sizes,explode=explode,labels=labels,colors=colors, labeldistance = 1.1,autopct = '%3.1f%%',shadow = False, startangle = 90,pctdistance = 0.6)

    plt.axis('equal')
    #plt.legend(loc=2,bbox_to_anchor=(0, 0))
    ax=plt.subplot(212)
    t=np.zeros(20)
    for num in cgnum_per_read:
        t[min(num-1,19)]+=1
    labels = map(str,np.arange(1,20))+['20+']
    print(t)
    t = (np.array(t).astype(float)/sum(reads_cg_num))*100
    plt.bar(np.arange(20),t)
    ax.set_xticks(np.arange(20))
    ax.set_xticklabels(labels)
    ax.set_ylabel('Percentage of reads including CG')
    ax.set_xlabel('CG number per read')
    plt.text(4,max(t)+4,'All reads including CG site: '+str(sum(reads_cg_num)))
    #print args.output+'.pdf'
    plt.savefig(args.output+'.pdf')

if __name__=="__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('-b','--bamfile',help="bam file name", metavar="FILE")
    parser.add_argument('-g','--genome',help="Genome fasta file path")
    parser.add_argument('-o','--output',help="pie figure's filename")
    run(parser)





