#!/usr/bin/env python
from mcAnalysis import *
from histoWithNuisances import _cloneNoDir
import re, sys, os, os.path
systs = {}

from optparse import OptionParser
parser = OptionParser(usage="%prog [options] mc.txt cuts.txt var bins")
addMCAnalysisOptions(parser)
parser.add_option("--od", "--outdir", dest="outdir", type="string", default=None, help="output directory name") 
parser.add_option("--asimov", dest="asimov", type="string", default=None, help="Use an Asimov dataset of the specified kind: including signal ('signal','s','sig','s+b') or background-only ('background','bkg','b','b-only')")
parser.add_option("--bbb", dest="bbb", type="string", default=None, help="Options for bin-by-bin statistical uncertainties with the specified nuisance name")
parser.add_option("--amc", "--autoMCStats", dest="autoMCStats", action="store_true", default=False, help="use autoMCStats")
parser.add_option("--autoMCStatsThreshold", dest="autoMCStatsValue", type="int", default=10, help="threshold to put on autoMCStats")
parser.add_option("--infile", dest="infile", action="store_true", default=False, help="Read histograms to file")
parser.add_option("--savefile", dest="savefile", action="store_true", default=False, help="Save histos to file")
parser.add_option("--categorize", dest="categ", type="string", nargs=3, default=None, help="Split in categories. Requires 3 arguments: expression, binning, bin labels")
parser.add_option("--categorize-by-ranges", dest="categ_ranges", type="string", nargs=2, default=None, help="Split in categories according to the signal extraction variables. Requires 2 arguments: binning (in bin numbers), bin labels")

parser.add_option("--regularize", dest="regularize", action="store_true", default=False, help="Regularize templates")
parser.add_option("--threshold", dest="threshold", type=float, default=0.0, help="Minimum event yield to consider processes")
parser.add_option("--filter", dest="filter", type="string", default=None, help="File with list of processes to be removed from the datacards")

parser.add_option("--tikhonov_unfolding", dest="tik", type="string", default=None, nargs=2, help="Unfolding datacard using the tikhonov method. Requires the process name and the signal strength name")
parser.add_option("--SVD_unfolding", dest="SVD", type="string", default=None, help="Unfolding datacard using the SVD method. Requires the signal strength name")

(options, args) = parser.parse_args()
options.weight = True
options.final  = True

if "/functions_cc.so" not in ROOT.gSystem.GetLibraries(): 
    ROOT.gROOT.ProcessLine(".L %s/src/CMGTools/TTHAnalysis/python/plotter/functions.cc+" % os.environ['CMSSW_BASE']);

mca  = MCAnalysis(args[0],options)
cuts = CutsFile(args[1],options)

binname = os.path.basename(args[1]).replace(".txt","") if options.binname == 'default' else options.binname
if binname[0] in "1234567890": raise RuntimeError("Bins should start with a letter.")
outdir  = options.outdir+"/" if options.outdir else ""
if not os.path.exists(outdir): os.mkdir(outdir)

report={}
if options.infile:
    infile = ROOT.TFile(outdir+binname+".bare.root","read")
    for p in mca.listSignals(True)+mca.listBackgrounds(True)+['data']:
        variations = mca.getProcessNuisances(p) if p != "data" else []
        h = readHistoWithNuisances(infile, "x_"+p, variations, mayBeMissing=True)
        if h: report[p] = h
else:
    if options.categ:
       cexpr, cbins, _ = options.categ
       report = mca.getPlotsRaw("x", cexpr+":"+args[2], makeBinningProductString(args[3],cbins), cuts.allCuts(), nodata=options.asimov) 
    else:
       report = mca.getPlotsRaw("x", args[2], args[3], cuts.allCuts(), nodata=options.asimov) 
    for p,h in report.iteritems(): h.cropNegativeBins(threshold=1e-5)

if options.savefile:
    savefile = ROOT.TFile(outdir+binname+".bare.root","recreate")
    for k,h in report.iteritems(): 
        h.writeToFile(savefile, takeOwnership=False)
    savefile.Close()

if options.asimov:
    if options.asimov in ("s","sig","signal","s+b"):
        asimovprocesses = mca.listSignals() + mca.listBackgrounds()
    elif options.asimov in ("b","bkg","background", "b-only"):
        asimovprocesses = mca.listBackgrounds()
    else: raise RuntimeError("the --asimov option requires to specify signal/sig/s/s+b or background/bkg/b/b-only")
    tomerge = None
    for p in asimovprocesses:
        if p in report: 
            if tomerge is None: 
                tomerge = report[p].raw().Clone("x_data_obs"); tomerge.SetDirectory(None)
            else: tomerge.Add(report[p].raw())
    report['data_obs'] = HistoWithNuisances(tomerge)
