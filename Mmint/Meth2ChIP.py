import numpy as np
import os,sys
import argparse
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
plt.style.use('ggplot')
import pybedtools 
def run(parser):
    args = parser.parse_args()

    '''
    The inputs for this script both are bedgraph, one is for meth signals and the other input is for chipseq signals.
    This script is mapping the chipseq signals to meth signal based on the sites and generate the scatter with xaxis
    represent the meth ratio and yaxis represent the chipseq ratio.

    '''
    
    blocks = 20

    peak_f = pybedtools.BedTool(args.peakfile)
    methy_f = pybedtools.BedTool(args.methfile)
    inter_f = peak_f.intersect(methy_f, wo=True, stream=True)
    d = inter_f.groupby(g=[1,2,3], c=[4,8], o=['mean', 'mean'])
    intense = [0]*blocks
    num = [0]*blocks
    step = 1.00/blocks
    for line in d:
        _intense = float(line[3])
        _ratio = float(line[4])
        _ratio = min(_ratio, 1.0)
        _index = int(_ratio//step)
        intense[_index] += _intense
        num[_index] += 1
    for i in range(len(intense)):
        if num[i]>0:
            intense[i] = intense[i]/num[i]
    density = np.array(num)
    density = density*100/np.sum(density)

    fig, ax1 = plt.subplots()
    fig.subplots_adjust(bottom=0.125,right=0.85)
    ax2 = ax1.twinx()
    ax1.grid(False)
    ax2.grid(False)

    ax1.bar(np.arange(0,1,step),density,facecolor='green',align='edge',bottom=0, alpha=0.9,width=0.04)
    ax1.set_xlabel('Methylation Ratio',fontsize=17)
    ax1.set_ylabel('Percentage',color="green",fontsize=18)
    ax1.yaxis.set_tick_params(labelsize=13)
    ax1.xaxis.set_tick_params(labelsize=13)
    ax1.set_xlim((-0.05,1.05))
    ax1.set_ylim((0,np.max(density)+10))
    region=[]
    region.append([0.0,0.0,0.09,0.09])
    region.append([0.11,0.11,0.49,0.49])
    region.append([0.51,0.51,0.89,0.89])
    region.append([0.91,0.91,1.0,1.0])
    regiony=[np.max(density)+6,np.max(density)+7,np.max(density)+7,np.max(density)+6]
    r=[]
    r.append(np.sum(density[:2]))
    r.append(np.sum(density[2:10]))
    r.append(np.sum(density[10:-2]))
    r.append(np.sum(density[-2:]))
    from decimal import Decimal
    for j in range(4):
        r[j] = Decimal(str(r[j])).quantize(Decimal('0.00'))
    for j in range(4):
        ax1.plot(region[j],regiony,lw=1.5,color='green')
        ax1.text((region[j][1]+region[j][2])/2,np.max(density)+8,str(r[j])+'%',ha='center', va='bottom')
    ax1.set_title("Peaks with CpGs: %s; Total Peaks: %s" %(len(d),len(peak_f)),fontsize=12)
    
    ax2.plot(np.arange(0,1,step)+0.025,intense,'-o',color="red")
    ax2.set_ylabel('ChIP-Seq Signal',color="red",fontsize=18)
    ax2.set_ylim((0,max(intense)*1.2))
    ax2.yaxis.set_tick_params(labelsize=13)
    fig.savefig(args.output+".pdf")
         
    umr = d.filter(lambda x:float(x[4])<0.1)
    lmr = d.filter(lambda x:(float(x[4])>=0.1) & (float(x[4])<0.5))
    mmr = d.filter(lambda x:(float(x[4])>=0.5) & (float(x[4])<0.9))
    hmr = d.filter(lambda x:float(x[4])>=0.9)
    filenames=[args.output+'.umr.bed',args.output+'.lmr.bed',args.output+'.mmr.bed',args.output+'.hmr.bed']
    regions = [umr, lmr, mmr, hmr]
    for i in range(4):
        regions[i].saveas(filenames[i])
   
    if args.annotationfile:
        if not os.path.exists(args.annotationfile):
            raise Exception('Fail to generate annotation files due to unexist annotation file.')
        for i in range(4):
            f = pybedtools.BedTool(filenames[i])
            f.closest(args.annotationfile).saveas(filenames[i]+'.anno.bed')


if __name__=="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-m','--methfile',help="input methylation Ratio file (the output file from mcall) ", metavar="FILE")
    parser.add_argument('-p','--peakfile',help="input peaks signal file (bedgraph format) ", metavar="FILE")
    parser.add_argument('-o','--output',help="output file name pre-index", metavar="FILE")
    parser.add_argument('-a','--annotationfile',help="annotate peaks by bedfiles. e.g. Gene,Exon etc", metavar="FILE")
    run(parser)
