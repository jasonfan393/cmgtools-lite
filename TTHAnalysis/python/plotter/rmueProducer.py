#!/usr/bin/env python
#from mcPlots import *
from CMGTools.TTHAnalysis.plotter.mcPlots import *
from CMGTools.TTHAnalysis.plotter.histoWithNuisances import _cloneNoDir
from math import sqrt, hypot

def makeRmue2(ee, mm):
    rmue2 = _cloneNoDir(mm)
    for i in range(1,mm.GetNbinsX()+1):
        print mm.GetBinLowEdge(i), mm.GetBinContent(i), ee.GetBinContent(i)
        rmue2.SetBinContent(i, mm.GetBinContent(i)/ee.GetBinContent(i))
        rmue2.SetBinError(i, hypot( mm.GetBinError(i)/ee.GetBinContent(i), mm.GetBinContent(i)*ee.GetBinError(i)/(ee.GetBinContent(i)**2)))
    return rmue2

def makeRmue(ee, mm):
    rmue2 = makeRmue2(ee, mm)
    rmue  = _cloneNoDir(rmue2)
    for i in range(1,rmue2.GetNbinsX()+1):
        rmue.SetBinContent(i, sqrt(rmue2.GetBinContent(i)))
        rmue.SetBinError(i, 0.5*rmue2.GetBinError(i)/sqrt(rmue2.GetBinContent(i)))
    return rmue

def addRmueParserOptions(parser):
    addMCAnalysisOptions(parser)
    parser.add_option("--select-plot", "--sP", dest="plotselect", action="append", default=[], help="Select only these plots out of the full file")
    parser.add_option("--exclude-plot", "--xP", dest="plotexclude", action="append", default=[], help="Exclude these plots from the full file")

def plotRmue(hdata, hmc):
    c1 = ROOT.TCanvas("roc_canvas","roc_canvas")
    hdata.Draw()
    hdata.GetYaxis().SetRangeUser(1.25,2.5)
    hdata.GetYaxis().SetTitle("r^{2}_{#mu/e}")
    hmc.Draw('same')
    rmue_data=ROOT.TF1("rmue_data", "[0]+[1]/x",20,200)
    rmue_mc=ROOT.TF1("rmue_mc", "[0]+[1]/x",20,200)
    hdata.Fit(rmue_data)
    hmc.Fit(rmue_mc)

    c1.Print('rmue.png')


if __name__ == "__main__":
    from optparse import OptionParser
    parser = OptionParser(usage="%prog [options] mc.txt cuts.txt plotfile.txt")
    addRmueParserOptions(parser)

    (options, args) = parser.parse_args()
    options.globalRebin = 1
    options.allowNegative = True

    ROOT.gROOT.ProcessLine(".x tdrstyle.cc")
    ROOT.gStyle.SetOptStat(0)

    mca  = MCAnalysis(args[0],options)
    cut = CutsFile(args[1],options).allCuts()
    plots = PlotFile(args[2],options).plots()


    pmaps = [  mca.getPlots(p,cut) for p in plots ]
    pmap = pmaps[0]
    hdata_ee = pmap['data_ee']
    hdata_mm = pmap['data_mm']
    hmc_ee = pmap['DY_ee']
    hmc_mm = pmap['DY_mm']

    data_rmue2=makeRmue2( hdata_ee, hdata_mm)
    mc_rmue2=makeRmue2( hmc_ee, hmc_mm)
    

    plotRmue(data_rmue2,mc_rmue2)
