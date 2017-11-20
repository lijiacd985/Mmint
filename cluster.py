import matplotlib.pyplot as plt
import numpy as np
#from sklearn import datasets
from sklearn.decomposition import PCA
import matplotlib.cm as cm
import argparse
import pandas as pd
import seaborn as sns
from scipy.cluster.hierarchy import dendrogram, linkage
from Format import formdata
'''
parser = argparse.ArgumentParser()
parser.add_argument('-i','--inputfile',help="input file name", metavar="FILE")
parser.add_argument('-n','--number',help="the number of samples")
parser.add_argument('-r','--replicate',help="the replicates for each sample")
parser.add_argument('-N','--name', nargs='+', help="the samples' names", required=True)
parser.add_argument('-o','--output',help="the output file")
args = parser.parse_args()
#print args.inputfile
#print args.number
#print args.replicate
'''

#data = np.loadtxt(args.inputfile,usecols = (1,2,3,4,5,6,7,8,9,10))
##inputfile format
##	SampleA	SampleB	SampleC ...
##gene1	value1	value2	value3
##gene2	.......
##gene3	.......
#.
#.
def run(parser):
    args = parser.parse_args()
    names = args.name
#data=formdata(args.inputfile,args.cov,bedfile)
    data = np.array(formdata(args.inputfile,args.cov,args.bed)).astype(float).T #pd.read_csv(args.inputfile,header=None,names = names,sep='\t').values.T
    plt.figure()
    plt.ylabel("Distance")
    z=linkage(data,args.linktype)
    dendrogram(z,no_labels=False,leaf_label_func=lambda x:names[x])
#    plt.xticks(np.arange(len(names)),names)
    plt.savefig(args.output+'.pdf')


    ##python PCA.meth.py -i inputfile -n 5 -r 2 -N A B C D E -o PCA
if __name__=="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-i','--inputfile',help="input file name", metavar="FILE")
    parser.add_argument('-n','--number',help="the number of samples")
    parser.add_argument('-r','--replicate',help="the replicates for each sample")
    parser.add_argument('-N','--name', nargs='+', help="the samples' names", required=True)
    parser.add_argument('-o','--output',help="the output file")
    pca(parser)


