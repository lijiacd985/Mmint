# practice

Requirements:

DeepTools
matplotlib



Installation

1. mdepth.py

This script will plot the Mean CpG methylation ratio and number of CpG sites under a series depth for multiple samples. The input file is the output file (*stat.txt) from mcall (MOABS).

2. PCA.meth.py

This script take methylation ratio matrix for multiple samples as input output a PCA plot.

Example Command:
python PCA.meth.py -i merge.mC -n 5 -r 1 -N A B C D E -o meth.PCA

merge.mC:

CpG A B C

chr10-100083445-100083643	1.00	0.50	0.38

chr10-10031131-10031160	0.99	0.73	0.97

chr10-1006098-1006108	0.89	0.50	1.00

chr10-100847166-100847457	0.93	0.79	0.94

chr10-10084773-10085013	1.00	0.68	0.95

3. mCor.py

This script will generate the correlation matrix for all the samples and some basic statistics. It will also generate a plot with diagnol as histgram of methylation ratio for each sample; offdiagnal as pairwise density for methylation ratio.

Input:

chr start end methRatio



4. Meth2ChIP.py

This script will plot the average ChIP-seq signals at certain methylation ratio range (5% intervals);the input files are methylation ratio file (*.G.bed from mcall MOABS) and the ChIP-seq signals intensity file.

ChIP-seq signals intensity file:

chr peak.start  peak.end  intensity

chr1    100113803       100113954       0.219254

chr1    100715377       100715412       0.1062

chr1    1007642 1007662 0.107425

chr1    100816764       100816969       0.35706

chr1    100817693       100817732       0.113485


4. multiBw2bed.py / multiBw2multiBed.py

This script generate the curve plot with multi-bigwig singal files against interested regions (bed file). Input files are multiple bigwig files and one bed (or multiple bed files) file.

5. curveDualYaxis.py

This script generate a two Yaxis (One for mCG/CG; the other is for ChIP-seq or other datatype) curve plot. This plot will show how methylation and other data type distribution on interested regions.

6. horizonalHeatmap.py

This script will use bigwig and bed files as input and plot multiple types of signals distribution on interested locations (up/dnstream xxx bp) as a horizonal heatmap.


7. multiTracks.py

This script will use bigwig and bed files as input and output pictures of multi-bigwig signals for each loci in the bedfiles. (similar with UCSC visualization tracks but can generated many automatically) 

Example command:
python  multiTracks.py -bs 100 -f regions.txt -b H3K4me3_m24.merge.bw H3K27me3_m24.merge.bw KO-K4m3.norm.bw KO-K27m3.norm.bw  -labels m_H3K4me3 m_H3K4me3 KO_H3K4me3 KO_H3K27me3 -out testRegions1.npz testRegions2.npz testRegions3.npz testRegions4.npz testRegions5.npz -outRawCounts testRegions1.tab testRegions2.tab testRegions3.tab testRegions4.tab testRegions5.tab -c r g b black yellow

regions.txt:

chr4:82878750:82888151	geneName1

chr14:56255857:56265260	geneName2

chr7:44809255:44818658	geneName3

chr7:45915022:45924426	geneName4

chr8:85068756:85078161	geneName5

