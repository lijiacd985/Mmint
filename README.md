# Mplot

<h3>Requirements:</h3>

- python2

- DeepTools

- matplotlib



Installation

<h3>Usage</h3>

1. mdepth.py

This script will plot the Mean CpG methylation ratio and the number of CpG sites under a series depths for multiple samples. The input file is the output file (*stat.txt) from mcall (MOABS).

Example Command:

mmint mdepth -m DE_stat.txt GT_stat.txt FG_stat.txt PE_stat.txt -l DE GT FG PE -o mdepth.pdf



2. DepthvsReadsNum.py

This script will plot the wig sum percentage (Y-axis) (total coverage for certain CpGs/total coverage for all CpGs) at depth >=x (x=1,2,4,8,16,32,64,128,256) (X-axis) to detect if there are high duplication level or sequence bias. If the sequence is randomly sequenced with no bias and no duplication, the total reads number should decrease to less than 10% with the depth increase to certain number (if the read length is 75 bp, the maximum coverage for one CpG supported by non-duplicate reads should be 75); if there is bias or high duplication level, the curve should be a flat line start at certain depth (eg. 100) with percentage of reads >= 20% (see the example).  


input file can be the ouput file (*.G.bed) from MOABS (mcall) or a file with at least 6 columns:

chr start end ratio total-C total-mC

Example Command:

mmint DepthvsReadsNum -m a.G.bed b.G.bed c.G.bed -l A B C -o depthvsReadsNum


3. PCA and cluster

This script take methylation ratio matrix for multiple samples and the bed file for intereseted regions as input and output a PCA/cluster plot based on mCG/CG on certain regions (e.g. promoter, CpG Island ...) with certain coverage (e.g. >=10).

Example Command:

A.G.bed is the output file from MAOBS (mcall) or it can be bed files with at least four columns:

chr  start   end   methRatio

mmint pca -i A.G.bed B.G.bed C.G.bed -n 3 -r 1 -N A B C -b cpgisland.bed -c 10 -o meth.PCA

mmint cluster -i A.G.bed B.G.bed C.G.bed -N A B C -o cluster -l average


4. mCor.py

This script will generate the correlation matrix for all the samples under certain coverage threshold and some basic statistics. It will also generate a plot with diagnol as histgram of methylation ratio for each sample; offdiagnal as pairwise density for methylation ratio.

The input file is the same with PCA;

Example Command:

mplot  mcor -m test1.bed test2.bed test3.bed -o mCorr


5. Meth2ChIP.py

This script will plot the average ChIP-seq signals at certain methylation ratio range (5% intervals); We separated the mehtylation level to four categories: UMR(0-0.1),LMR(0.1-0.5),MMR(0.5-0.9),HMR(0.9-1.0); and it will also output the numbers of regions that include the CpGs in your inputfile; the ratios of regions that fall into the four categories, respectively.
In addition, it will generate a scatter plot with Xaxis as mCG/CG ratio and Yaxis as ChIPseq intensity. The input files are methylation ratio file (*.G.bed from mcall MOABS) and the ChIP-seq signals intensity file.

Example Command:

mmint meth2chip -m A.G.bed -p ChIP.bed -o meth2ChIP

ChIP-seq signals intensity file:

chr peak.start  peak.end  intensity

chr1    100113803       100113954       0.219254

chr1    100715377       100715412       0.1062

chr1    1007642 1007662 0.107425

chr1    100816764       100816969       0.35706

chr1    100817693       100817732       0.113485


5. multiBw2bed.py / multiBw2multiBed.py

This script generate the curve plot with multi-bigwig singal files against interested regions (bed file). Input files are multiple bigwig files and one bed (or multiple bed files) file.

6. curveDualYaxis.py

This script generate a two Yaxis (One for mCG/CG; the other is for ChIP-seq or other datatype) curve plot. This plot will show how methylation and other data type distribution on interested regions.

7. horizonalHeatmap.py

This script will use bigwig and bed files as input and plot multiple types of signals distribution on interested locations (up/dnstream xxx bp) as a horizonal heatmap.


8. multiTracks.py/multiTracks.meth.py

This script will use bigwig and bed files as input and output pictures of multi-bigwig signals for each loci in the bedfiles. (similar with UCSC visualization tracks but can generated many automatically) 
The multiTracks.meth.py is taking methylation bw files as input and output the up/dn 5000 bp of the intereseted regions;with 
red dashed lines as the boundaries of the interested regions.

Example command:
python  multiTracks.py -bs 100 -f regions.txt -b H3K4me3_m24.merge.bw H3K27me3_m24.merge.bw KO-K4m3.norm.bw KO-K27m3.norm.bw  -labels m_H3K4me3 m_H3K4me3 KO_H3K4me3 KO_H3K27me3 -out testRegions1.npz testRegions2.npz testRegions3.npz testRegions4.npz testRegions5.npz -outRawCounts testRegions1.tab testRegions2.tab testRegions3.tab testRegions4.tab testRegions5.tab -c r g b black yellow

regions.txt:

chr4:82878750:82888151	geneName1

chr14:56255857:56265260	geneName2

chr7:44809255:44818658	geneName3

chr7:45915022:45924426	geneName4

chr8:85068756:85078161	geneName5


NOTE:

the #6,#7,#8 -o option need to be *.gz format and the number of -o option is the same to your input files number

9. volcano
This script will draw volcano plot about bed files

Example command:
mplot volcano -f dmrtest.bed -p 5 -o test

dmrtest.bed:

chr1    start   end methylation_difference  p_value

Fields seperate by tab.
