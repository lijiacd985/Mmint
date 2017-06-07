#!/share/apps/bin/python
# coding=utf-8

import sys
import argparse
#func_list=['mdepth','pca','mcor','meth2chip','multiBw2Bed','curveDualYaxis','horizonalHeatmap','multiTracks']

def main():
    argparser = common_parser()
    #print(argparser)
    args = argparser.parse_args()
    subcommand = args.subcommand
    if subcommand=='mdepth':
        from mdepth import run
       # mdepth(argparser)
    if subcommand=='pca':
        from PCAmeth import run
       # pca(argparser)
    if subcommand=='mcor':
        from mCor import run
    if subcommand=='meth2chip':
        from Meth2ChIP import run
    if subcommand=='multibw2bed':
        from multiBw2bed import run
    if subcommand=='multibw2multibed':
        from multiBw2multiBed import run
    if subcommand=='curveDualYaxis':
        from curveDualYaxis import run
    if subcommand=='horizonalHeatmap':
        from horizonalHeatmap import run
    if subcommand=='multiTracks':
        from multiTracks import run
    run(argparser)

def common_parser():
    argparser = argparse.ArgumentParser()
    subparsers = argparser.add_subparsers(dest="subcommand")
    add_mdepth_parsers(subparsers)
    add_pca_parsers(subparsers)
    add_mcor_parsers(subparsers)
    add_meth2chip_parsers(subparsers)
    add_multibw2bed_parsers(subparsers)
    add_multibw2multibed_parsers(subparsers)
    add_curveDualYaxis_parsers(subparsers)
    add_horizonalHeatmap_parsers(subparsers)
    add_multiTracks_parsers(subparsers)
    return argparser

def add_multiTracks_parsers(s):
    parser = s.add_parser("multiTracks",help="This script will use bigwig and bed files as input and output pictures of multi-bigwig signals for each loci in the bedfiles. (similar with UCSC visualization tracks but can generated many automatically)")
    parser.add_argument('-b','--bigwig',help="input file (bw format)",nargs="*", metavar="FILE")
    parser.add_argument('-labels','--labels',help="labels for the input files",nargs="*", metavar="FILE")
    parser.add_argument('-c','--color',help="colors for the input file tracks",nargs="*", metavar="FILE")
    parser.add_argument('-bs','--binsize',help="bins size",metavar="FILE")
    parser.add_argument('-out','--out',help="output",nargs="*",metavar="FILE")
    parser.add_argument('-outRawCounts','--RawCounts',help="Raw counts output",nargs="*",metavar="FILE")
    parser.add_argument('-r','--regions',help="regions to plot",metavar="FILE")
    parser.add_argument('-f','--file',help="file include all the regions to plot",metavar="FILE")

def add_horizonalHeatmap_parsers(s):
    parser = s.add_parser("horizonalHeatmap",help="This script will use bigwig and bed files as input and plot multiple types of signals distribution on interested locations (up/dnstream xxx bp) as a horizonal heatmap.")
    parser.add_argument('-bw','--bigwig',help="bigwig for the computeMatrix", nargs="*",metavar="FILE")
    parser.add_argument('-bed','--bed',help="the regions to plot", metavar="FILE")
    parser.add_argument('-after','--dnregions',help="downstream regions to plot",metavar="FILE")
    parser.add_argument('-before','--upregions',help="upstream regions to plot",metavar="FILE")
    parser.add_argument('-bs','--binsize',help="bins size to use", metavar="FILE")
    parser.add_argument('-m','--scaleregion',help="scale the input bed regions to certain length(bp)",metavar="FILE")
    parser.add_argument('-o','--outFile',help="output file name",nargs="*",metavar="FILE")
    parser.add_argument('-L','--rowlabels',nargs="*",help="row labels for samples", metavar="FILE")
    parser.add_argument('-n','--name',help="name for picture", metavar="FILE")

def add_curveDualYaxis_parsers(s):
    parser = s.add_parser("curveDualYaxis",help="This script generate a two Yaxis (One for mCG/CG; the other is for ChIP-seq or other datatype) curve plot. This plot will show how methylation and other data type distribution on interested regions.")
    parser.add_argument('-bw','--bigwig',help="bigwig for the computeMatrix", nargs="*",metavar="FILE")
    parser.add_argument('-bed','--bed',help="the regions to plot", metavar="FILE")
    parser.add_argument('-after','--dnregions',help="downstream regions to plot",metavar="FILE")
    parser.add_argument('-before','--upregions',help="upstream regions to plot",metavar="FILE")
    parser.add_argument('-bs','--binsize',help="bins size to use", metavar="FILE")
    parser.add_argument('-m','--scaleregion',help="scale the input bed regions to certain length(bp)",metavar="FILE")
    parser.add_argument('-o','--outFile',help="output file name",nargs="*",metavar="FILE")
    parser.add_argument('-L','--rowlabels',nargs="*",help="row labels for samples", metavar="FILE")
    parser.add_argument('-n','--pdfName',help="name for pdf", metavar="FILE")

