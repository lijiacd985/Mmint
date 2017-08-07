import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
import argparse

def run(parser):
    args = parser.parse_args()
    data = pd.read_csv(args.file,delimiter="\t")
    #print(data[:10])
    plt.figure()
    #print(data.iloc[:,4].values.astype(float))
    nl=-1*(np.log(data.iloc[:,4].values.astype(float))/np.log(10))
    md=data.iloc[:,3].values.astype(float)
    plt.plot(md[np.where(nl>=args.p)[0]],nl[np.where(nl>=args.p)[0]],'r.',alpha=0.5)
    plt.plot(md[np.where(nl<args.p)[0]],nl[np.where(nl<args.p)[0]],'g.',alpha=0.5)
    #plt.ylim(0,100)
    plt.ylabel('-log10p-value')
    plt.xlabel('Hypomethylated                      Hypermethylated')
    plt.savefig(args.output)

if __name__=="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-f','--file',help=r'DMR file. Format: chr start end ratio_difference p_value. Seperate:\t')
    parser.add_argument('-p','--p',help='cutoff p value',type=float)
    parser.add_argument('-o','--output',help='output file name')
    run(parser)
