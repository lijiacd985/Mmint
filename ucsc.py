import argparse
import os

def run(parser):
    '''
    -t type
    -g genome
    -s scale
    -o output
    '''
    args = parser.parse_args()
    #files genome scale output
    #os.system('mkdir ')
    os.system("perl ucsc_tracks.pl -t "+str(args.type)+" -g "+str(args.genome)+" -s " \
            +str(args.scale)+" -o "+str(args.output))

