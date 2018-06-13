import urllib
import argparse

def great(args):
    baseurl = 'http://bejerano.stanford.edu/great/public/cgi-bin/greatStart.php'
    text=['requestURL','requestSpecies','requestName','requestSender','bgURL','bgName','outputType']
    #args = parser.parse_args()

def david(args):

def run(parser):
    args = parser.parse_args()
    if args.analysis == 'great':
        great(args)
    if args.analysis == 'david':
        david(args)
