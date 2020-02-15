import urllib.request, urllib.parse, urllib.error
import argparse
import chartReport
#def great(args):
#    baseurl = 'http://bejerano.stanford.edu/great/public/cgi-bin/greatStart.php'
#    text=['requestURL','requestSpecies','requestName','requestSender','bgURL','bgName','outputType']
    #args = parser.parse_args()
'''
def add_onlineanalysis_parsers(s):
    parser = s.add_parser("OnlineAnalysis",help="Doing online analysis using DAVID analysis api")
    #parser.add_argument('-r','--analysis',help=r'Select online analysis you want, great or david',required=True,default='david')
    parser.add_argument('-f','--file',help=r"Output file name",required=True,default='david.genelist.txt')
    parser.add_argument('-g','--genelist',help=r"Genelist file name. Use gene name or ensembl id")
    parser.add_argument('-t','--type',help=r"Gene list type: ensembl(0) or gene name(1)")
'''

def genename_to_ensembl(names):
    path = os.path.abspath(__file__)
    path = path[:path.rfind('/')]+'/ensemblGene.v3.geneSymbolToId'
    dic={}
    with open(path) as f:
        lines = f.readlines()
    for line in lines:
        n,e = line.strip().split()
        dic[n]=e
    ans=[]
    for name in names:
        if name in dic:
            ans.append(dic[name])
    return ans


def david(name,list):
    chartReport.david_analysis(name,list)

def run(parser):
    args = parser.parse_args()
    with open(args.genelist) as f:
        lines = f.readlines()
    if args.type=='1':
        lines=genename_to_ensembl(lines)
    s=''
    for n in lines:
        s = s+n.strip()+','
    s = s[:-1]
    david(args.file,s)