else:
    report['data_obs'] = report['data'].Clone("x_data_obs") 

if options.categ:
    allreports = dict()
    catlabels = options.categ[2].split(",")
    if len(catlabels) != report["data_obs"].GetNbinsY(): raise RuntimeError("Mismatch between category labels and bins")
    for ic,lab in enumerate(catlabels):
        allreports["%s_%s"%(binname,lab)] = dict( (k, h.projectionX("x_"+k,ic+1,ic+1)) for (k,h) in report.iteritems() )
elif options.categ_ranges: 
    allreports = dict()
    catlabels = options.categ_ranges[1].split(',')
    catbinning = eval( options.categ_ranges[0] ) 
    #print "catbinning ", catbinning
    for ic,lab in enumerate(catlabels):
        kk = {} 
        for (k,h) in report.iteritems(): 
            #print "x_"+k
            kk[k] = h.getHistoInRange( "x_"+k, catbinning[ic],catbinning[ic+1])
        allreports["%s_%s"%(binname,lab)] = kk
else:
    allreports = {binname:report}


if options.filter: 
    toremove=[]
    with open(options.filter, 'r') as f:
        for l in f.readlines(): 
            binname,proc = l.split(':')
            procpattern = re.compile( proc.rstrip() ) 
            if binname in allreports:
                for p in allreports[binname]:
                    if procpattern.match(p):
                        if (binname,p) not in toremove:
                           toremove.append( (binname, p))
    for binname,p in toremove:
        allreports[binname].pop(p)

