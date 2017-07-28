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
    p = subprocess.Popen('samtools view '+args.bamfile,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    reads_num=0
    reads_cg_num=[0,0,0] #CG,cg,Cg
    cgnum_per_read=[]

    for line in p.stdout:
        t = line.decode('utf-8').strip().split()
        chr = t[2]
        start=int(t[3])
        length = len(t[9])
        if not chr in chrs: continue
            #raise Exception("Bamfile contains chr which not in genome")
        #if start+length>l[chr]:
        #    raise Exception("Bamfile contains reads not in this genome")
        end=min(start+length+1,l[chr])
        read=bases[chr][start:end]
        ls=len(read)
        reads_num+=1
        cg=[0,0,0]
        for i in range(1,ls):
            if 'G'==read[i] and 'C'==read[i-1]:
                cg[0]+=1
            else:
                if 'g'==read[i] and 'c'==read[i-1]:
                    cg[1]+=1
                else:
                    if ('G'==read[i] or 'g'==read[i]) and ('C'==read[i-1] or 'c'==read[i-1]):
                        cg[2]+=1
        count = int(cg[0]>0)+int(cg[1]>0)+int(cg[2]>0)
        if count==0: continue
        if count==1:
            if cg[0]>0:
                reads_cg_num[0]+=1
            else:
                if cg[1]>0:
                    reads_cg_num[1]+=1
                else:
                    if cg[2]>0:
                        reads_cg_num[2]+=1
        else:
            reads_cg_num[2]+=1
        cgnum_per_read.append(sum(cg))

    print reads_cg_num
    print reads_num

    plt.figure()
    plt.subplot(211)
    labels = ['noCG','Nonrepeat CG','Repeat cg','CGcg mix']
    colors = ['r','b','g','y']
    explode=(0.05,0,0,0)
    sizes=[reads_num-sum(reads_cg_num)]+reads_cg_num
    patches,l_text,p_text = plt.pie(sizes,explode=explode,labels=labels,colors=colors, labeldistance = 1.1,autopct = '%3.1f%%',shadow = False, startangle = 90,pctdistance = 0.6)

    plt.axis('equal')
    plt.legend(loc=2)
    ax=plt.subplot(212)
    t=np.zeros(20)
    for num in cgnum_per_read:
        t[min(num-1,19)]+=1
    labels = map(str,np.arange(1,20))+['20+']
    t = (np.array(t).astype(float)/sum(reads_cg_num))*100
    plt.bar(np.arange(20),t)
    ax.set_xticks(np.arange(20))
    ax.set_xticklabels(labels)
    ax.set_ylabel('Percent of all CG containing reads')
    ax.set_xlabel('CG number pre read')
    plt.text(4,max(t)+0.05,'All CG containing reads: '+str(sum(reads_cg_num)))
    print args.output+'.pdf'
    plt.savefig(args.output+'.pdf')

if __name__=="__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('-b','--bamfile',help="bam file name", metavar="FILE")
    parser.add_argument('-g','--genome',help="Genome fasta file path")
    parser.add_argument('-o','--output',help="pie figure's filename")
    run(parser)





