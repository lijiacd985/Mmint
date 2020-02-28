#import ssl
#ssl._create_default_https_context = ssl._create_unverified_context

import sys
sys.path.append('../')

import logging
from tests import *
from suds import *
from suds.client import Client
from datetime import datetime


def david_analysis(resF,inputIds):
    errors = 0
    
    setup_logging()
    
    logging.getLogger('suds.client').setLevel(logging.DEBUG)
    
    url = 'https://david.ncifcrf.gov/webservice/services/DAVIDWebService?wsdl'
        
    print('URL : %s' % url)
    
    client = Client(url)
    client.wsdl.services[0].setlocation('https://david.ncifcrf.gov/webservice/services/DAVIDWebService.DAVIDWebServiceHttpSoap11Endpoint/')
    client.service.authenticate('deqiangs@bcm.edu')
    
    idType='ENSEMBL_GENE_ID'
    listName = 'make_up'
    listType = 0
    print(client.service.addList(inputIds, idType, listName, listType))
    
    
    thd = 0.1
    ct = 2
    chartReport = client.service.getChartReport(thd,ct)
    chartRow = len(chartReport)
    print('Total chart records:',chartRow)
    
    with open(resF, 'w') as fOut:
    	fOut.write('Category\tTerm\tCount\t%\tPvalue\tGenes\tList Total\tPop Hits\tPop Total\tFold Enrichment\tBonferroni\tBenjamini\tFDR\n')
    	for simpleChartRecord in chartReport:
            categoryName = simpleChartRecord.categoryName
            termName = simpleChartRecord.termName
            listHits = simpleChartRecord.listHits
            percent = simpleChartRecord.percent
            ease = simpleChartRecord.ease
            Genes = simpleChartRecord.geneIds
            listTotals = simpleChartRecord.listTotals
            popHits = simpleChartRecord.popHits
            popTotals = simpleChartRecord.popTotals
            foldEnrichment = simpleChartRecord.foldEnrichment
            bonferroni = simpleChartRecord.bonferroni
            benjamini = simpleChartRecord.benjamini
            FDR = simpleChartRecord.afdr
            rowList = [categoryName,termName,str(listHits),str(percent),str(ease),Genes,str(listTotals),str(popHits),str(popTotals),str(foldEnrichment),str(bonferroni),str(benjamini),str(FDR)]
            fOut.write('\t'.join(rowList)+'\n')
    print('write file:', resF, 'finished!')
