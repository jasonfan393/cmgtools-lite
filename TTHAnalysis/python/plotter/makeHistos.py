import ROOT as r 
import json
from array import array
srs = [
    'SRA',
    'SRAb',
    'SRB',
    'SRBb',
    'SRC',
    'SRCb',
    'SRHZ',
    'SRVZBoosted',
    'SRVZResolved'
]
binnings = {
    'SRA' : array('d',[50,100,150,230,300,600]),
    'SRAb': array('d',[50,100,150,230,300,600]),
    'SRB' : array('d',[50,100,150,230,300,600]),
    'SRBb': array('d',[50,100,150,230,300,600]),
    'SRC' : array('d',[50,100,150,250,300]),
    'SRCb': array('d',[50,100,150,250,300]),
    'SRHZ': array('d',[50,100,150,250,300]),
    'SRVZBoosted': array('d',[50,100,200,300,400,500,600]),
    'SRVZResolved' : array('d',[50,100,150,250,350,400])
}


outHists = []
for sr in srs: 
    bins = []
    uncrst = []
    k = open('input/template_%s.json'%sr)
    dictthingy = json.loads(k.read())
    for bin in dictthingy: 
        binNum = bin[-1]
        var    = bin[:-1]
        if binNum not in bins: bins.append( int(binNum) )
        if var    not in uncrst: uncrst.append( var ) 
    for var in uncrst:
        h = r.TH1F('%s_%s'%(sr,var),'',len(binnings[sr])-1,binnings[sr])
        for bin in bins:
            h.SetBinContent( bin+1, dictthingy[var+'%d'%bin])
        outHists.append(h)
tf = r.TFile.Open("Templates.root","recreate")
for h in outHists:
    h.Write()
tf.Close()