for binname, report in allreports.iteritems():
  if options.bbb:
    if options.autoMCStats: raise RuntimeError("Can't use --bbb together with --amc/--autoMCStats")
    for p,h in report.iteritems(): 
      if p not in ("data", "data_obs"):
        h.addBinByBin(namePattern="%s_%s_%s_bin{bin}" % (options.bbb, binname, p), conservativePruning = True)
  for p,h in report.iteritems():
    for b in xrange(1,h.GetNbinsX()+1):
      h.SetBinError(b,min(h.GetBinContent(b),h.GetBinError(b))) # crop all uncertainties to 100% to avoid negative variations
  nuisances = sorted(listAllNuisances(report))

  allyields = dict([(p,h.Integral()) for p,h in report.iteritems()])
  procs = []; iproc = {}
  for i,s in enumerate(mca.listSignals()):
    if s not in allyields: continue
    if allyields[s] <= options.threshold: continue
    procs.append(s); iproc[s] = i-len(mca.listSignals())+1
  for i,b in enumerate(mca.listBackgrounds()):
    if b not in allyields: continue
    if allyields[b] <= options.threshold: continue
    procs.append(b); iproc[b] = i+1
  #for p in procs: print "%-10s %10.4f" % (p, allyields[p])

  systs = {}
  for name in nuisances:
    effshape = {}
    isShape = False
    for p in procs:
        h = report[p]
        n0 = h.Integral()
        if h.hasVariation(name):
            if isShape or h.isShapeVariation(name):
                if name.endswith("_lnU"): 
                    raise RuntimeError("Nuisance %s should be lnU but has shape effect on %s" % (name,p))
                #print "Nuisance %s has a shape effect on process %s" % (name, p)
                #if "templstat" not in name and not isShape:
                #    h.isShapeVariation(name,debug=True)
                isShape = True
            variants = list(h.getVariation(name))
            for hv,d in zip(variants, ('up','down')):
                k = hv.Integral()/n0
                if k == 0: 
                    print "Warning: underflow template for %s %s %s %s. Will take the nominal scaled down by a factor 2" % (binname, p, name, d)
                    hv.Add(h.raw()); hv.Scale(0.5)
                elif k < 0.2 or k > 5:
                    print "Warning: big shift in template for %s %s %s %s: kappa = %g " % (binname, p, name, d, k)
            # prevent variations from going to zero by symmetrizing
            for bin in range(1,h.GetXaxis().GetNbins()+1):
                for d in range(2):
                    if variants[d].GetBinContent( bin ) == 0: 
                        shift = variants[1-d].GetBinContent(bin); shift = max(5e-6, shift)
                        variants[d].SetBinContent( bin, h.raw().GetBinContent( bin )**2/shift)
                    if variants[d].GetBinContent( bin )/h.raw().GetBinContent(bin) > 10: 
                        print "Warning: big shift in template for %s %s %s %s in bin %d: variation = %g"%( binname, p, name, d, bin, variants[d].GetBinContent( bin )/h.raw().GetBinContent(bin))
                        variants[d].SetBinContent( bin, 10*h.raw().GetBinContent(bin) )
                    if variants[d].GetBinContent( bin )/h.raw().GetBinContent(bin) < 0.1: 
                        print "Warning: big shift in template for %s %s %s %s in bin %d: variation = %g"%( binname, p, name, d, bin, variants[d].GetBinContent( bin )/h.raw().GetBinContent(bin))
                        variants[d].SetBinContent( bin, 0.1*h.raw().GetBinContent(bin) )

            effshape[p] = variants 
    if isShape:
        if options.regularize: 
            for p in procs:
                report[p].regularizeVariation(name,binname=binname)
        systs[name] = ("shape", dict((p,"1" if p in effshape else "-") for p in procs), effshape)
    else:
        effyield = dict((p,"-") for p in procs)
        isNorm = False
        for p,(hup,hdn) in effshape.iteritems():
            i0 = allyields[p]
            kup, kdn = hup.Integral()/i0, hdn.Integral()/i0
            if abs(kup*kdn-1)<1e-5:
                if abs(kup-1)>2e-4:
                    effyield[p] = "%.3f" % kup
                    isNorm = True
            else:
                effyield[p] = "%.3f/%.3f" % (kdn,kup)
                isNorm = True
        if isNorm:
            if name.endswith("_lnU"):
                systs[name] = ("lnU", effyield, {})
            else:
                systs[name] = ("lnN", effyield, {})
  # make a new list with only the ones that have an effect
  nuisances = sorted(systs.keys())

  datacard = open(outdir+binname+".txt", "w"); 
  datacard.write("## Datacard for cut file %s\n"%args[1])
  datacard.write("shapes *        * %s.root x_$PROCESS x_$PROCESS_$SYSTEMATIC\n" % binname)
  datacard.write('##----------------------------------\n')
  datacard.write('bin         %s\n' % binname)
  datacard.write('observation %s\n' % allyields['data_obs'])
  datacard.write('##----------------------------------\n')
  klen = max([7, len(binname)]+[len(p) for p in procs])
  kpatt = " %%%ds "  % klen
  fpatt = " %%%d.%df " % (klen,3)
  npatt = "%%-%ds " % max([len('process')]+map(len,nuisances))
  datacard.write('##----------------------------------\n')
  datacard.write((npatt % 'bin    ')+(" "*6)+(" ".join([kpatt % binname  for p in procs]))+"\n")
  datacard.write((npatt % 'process')+(" "*6)+(" ".join([kpatt % p        for p in procs]))+"\n")
  datacard.write((npatt % 'process')+(" "*6)+(" ".join([kpatt % iproc[p] for p in procs]))+"\n")
  datacard.write((npatt % 'rate   ')+(" "*6)+(" ".join([fpatt % allyields[p] for p in procs]))+"\n")
  datacard.write('##----------------------------------\n')
  towrite = [ report[p].raw() for p in procs ] + [ report["data_obs"].raw() ]
  for name in nuisances:
    (kind,effmap,effshape) = systs[name]
    datacard.write(('%s %5s' % (npatt % name,kind)) + " ".join([kpatt % effmap[p]  for p in procs]) +"\n")
    for p,(hup,hdn) in effshape.iteritems():
        towrite.append(hup.Clone("x_%s_%sUp"   % (p,name)))
        towrite.append(hdn.Clone("x_%s_%sDown" % (p,name)))
  if options.autoMCStats: 
    datacard.write('* autoMCStats %d\n' % options.autoMCStatsValue)
    #print allyields[p].GetBinContent(1) for p in procs
  
