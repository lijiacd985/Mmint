import matplotlib.pyplot as plt
import numpy as np
#from sklearn import datasets
from sklearn.decomposition import PCA
import matplotlib.cm as cm
import argparse

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


#data = np.loadtxt(args.inputfile,usecols = (1,2,3,4,5,6,7,8,9,10))
##inputfile format
##	SampleA	SampleB	SampleC ...
##gene1	value1	value2	value3
##gene2	.......
##gene3	.......
#.
#.

data = np.genfromtxt(args.inputfile,skip_header=1)[:,1:]
#data = np.loadtxt(args.inputfile)
data1=np.transpose(data)
X=data1
#y=np.array([0,0,1,1,2,2,3,3,4,4])
y=np.arange(0,int(args.number),1)
Y=np.repeat(y,int(args.replicate))
#names = np.array(['A','B','C','D','E'])
#names = np.arange(0,int(args.number),1)
names = args.name
pca = PCA(n_components=2)
X_r = pca.fit(X).transform(X)
#for c, i, name, markers in zip("rgbky", [0, 1, 2, 3, 4], names, ('o', 'v', '^', '<', '>')):
#for c, i, name, markers in zip("rgbky", np.arange(0,int(args.number)), names, ('o', 'v', '^', '<', '>','')):
##shape and color setting
x = np.arange(int(args.number))
ys = [i+x+(i*x)**2 for i in range(int(args.number))]
colors = cm.rainbow(np.linspace(0, 1, len(ys)))
for c, i, name, markers in zip(colors, np.arange(0,int(args.number)+2), names, ('^', '^','^','^','^','^','^', '^','^','^','^','^','^', '^','^','^','^','^','^', '^','^','^','^','^')):
	plt.scatter(X_r[Y == i, 0], X_r[Y == i, 1], c=c, label=name,alpha=0.8,marker=markers,s=80)
plt.legend(loc=2)
plt.savefig(args.output+".pdf")
#plt.show()


##python PCA.meth.py -i inputfile -n 5 -r 2 -N A B C D E -o PCA