def add_multibw2multibed_parsers(s):
    parser = s.add_parser("multibw2multibed",help="This script generate the curve plot with multi-bigwig singal files against interested regions (bed file). Input files are multiple bigwig files and one bed (or multiple bed files) file.")
    parser.add_argument('-bw','--bigwig',help="bigwig for the computeMatrix", nargs="*",metavar="FILE")
    parser.add_argument('-bed','--bed',help="the regions to plot",nargs="*", metavar="FILE")
    parser.add_argument('-after','--dnregions',help="downstream regions to plot",metavar="FILE")
    parser.add_argument('-before','--upregions',help="upstream regions to plot",metavar="FILE")
    parser.add_argument('-bs','--binsize',help="bins size to use", metavar="FILE")
    parser.add_argument('-o','--outFile',help="output file name",nargs="*",metavar="FILE")
    parser.add_argument('-L','--rowlabels',nargs="*",help="row labels for samples", metavar="FILE")
    parser.add_argument('-n','--pdfName',help="name for pdf", metavar="FILE")

def add_multibw2bed_parsers(s):
    parser = s.add_parser("multibw2bed",help="This script generate the curve plot with multi-bigwig singal files against interested regions (bed file). Input files are multiple bigwig files and one bed (or multiple bed files) file.")
    parser.add_argument('-bw','--bigwig',help="bigwig for the computeMatrix", nargs="*",metavar="FILE")
    parser.add_argument('-bed','--bed',help="the regions to plot", metavar="FILE")
    parser.add_argument('-after','--dnregions',help="downstream regions to plot",metavar="FILE")
    parser.add_argument('-before','--upregions',help="upstream regions to plot",metavar="FILE")
    parser.add_argument('-bs','--binsize',help="bins size to use", metavar="FILE")
    parser.add_argument('-m','--scaleregion',help="scale the input bed regions to certain length(bp)",metavar="FILE")
    parser.add_argument('-o','--outFile',help="output file name",nargs="*",metavar="FILE")
    parser.add_argument('-L','--rowlabels',nargs="*",help="row labels for samples", metavar="FILE")
    parser.add_argument('-n','--pdfName',help="name for pdf", metavar="FILE")

def add_meth2chip_parsers(s):
    parser = s.add_parser("meth2chip",help="This script will plot the average ChIP-seq signals at certain methylation ratio range; the input files are methylation ratio file (*.G.bed from mcall MOABS) and the ChIP-seq signals intensity file.")
    parser.add_argument('-m','--methfile',help="input methylation Ratio file (the output file from mcall) ", metavar="FILE")
    parser.add_argument('-p','--peakfile',help="input peaks signal file (bedgraph format) ", metavar="FILE")
    parser.add_argument('-o','--output',help="output file name pre-index", metavar="FILE")

def add_mcor_parsers(s):
    parser = s.add_parser("mcor",help="This script will generate the correlation matrix for all the samples and some basic statistics. It will also generate a plot with diagnol as histgram of methylation ratio for each sample; offdiagnal as pairwise density for methylation ratio.")
    parser.add_argument('-m','--methfile',help="The output from mcall",nargs='*', metavar="FILE")
    parser.add_argument('-o','--output',help="The output file", metavar="FILE")

def add_mdepth_parsers(s):
    parser = s.add_parser("mdepth",help="This script will plot the Mean CpG methylation ratio and number of CpG sites under a series depth for multiple samples. The input file is the output file (*stat.txt) from mcall (MOABS).")
    parser.add_argument('-m','--methfile',help="The output *stat.txt from mcall",nargs="*",metavar="FILE")
    parser.add_argument('-l','--label',help="Labels for samples",nargs="*",metavar="FILE")
    parser.add_argument('-o','--output',help="The output file: *.pdf, *.png...", metavar="FILE")

def add_pca_parsers(s):
    parser = s.add_parser("pca",help="This script take methylation ratio matrix for multiple samples as input output a PCA plot.")
    parser.add_argument('-i','--inputfile',help="input file name", metavar="FILE")
    parser.add_argument('-n','--number',help="the number of samples")
    parser.add_argument('-r','--replicate',help="the replicates for each sample")
    parser.add_argument('-N','--name', nargs='+', help="the samples' names", required=True)
    parser.add_argument('-o','--output',help="the output file")

if __name__=="__main__":
    main()

