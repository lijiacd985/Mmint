# practice

Requirements:

DeepTools
matplotlib



Installation

mdepth.py

This script will plot the Mean CpG methylation ratio and number of CpG sites under a series depth for multiple samples. The input file is the output file (*stat.txt) from mcall (MOABS).

Meth2ChIP.py

This script will plot the average ChIP-seq signals at certain methylation ratio range (5% intervals);the input files are methylation ratio file (*.G.bed from mcall MOABS) and the ChIP-seq signals intensity file.

multiBw2bed.py / multiBw2multiBed.py

This script generate the curve plot with multi-bigwig singal files against interested regions (bed file). Input files are multiple bigwig files and one bed (or multiple bed files) file.

horizonalHeatmap.py

This script will use bigwig and bed files as input and plot multiple types of signals distribution on interested locations (up/dnstream xxx bp) as a horizonal heatmap.


multiTracks.py

This script will use bigwig and bed files as input and output pictures of multi-bigwig signals for each loci in the bedfiles. (similar with UCSC visualization tracks but can generated many automatically) 

