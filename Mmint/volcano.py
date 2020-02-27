import matplotlib
matplotlib.use('Agg')
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
import argparse
plt.style.use('seaborn-white')

def run(parser):
    args = parser.parse_args()
    data = pd.read_csv(args.file,delimiter="\t")
    plt.figure()
    nl=-1*(np.log(data.iloc[:,4].values.astype(float)+0.0000000000000001)/np.log(10))
    md=data.iloc[:,3].values.astype(float)
    plt.plot(md[np.where(nl>=args.p)[0]],nl[np.where(nl>=args.p)[0]],'r.',alpha=0.5)
    plt.plot(md[np.where(nl<args.p)[0]],nl[np.where(nl<args.p)[0]],'g.',alpha=0.5)
    plt.ylabel('-log10p-value')
    plt.xlabel('Hypomethylated                      Hypermethylated')
    plt.savefig(args.output+'.pdf',bbox_inches="tight")

if __name__=="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-f','--file',help=r'DMR file. Format: chr start end ratio_difference p_value. Seperate:\t')
    parser.add_argument('-p','--p',help='cutoff p value',type=float)
    parser.add_argument('-o','--output',help='Prefix for the output PDF file.')
    run(parser)
