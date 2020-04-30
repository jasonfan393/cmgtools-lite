import ROOT as r 
import susy_edge.xsec_server as xsec_server
import copy


class binning:
    def __init__(self, mi, ma, w):
        self._min = mi
        self._max = ma
        self.w  = w
        self.n  = abs(ma-mi)/w

class limitContainer:
    def __init__(self):
        self.ex_obs = 0 
        self.ex_obs_p1s = 0
        self.ex_obs_m1s = 0 
        self.ex_exp = 0
        self.ex_exp_p1s = 0
        self.ex_exp_m1s = 0

class Scan: 
    def __init__(self, name):
        self.name = name
        if self.name == 'slepton': 
            self.regions = [ ('slepton_nojet', '-E ^sr_wojets --neglist ZZ_sub --plotgroup ZZ+=ZZ_sub '), ('slepton_withjets', '-E ^sr_withjet --neglist ZZ_sub --plotgroup ZZ+=ZZ_sub ') ]
            self.signalregex = 'TSlepslep_(?P<m1>.*)_(?P<m2>.*)'
            self.categorize  = { 'slepton_nojet'    : 'MET_pt_Edge [100,150,225,300,14000] low,med,high,vhigh',
                                 'slepton_withjets' : 'MET_pt_Edge [100,150,225,300,14000] low,med,high,vhigh'
            }
            self.cutfile = 'susy-edge/regions/slepton.txt'
            self.mca = "susy-edge/mca-{year}-dd-data-offz.txt"
            self.cardRegex = "slepton.*_m1_(?P<m1>.*)_m2_(?P<m2>.*).card.txt"
            self.xbins = binning(100,1000,10)
            self.ybins = binning(0,1000,10)
            self.xsection = xsec_server.slep
            self.maxmass = 1000
        elif self.name == "t5zz": 
            self.regions = []
            self.categorize = {} 
            for subreg in 'SRA_btag,SRA_bveto,SRB_btag,SRB_bveto,SRC_btag,SRC_bveto'.split(','):
                self.regions.append( (subreg, '-E ^%s'%subreg))
                self.categorize[subreg] = "MET_pt_Edge " + ("[50,100,150,230,300,14000] norm,vlow,low,med,high" if 'SRC' in subreg else "[50,100,150,250,300] norm,low,med,high")
            
        else: 
            raise RuntimeError

    def xsecs(self, mass, var=0): 
        mass1 = int(mass) 
        mass2 = int(mass)
        mass  = float(mass)
        while mass1 not in self.xsection: 
            mass1=mass1+1
            if mass1 > self.maxmass: 
                return 0 
        while mass2 not in self.xsection: 
            mass2=mass2-1
            if mass2 > self.maxmass: 
                return 0 
        variation1 = 0; variation2 = 0 
        if var > 0: 
            variation1 = self.xsection[mass1][1]*self.xsection[mass1][0]/100.
            variation2 = self.xsection[mass2][1]*self.xsection[mass2][0]/100.
        elif var < 0: 
            variation1 = -self.xsection[mass1][2]*(self.xsection[mass1][0]/100.)
            variation2 = -self.xsection[mass2][2]*(self.xsection[mass2][0]/100.)

        ret1 = self.xsection[mass1][0]+variation1
        ret2 = self.xsection[mass2][0]+variation2
        if mass1 == mass2: 
            return ret1
        return ret1 + (ret2-ret1)*(float(mass)-float(mass1))/(float(mass2)-mass1)

    def getEmptyScanHist(self, name):
        return r.TH2F(name, '',
                      self.xbins.n+1, self.xbins._min-self.xbins.w/2.,
                      self.xbins._max+self.xbins.w/2., self.ybins.n+1,
                      self.ybins._min-self.ybins.w/2.,
                      self.ybins._max+self.ybins.w/2.)
    
    def getSmoothedSignificanceGraphs(self):
        tmp_2d_graph = r.TGraph2D(getattr(self, 'ex_obs'))
        xbinsize = 12.5; ybinsize = 12.5
        tmp_2d_graph.SetNpx( int((tmp_2d_graph.GetXmax() - tmp_2d_graph.GetXmin())/xbinsize) )
        tmp_2d_graph.SetNpy( int((tmp_2d_graph.GetYmax() - tmp_2d_graph.GetYmin())/ybinsize) )
        setattr( self, 'ex_obs',  tmp_2d_graph.GetHistogram())
        self.getSmoothedGraph(self.ex_obs)
        print self.ex_obs
        setattr(self, 'ul_histo', copy.deepcopy(self.ex_obs))
        #self.ul_histo.Draw("colz")
            
    def getSmoothedGraphs(self):
        for hist in ['ex_obs', 'ex_obs_p1s', 'ex_obs_m1s', 'ex_exp', 'ex_exp_m1s', 'ex_exp_p1s']: 
            tmp_2d_graph = r.TGraph2D(getattr(self, '%s'%hist))
            xbinsize = 12.5; ybinsize = 12.5
            tmp_2d_graph.SetNpx( int((tmp_2d_graph.GetXmax() - tmp_2d_graph.GetXmin())/xbinsize) )
            tmp_2d_graph.SetNpy( int((tmp_2d_graph.GetYmax() - tmp_2d_graph.GetYmin())/ybinsize) )
            tmp_2d_histo = tmp_2d_graph.GetHistogram()
            tmp_graph_list = tmp_2d_graph.GetContourList(1.0)
            tmp_graph = tmp_graph_list[max( (i.GetN(),j) for j,i in enumerate( tmp_graph_list )  )[1]]
            setattr(self, '%s_graph'%hist, copy.deepcopy(tmp_graph    ) )
            setattr(self, '%s_2dg'  %hist, copy.deepcopy(tmp_2d_graph ) )
            setattr(self, '%s_2dh'  %hist, copy.deepcopy(tmp_2d_histo ) )

            self.getSmoothedGraph( getattr(self,'%s_2dh'%hist))

        # now make upper limit in terms of the cross-section
        h_rhisto = copy.deepcopy(self.ex_obs)
        for i in range(h_rhisto.GetNbinsX()+1):
            for j in range(h_rhisto.GetNbinsY()+1):
                xs = self.xsecs( int(h_rhisto.GetXaxis().GetBinCenter(i)) ) 
                h_rhisto.SetBinContent(i,j,h_rhisto.GetBinContent(i,j)*xs)
        gr2d = r.TGraph2D(h_rhisto)
        xbinsize = 12.5; ybinsize = 12.5
        gr2d.SetNpx( int((gr2d.GetXmax() - gr2d.GetXmin())/xbinsize) )
        gr2d.SetNpy( int((gr2d.GetYmax() - gr2d.GetYmin())/ybinsize) )
        tmp_2d_histo = gr2d.GetHistogram()
        tmp_2d_histo.SetName('ul_histo')
        setattr(self, 'ul_histo', copy.deepcopy(tmp_2d_histo))

    def getSmoothedGraph(self, h_orig):
        tmp_name       = (h_orig.GetName()+'_smoothed').replace('Graph2D_from_','')
        tmp_name_graph = tmp_name+'_graph'
        h_smoothed = h_orig.Clone(tmp_name)
        smoothedbins = []
        for i in range(h_smoothed.GetNbinsX()+1):
            for j in range(h_smoothed.GetNbinsY()+1):
                if j > 0 and not h_smoothed.GetBinContent(i,j):
                    h_smoothed.SetBinContent(i,j,h_smoothed.GetBinContent(i-1,j))
                    smoothedbins.append((i,j))
                    break
        h_smoothed.Smooth(1, 'k3a')
        for i,j in smoothedbins:
            h_smoothed.SetBinContent(i,j,0.)
        
        smcopy = copy.deepcopy(h_smoothed)
        smoothed_2dg = r.TGraph2D(smcopy)
        xbinsize = 5.; ybinsize = 5.
        smoothed_2dg.SetNpx( int((smoothed_2dg.GetXmax() - smoothed_2dg.GetXmin())/xbinsize) )
        smoothed_2dg.SetNpy( int((smoothed_2dg.GetYmax() - smoothed_2dg.GetYmin())/ybinsize) )
        kk = smoothed_2dg.GetHistogram() ## have to call this, otherwise root will freak out
        c = smoothed_2dg.GetContourList(1.0)
        smoothed_g   = c[max( (i.GetN(),j) for j,i in enumerate( c )  )[1]]
        smoothed_g.SetName(tmp_name_graph)
        setattr(self, tmp_name      , copy.deepcopy(h_smoothed) )
        setattr(self, tmp_name_graph, copy.deepcopy(smoothed_g) )#copy.deepcopy(graph[0][1]) )

    def writeRelevantHistsToFile(self, suffix, noExclusionLines):
        
        f = r.TFile('makeExclusionPlot/config/%s/%s%s_results.root'%('SUS20001',suffix,self.name),'RECREATE')
        f.cd()
        self.ul_histo.Write()
        if not noExclusionLines:
            self.ex_exp_smoothed_graph    .Write()
            self.ex_exp_p1s_smoothed_graph.Write()
            self.ex_exp_m1s_smoothed_graph.Write()
            self.ex_obs_smoothed_graph    .Write()
            self.ex_obs_p1s_smoothed_graph.Write()
            self.ex_obs_m1s_smoothed_graph.Write()
        f.Close()
