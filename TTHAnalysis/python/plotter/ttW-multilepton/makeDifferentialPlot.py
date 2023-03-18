import ROOT as r 
import collections
import math 



r.gROOT.ProcessLine(".x tdrstyle.cc")
r.gStyle.SetOptStat(0)
r.gStyle.SetOptTitle(0)
r.gROOT.SetBatch(True)

_noDelete={}
def doSpam(text,x1,y1,x2,y2,align=12,fill=False,textSize=0.033,_noDelete={}):
    cmsprel = r.TPaveText(x1,y1,x2,y2,"NDC");
    cmsprel.SetTextSize(textSize);
    cmsprel.SetFillColor(0);
    cmsprel.SetFillStyle(1001 if fill else 0);
    cmsprel.SetLineStyle(2);
    cmsprel.SetLineColor(0);
    cmsprel.SetTextAlign(align);
    cmsprel.SetTextFont(42);
    cmsprel.AddText(text);
    cmsprel.Draw("same");
    _noDelete[text] = cmsprel; ## so it doesn't get deleted by PyROOT                                                                                                   
    return cmsprel


def hypot(a,b):
    return math.sqrt(a**2+b**2)


tf=r.TFile.Open("genlevel.root")
reference=tf.Get("gen_lep1_pt_ttW")

tf_fit = r.TFile.Open("higgsCombine.Test.MultiDimFit.mH120.root")
lim=tf_fit.Get("limit")

maxim=0
gr=r.TGraphAsymmErrors(len(reference))
for bin in range(reference.GetNbinsX()):
    values=[]
    for entry in lim:
        values.append( getattr(entry, 'r_TTW_lep1_pt_bin%d'%(bin+1)) )
    upvar=max(values)
    dnvar=min(values)
    values.remove(upvar); values.remove(dnvar)
    nom=values[0]
    print(nom, upvar, dnvar)
    xval=reference.GetBinCenter(bin)
    binwidth=reference.GetBinWidth(bin)
    
    gr.SetPoint(bin-1, xval, nom*reference.GetBinContent(bin+1))
    gr.SetPointEXhigh( bin-1,binwidth/2)
    gr.SetPointEXlow( bin-1,binwidth/2)
    gr.SetPointEYhigh( bin-1,(upvar-nom)*reference.GetBinContent(bin+1))
    gr.SetPointEYlow( bin-1,(nom-dnvar)*reference.GetBinContent(bin+1))
    maxim=xval+binwidth/2
    
gr.SetFillColor(r.kGray)

            
tokeep=[]
topSpamSize=1.2
plotformat = (600,600)
height = plotformat[1]+150
c1 = r.TCanvas("_canvas", '', plotformat[0], height)
c1.SetWindowSize(plotformat[0] + (plotformat[0] - c1.GetWw()), (plotformat[1]+150 + (plotformat[1]+150 - c1.GetWh())));
p1 = r.TPad("pad1","pad1",0,0.30,1,1);
p1.SetTopMargin(p1.GetTopMargin()*topSpamSize);
p1.SetBottomMargin(0)
p1.Draw();
p2 = r.TPad("pad2","pad2",0,0,1,0.30);
p2.SetTopMargin(0)
p2.SetBottomMargin(0.3);
p2.SetFillStyle(0);
p2.Draw();
p1.cd();

doSpam('#scale[1.1]{#bf{CMS}} #scale[0.9]{#it{Preliminary}}',  0.16, .955,0.6, .995, align=12, textSize=0.033*1.4)
doSpam('59.7 fb^{-1} (13 TeV)',  0.67, .955,0.99, .995, align=12, textSize=0.033*1.4)



frame=r.TH1F("frame","",1, 0, maxim)
frame.GetXaxis().SetTitleFont(42)
frame.GetXaxis().SetTitleSize(0.06)
frame.GetXaxis().SetTitleOffset(1.1)
frame.GetXaxis().SetLabelFont(42)
frame.GetXaxis().SetLabelSize(0.06)
frame.GetXaxis().SetLabelOffset(0.007)
frame.GetYaxis().SetTitleFont(42)
frame.GetYaxis().SetTitleSize(0.12)
frame.GetYaxis().SetTitleOffset(2.0)
frame.GetYaxis().SetLabelFont(42)
frame.GetYaxis().SetLabelSize(0.12)
frame.GetYaxis().SetLabelOffset(0.007)
frame.GetYaxis().SetTitle("#frac{d#sigma}{d p_{T} (lep)}")
frame.GetXaxis().SetTitle("p_{T} (lep)")
frame.GetXaxis().SetNdivisions(510)
frame.GetYaxis().SetRangeUser(0,25)


frame.Draw()
gr.Draw("E,same")


p2.cd();
frameratio=r.TH1F("ratioframe","",1, 10, 120)
frameratio.GetXaxis().SetTitle("p_{T} (lep)")
frameratio.SetBinError(1,0)
frameratio.SetBinContent(1,1)
frameratio.GetXaxis().SetTitleFont(42)
frameratio.GetXaxis().SetTitleSize(0.14)
frameratio.GetXaxis().SetTitleOffset(1.0)
frameratio.GetXaxis().SetLabelFont(42)
frameratio.GetXaxis().SetLabelSize(0.14)
frameratio.GetXaxis().SetLabelOffset(0.015)
frameratio.GetYaxis().SetNdivisions(505)
frameratio.GetYaxis().SetTitleFont(42)
frameratio.GetYaxis().SetTitleSize(0.14)
offset = 0.62
frameratio.GetYaxis().SetTitleOffset(offset)
frameratio.GetYaxis().SetLabelFont(42)
frameratio.GetYaxis().SetLabelSize(0.14)
frameratio.GetYaxis().SetLabelOffset(0.01)
frameratio.GetYaxis().SetDecimals(True) 
frameratio.GetYaxis().SetTitle("Data/MC")
frame.GetXaxis().SetLabelOffset(999) ## send them away
frame.GetXaxis().SetTitleOffset(999) ## in outer space
frame.GetYaxis().SetTitleSize(0.06)
frame.GetYaxis().SetTitleOffset(1.48)
frame.GetYaxis().SetLabelSize(0.05)
frame.GetYaxis().SetLabelOffset(0.007)
leg=r.TLegend(0.5,0.2,0.9,0.4)
leg.SetLineColor(0)
leg.SetFillColor(0)
leg.SetShadowColor(0)
leg.SetTextFont(42)
leg.SetTextSize(0.060)


frameratio.Draw()



p2.cd()
#gr_ratio.Draw('p,E,same')


plot='lep_pt'
c1.SaveAs('plot_%s.png'%(plot.replace('.','p')))
c1.SaveAs('plot_%s.pdf'%(plot.replace('.','p')))
    
                            