if options.tik:
    genlabels = options.tik[0].split(",")
    rlabels = options.tik[1].split(",")
    if(len (genlabels) != len(rlabels)): 
        raise RuntimeError("Len Gen bins is different from len signal strenght please check")
        
    #print genlabels
    #print rlabels
    
    for p in procs:
        h = report[p]
        if str(genlabels[0]) in p:
            sum0=0
            for i in range(1,h.GetNbinsX()+1):
                sum0 += h.GetBinContent(i)
            print "sum0 ", round(sum0,3)
            
        if str(genlabels[1]) in p:
            sum1=0
            for i in range(1,h.GetNbinsX()+1):
                sum1 += h.GetBinContent(i)
            print "sum1 ", sum1


        if str(genlabels[2]) in p:
            sum2=0
            for i in range(1,h.GetNbinsX()+1):
                sum2 += h.GetBinContent(i)
            print "sum2 ",sum2
            
        if str(genlabels[3]) in p:
            sum3=0
            for i in range(1,h.GetNbinsX()+1):
                sum3 += h.GetBinContent(i)
            print "sum3 ",sum3


        if str(genlabels[4]) in p:
            sum4=0
            for i in range(1,h.GetNbinsX()+1):
                sum4 += h.GetBinContent(i)
            print "sum4 ",sum4


        if str(genlabels[5]) in p:
            sum5=0
            for i in range(1,h.GetNbinsX()+1):
                sum5 += h.GetBinContent(i)
            print "sum5 ", sum5

    datacard.write('constr1 constr -'+str(rlabels[0])+'*('+str(sum0)+')+('+str(sum0)+')+'+str(rlabels[1])+'*('+str(sum1)+')-('+str(sum1)+') {rBin1,rBin2} delta[0.03]'+'\n')
    datacard.write('constr2 constr '+str(rlabels[0])+'*('+str(sum0)+')-('+str(sum0)+')-2*'+str(rlabels[1])+'*('+str(sum1)+')+2*('+str(sum1)+')+'+str(rlabels[2])+'*('+str(sum2)+')-('+str(sum2)+') {rBin1,rBin2,rBin3} delta[0.03]'+'\n')
    datacard.write('constr3 constr '+str(rlabels[1])+'*('+str(sum1)+')-('+str(sum1)+')-2*'+str(rlabels[2])+'*('+str(sum2)+')+2*('+str(sum2)+')+'+str(rlabels[3])+'*('+str(sum3)+')-('+str(sum3)+') {rBin2,rBin3,rBin4} delta[0.03]'+'\n')
    datacard.write('constr4 constr '+str(rlabels[2])+'*('+str(sum2)+')-('+str(sum2)+')-2*'+str(rlabels[3])+'*('+str(sum3)+')+2*('+str(sum3)+')+'+str(rlabels[4])+'*('+str(sum4)+')-('+str(sum4)+') {rBin3,rBin4,rBin5} delta[0.03]'+'\n')
    datacard.write('constr5 constr '+str(rlabels[3])+'*('+str(sum3)+')-('+str(sum3)+')-2*'+str(rlabels[4])+'*('+str(sum4)+')+2*('+str(sum4)+')+'+str(rlabels[5])+'*('+str(sum5)+')-('+str(sum5)+') {rBin4,rBin5,rBin6} delta[0.03]'+'\n')

if options.SVD:
    rlabels = options.SVD.split(",")
    #print options.SVD
    #print rlabels
    datacard.write('constr1 constr -'+str(rlabels[0])+'+'+str(rlabels[1])+' {rBin1,rBin2} delta[0.03]'+'\n')
    datacard.write('constr2 constr '+str(rlabels[0])+'-2*'+str(rlabels[1])+'+'+str(rlabels[2])+' {rBin1,rBin2,rBin3} delta[0.03]'+'\n')
    datacard.write('constr3 constr '+str(rlabels[1])+'-2*'+str(rlabels[2])+'+'+str(rlabels[3])+' {rBin2,rBin3,rBin4} delta[0.03]'+'\n')
    datacard.write('constr4 constr '+str(rlabels[2])+'-2*'+str(rlabels[3])+'+'+str(rlabels[4])+' {rBin3,rBin4,rBin5} delta[0.03]'+'\n')
    datacard.write('constr5 constr '+str(rlabels[3])+'-2*'+str(rlabels[4])+'+'+str(rlabels[5])+' {rBin4,rBin5,rBin6} delta[0.03]'+'\n')

workspace = ROOT.TFile.Open(outdir+binname+".root", "RECREATE")
for h in towrite:
    workspace.WriteTObject(h,h.GetName())
workspace.Close()

print "Wrote to {0}.txt and {0}.root ".format(outdir+binname)
if options.tik:
    print "You are now ready to run the tikhonov unfolding -- REMINDER: delta is set to 0.03,remeber to adjust it"
if options.SVD:
    print "You are now ready to run the SVD unfolding -- REMINDER: delta is set to 0.03,remeber to adjust it"
