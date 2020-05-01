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
    uncrst_2 = []
    k = open('input/template_%s.json'%sr)
    dictthingy = json.loads(k.read())
    for bin in dictthingy: 
        binNum = bin[-1]
        var    = bin[:-1]
        var_2 = bin
        if binNum not in bins: bins.append( int(binNum) )
        if var    not in uncrst: uncrst.append( var ) 
        if var_2    not in uncrst_2: uncrst_2.append( var_2 ) 
    for var in uncrst:
        h_name='%s_%s'%(sr,var[:-4])
        h = r.TH1F(h_name.replace('_prediction',''),'',len(binnings[sr])-1,binnings[sr])
        for bin in bins:
            h.SetBinContent( bin+1, dictthingy[var+'%d'%bin])
        outHists.append(h)
    for var in uncrst_2:
        if 'prediction' in var: continue
        h_name='%s_%s'%(sr,var+'_perBin')
        h = r.TH1F(h_name,'',len(binnings[sr])-1,binnings[sr])
        error = var+'_perBin'
        list_of_process = []
        if 'VZ' in sr: 
            list_of_process.append('TChiWZ')
            list_of_process.append('TChiZZ')
        for process in list_of_process:
            if 'WZ' in process: b = 'WZ'
            elif 'HZ' in process: b = 'HZ'
            elif 'ZZ' in process: b = 'ZZ'
            nuisance=h_name.replace('_perBin','').replace('VZ',b)
            print("{nuisance} : template_{sr} : {process}.* : altFileSym; suffix='_{error}'".format(nuisance=nuisance,sr=sr.replace('VZ',b),process=process,error=error))
        for bin in bins:
            if bin == int(var[-1]):
               h.SetBinContent( bin+1, dictthingy[var])
            else:
               h.SetBinContent(bin+1, dictthingy['prediction_bin'+'%d'%bin])
        outHists.append(h)
tf = r.TFile.Open("Templates.root","recreate")
for h in outHists:
    h.Write()
tf.Close()
