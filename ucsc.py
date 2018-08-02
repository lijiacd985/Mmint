import argparse
import os

def run(parser):
    '''
    -t type
    -g genome
    -s scale
    -o output
    os.path.abspath(__file__)
    '''
    args = parser.parse_args()
    #files genome scale output
    #os.system('mkdir ')
    path = os.path.abspath(__file__)[:os.path.abspath(__file__).rfind('/')+1]
    os.system("perl "+path+"ucsc_tracks.pl -t "+str(args.type)+" -r "+str(args.genome)+" -s " \
            +str(args.scale)+" -o "+str(args.output))

