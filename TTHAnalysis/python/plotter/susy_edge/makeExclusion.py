import ROOT as r
import os, re
import copy
from CMGTools.TTHAnalysis.plotter.susy_edge.scan_server import Scan, limitContainer
whichscan = 'slepton'
cardDirectory="cards_apr1"
outputDirectory="cards_apr1_sigscan"


scan = Scan(whichscan)
cardRegex = scan.cardRegex
scanName  = scan.name

#r.gROOT.SetBatch(True)
r.gStyle.SetPaintTextFormat('4.1f')



def readLimit(limitTree, mass, onlyObs=False):
    if not limitTree: 
        print 'Warning, no limit object, fit has crashed for point %s %s!'%(m1, m2)
        return None
    if not limitTree.GetEntries():
        print 'Warning, limit object is empty for %s %s!'%(m1, m2)
        return None
        
    retlimit = limitContainer()
    for ev in limitTree: 
        if ev.quantileExpected == -1: 
            retlimit.ex_obs = ev.limit
            retlimit.ex_obs_p1s = ev.limit*( scan.xsecs(mass,1) / scan.xsecs(mass,0))
            retlimit.ex_obs_m1s = ev.limit*( scan.xsecs(mass,-1) / scan.xsecs(mass,0))
        elif 0.49 < ev.quantileExpected < 0.51:
            retlimit.ex_exp = ev.limit
        elif 0.15 < ev.quantileExpected < 0.17:
            retlimit.ex_exp_p1s = ev.limit
        elif 0.83 < ev.quantileExpected < 0.85:
            retlimit.ex_exp_m1s = ev.limit
    if onlyObs:
        for hist in ['ex_obs_p1s', 'ex_obs_m1s', 'ex_exp', 'ex_exp_m1s', 'ex_exp_p1s']:
            setattr(retlimit, hist,retlimit.ex_obs)
    return retlimit


def dumpDictToTH2s(dictio, scan, suffix='', significance=False): 

    for hist in ['ex_obs', 'ex_obs_p1s', 'ex_obs_m1s', 'ex_exp', 'ex_exp_m1s', 'ex_exp_p1s']: 
        if significance and hist!='ex_obs': continue
        thehist = scan.getEmptyScanHist(hist)

        for (m1,m2) in dictio: 
            bin = thehist.FindBin(float(m1),float(m2))
            if thehist.GetBinContent( bin ): 
                raise RuntimeError("Point (%d,%d) has already been filled"%(m1,m2))
            thehist.SetBinContent( bin, getattr(dictio[(m1,m2)], hist))
        thehist.GetZaxis().SetRangeUser(0,10)
        if significance: # remove spikes
            for i in range(1,1+thehist.GetXaxis().GetNbins()):
                for j in range(1,1+thehist.GetYaxis().GetNbins()):
                    bin1 = thehist.GetBin(i,j)
                    cont = thehist.GetBinContent(bin1)
                    if not cont: continue
                    for j2 in range(j+1,1+thehist.GetYaxis().GetNbins()):
                        bin2 = thehist.GetBin(i,j2)
                        cont2 = thehist.GetBinContent(bin2)
                        if cont2:
                            if abs(cont-cont2)/cont > 1.1: 
                                print 'found spike!', thehist.GetXaxis().GetBinCenter(i),thehist.GetYaxis().GetBinCenter(j)
                                thehist.SetBinContent(bin1,0)
                            break
        setattr(scan, hist, thehist)

    if not significance:
        scan.getSmoothedGraphs()
    else:
        scan.getSmoothedSignificanceGraphs()
    scan.writeRelevantHistsToFile(suffix=suffix,noExclusionLines=significance)



pattern = "higgsCombinefit_%s_(?P<m1>.*)_(?P<m2>.*).AsymptoticLimits.mH120.root"%scanName
print pattern
pattern = re.compile( pattern )
limits = { }; signis = {}
for point in os.listdir(outputDirectory):
    match = pattern.search( point ) 
    if not match: continue
    m1,m2 = (match.group('m1'), match.group('m2'))
    fil = r.TFile.Open( outputDirectory + '/' + point ) 
    limit = readLimit(  fil.Get('limit') , m1 ) 
    if limit: 
        limits[(m1,m2)] = limit
    
    fil = r.TFile.Open( outputDirectory + '/' + point.replace('AsymptoticLimits','Significance'))
    if fil: 
        sig = readLimit( fil.Get('limit'), m1)
        if sig:
            signis[(m1,m2)] = sig

dumpDictToTH2s(limits,scan)
dumpDictToTH2s(signis,scan, suffix='significance',significance=True)


            




    

