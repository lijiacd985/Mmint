import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
plt.style.use('seaborn-white')
import numpy as np
#from sklearn import datasets
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
import matplotlib.cm as cm
import argparse
from .Format import formdata
import os

def run(parser):
    args = parser.parse_args()
    if len(args.name)!=len(args.inputfile):
        raise Exception('Equal number of sample names and input sample files are required!')
    bedfile = args.bed
    names = args.name
    samples = args.inputfile
    coverage = args.cov
    if bedfile!='':
        if not os.path.exists(bedfile):
            raise Exception(bedfile+' does not exist!')
    
    sample_number = len(samples)
    flat_sample_name = []
    ind = []
    extend_label = []
    index = 0
    for n,label in zip(samples,names):
        c = n.strip().split(',')
        # replicates_number.append(len(c))
        flat_sample_name.extend(c)
        for i in range(len(c)):
            extend_label.append(label)
            ind.append(index)
        index += 1
    data=formdata(flat_sample_name, coverage, bedfile)
    data1=np.transpose(data).astype(float)
    X=data1
    names = args.name
    if not args.method in ['pca','TSNE']:
        raise Exception("Unacceptable method")
    if args.method=='pca':
        pca = PCA(n_components=2)
        X_r = pca.fit(X).transform(X)
    else:
        pca = PCA(n_components=50)
        xx = pca.fit_transform(X)
        tsne = TSNE(n_components=2)
        X_r = tsne.fit_transform(xx)

    colors = cm.rainbow(np.linspace(0, 1, len(flat_sample_name)))
    fig=plt.figure()
    plt.subplot(111)
    plt.xlim(np.min(X_r[:,0])-0.2*np.abs(np.min(X_r[:,0])),np.max(X_r[:,0])+0.2*np.abs(np.max(X_r[:,0])))
    plt.ylim(np.min(X_r[:,1])-0.2*np.abs(np.min(X_r[:,1])),np.max(X_r[:,1])+0.2*np.abs(np.max(X_r[:,1])))
    fig.subplots_adjust(left=0.1,right=0.8)
    markers = ['o', '^','v','<','>','1','2', '3','4','8','s','P','p', '*','H','h','x','X','D', 'd','|','_','+']
    for i,label in enumerate(extend_label):
        plt.scatter(X_r[i,0], X_r[i,1], c=colors[ind[i]], label=label, alpha=0.8, marker=markers[ind[i]],s=80)
    plt.legend(loc='center left', bbox_to_anchor=(1.04, 0.5))
    plt.savefig(args.output, bbox_inches="tight")


    ##python PCA.meth.py -i inputfile -n 5 -r 2 -N A B C D E -o PCA
if __name__=="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-i','--inputfile',help="input file name", metavar="FILE", nargs='+', required=True)
    parser.add_argument('-N','--name', nargs='+', help="the samples' names", required=True)
    parser.add_argument('-o','--output',help="the output file")
    parser.add_argument('-b','--bed',metavar="FILE",default='',help="If -b available, only cpgs in these regions will be selected in cluster.")
    parser.add_argument('-c','--cov',type=int,help="minimal coverage of cpg sites for every sample,default=0",default=0)
    parser.add_argument('-m','--method',help="pca or TSNE",default="pca")
    run(parser)


