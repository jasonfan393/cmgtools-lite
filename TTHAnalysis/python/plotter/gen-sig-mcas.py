import ROOT as r 
import re 
import os 

slepton = {
    50  :5.368  ,
    80  : 0.8014   ,
    100 : 0.3657   ,
    120 : 0.1928   ,
    125 : 0.1669   ,
    140 : 0.1116   ,
    150 : 0.08712  ,
    160 : 0.06896  ,
    175 : 0.04975  ,
    180 : 0.04485  ,
    200 : 0.03031  ,
    220 : 0.02115  ,
    225 : 0.01941  ,
    240 : 0.01514  ,
    250 : 0.01292  ,
    260 : 0.01108  ,
    275 : 0.008875 ,
    280 : 0.008259 ,
    300 : 0.006254 ,
    320 : 0.004802 ,
    340 : 0.003732 ,
    360 : 0.002931 ,
    380 : 0.002325 ,
    400 : 0.001859 ,
    440 : 0.001216 ,
    500 : 0.0006736,
    600 : 0.0002763,
    700 : 0.0001235,
    800 : 5.863e-05,
    900 : 2.918e-05,
    1000: 1.504e-05,
}

tchiwz = {  # in fb
  100   :  22670.1   ,  
  125   :  10034.8   ,  
  150   :  5180.86   ,  
  175   :  2953.28   ,  
  200   :  1807.39   ,  
  225   :  1165.09   ,  
  250   :  782.487   ,  
  275   :  543.03    ,  
  300   :  386.936   ,  
  325   :  281.911   ,  
  350   :  209.439   ,  
  375   :  158.06    ,  
  400   :  121.013   ,  
  425   :  93.771    ,  
  450   :  73.4361   ,  
  475   :  58.0811   ,  
  500   :  46.3533   ,  
  525   :  37.2636   ,  
  550   :  30.1656   ,  
  575   :  24.5798   ,  
  600   :  20.1372   ,  
  625   :  16.5706   ,  
  650   :  13.7303   ,  
  675   :  11.3975   ,  
  700   :  9.51032   ,  
  725   :  7.9595    ,  
  750   :  6.69356   ,  
  775   :  5.63562   ,  
  800   :  4.75843   ,  
  825   :  4.02646   ,  
  850   :  3.42026   ,  
  875   :  2.90547   ,  
  900   :  2.49667   ,  
  925   :  2.12907   ,  
  950   :  1.8164    ,  
  975   :  1.56893   ,  
  1000  :  1.34352   ,  
  1025  :  1.15949   ,  
  1050  :  0.997903  ,  
  1075  :  0.86504   ,  
  1100  :  0.740372  ,  
  1125  :  0.647288  ,  
  1150  :  0.555594  ,  
  1175  :  0.486863  ,  
  1200  :  0.415851  ,  
  1225  :  0.362455  ,  
  1250  :  0.316975  ,  
  1275  :  0.276522  ,  
  1300  :  0.240739  ,  
  1325  :  0.20999   ,  
  1350  :  0.185601  ,  
  1375  :  0.161343  ,  
  1400  :  0.131074  ,  
  1425  :  0.121045  ,  
  1450  :  0.110889  ,  
  1475  :  0.0906868 ,  
  1500  :  0.0795585 ,  
  1525  :  0.0694615 ,  
  1550  :  0.0610387 ,  
  1575  :  0.0531447 ,  
  1600  :  0.0468796 ,  
  1625  :  0.0413666 ,  
  1650  :  0.0359383 ,  
  1675  :  0.0313343 ,  
  1700  :  0.0271773 ,  
  1725  :  0.0239993 ,  
  1750  :  0.0209773 ,  
  1775  :  0.0183553 ,  
  1800  :  0.0161098 ,  
  1825  :  0.0139216 ,  
  1850  :  0.0120539 ,  
  1875  :  0.0104658 ,  
  1900  :  0.00937288,  
  1925  :  0.00814838,  
  1950  :  0.00713734,  
  1975  :  0.00621999,  
  2000  :  0.00544778,  
}
scan = 'TSlepslep'


events = {
    'TSlepslep' : r.TFile.Open("/pool/ciencias/HeppyTrees/EdgeZ/Edge/Edge_260120_signals/TSlepSlep_2016/nanoAODskim/Events.root"),
    'TSlepslep2': r.TFile.Open("/pool/ciencias/HeppyTrees/EdgeZ/Edge/Edge_260120_signals/TSlepSlep_500To1300_2016/nanoAODskim/Events.root"),
    'TChiWZ' : r.TFile.Open("/pool/phedex/userstorage/sscruz/NanoAOD/Edge_171119_merge/TChiWZ_325to1000_2016/nanoAODskim/Events.root"),
}
events_2017 = {
    'TSlepslep' : r.TFile.Open("/pool/ciencias/HeppyTrees/EdgeZ/Edge/Edge_260120_signals/TSlepSlep_2017/nanoAODskim/Events.root"),
    'TSlepslep2': r.TFile.Open("/pool/ciencias/HeppyTrees/EdgeZ/Edge/Edge_260120_signals/TSlepSlep_500To1300_2017/nanoAODskim/Events.root"),
    'TChiWZ' : r.TFile.Open("/pool/phedex/userstorage/sscruz/NanoAOD/Edge_171119_merge/TChiWZ_325to1000_2017/nanoAODskim/Events.root"),
}
events_2018 = {
    'TSlepslep' : r.TFile.Open("/pool/ciencias/HeppyTrees/EdgeZ/Edge/Edge_260120_signals/TSlepSlep_2018/nanoAODskim/Events.root"),
    'TSlepslep2': r.TFile.Open("/pool/ciencias/HeppyTrees/EdgeZ/Edge/Edge_260120_signals/TSlepSlep_500To1300_2018/nanoAODskim/Events.root"),
    'TChiWZ' : r.TFile.Open("/pool/phedex/userstorage/sscruz/NanoAOD/Edge_171119_merge/TChiWZ_325to1000_2018/nanoAODskim/Events.root"),
}
dnames = { 
    'TSlepslep' : "TSlepslep",
    'TSlepslep2' : "TSlepslep",
    'TChiWZ'    : "TChiWZ_325to1000",
}
skimFileAsWell = False
runs_2016 = events[scan].Get("Runs_SUSY")
runs_2017 = events_2017[scan].Get("Runs_SUSY")
runs_2018 = events_2018[scan].Get("Runs_SUSY")

Events_2016 = events[scan].Get("Events")
Events_2017 = events_2017[scan].Get("Events")
Events_2018 = events_2018[scan].Get("Events")

pattern = re.compile("sumWeights_(?P<m1>[0-9]+)_(?P<m2>[0-9]+)")
mcas = { '2016' : '',
         '2017' : '',
         '2018' : ''
}
xsec_dict = slepton if "TSlepslep" in scan else tchiwz if scan == "TChiWZ" else None
for k in runs_2016.GetListOfBranches(): 
    match = pattern.search( k.GetName())
    if not match: 
        continue
    if not runs_2017.GetBranch(k.GetName()): print 'Branch %s is not in 2017'%k.GetName()
    if not runs_2018.GetBranch(k.GetName()): print 'Branch %s is not in 2018'%k.GetName()
    m1,m2 = int(match.group( 'm1')), int(match.group('m2'))
    if m1 in xsec_dict:
        xsec = xsec_dict[m1]
    else: 
        if m1 > 1000: continue
        # interpolate
        m1p = m1; m1m = m1
        while m1p not in xsec_dict: 
            m1p = m1p+1
        while m1m not in xsec_dict: 
            m1m = m1m-1
        xsec = xsec_dict[m1m] + (xsec_dict[m1p]-xsec_dict[m1m])*(m1-m1m)/(m1p-m1m)

    if scan == "TSlepslep":
        xsec = "2*{xsec:4.3e}".format(xsec=xsec)
    elif scan == "TSlepslep2":
        xsec = "2*{xsec:4.3e}".format(xsec=xsec)
    elif scan == "TChiWZ": 
        xsec = "0.10099*{xsec:4.3e}".format(xsec=xsec/1000.)
    else: 
        raise RuntimeError
    for year in '2016,2017,2018'.split(","):
        mcas[year] +='''{scan}_{m1}_{m2}+    : {dname}_{m1}_{m2}_{year} : {xsec} : GenSusyMScan1_mass=={m1}&&GenSusyMScan2_mass=={m2}; FillColor=ROOT.kOrange+6, genSumWeightName="sumWeights_{m1}_{m2}",NormalizeFrom="Runs_SUSY" \n'''.format(dname=dnames[scan], scan=scan, year=year, xsec=xsec, m1=m1,m2=m2) # , SkipMe=True, 
        if skimFileAsWell: 
            print " Writing {dname}_{m1}_{m2}_{year}.root".format(scan=scan,year=year,m1=m1,m2=m2,dname=dnames[scan])
            if os.path.isdir("/pool/cienciasrw/HeppyTrees/EdgeZ/Edge/Edge_260120/slepton_points/{dname}_{m1}_{m2}_{year}/nanoAODskim/".format(scan=scan,year=year,m1=m1,m2=m2,dname=dnames[scan])):
                print 'attempting to override {dname}_{m1}_{m2}_{year}. will skip'.format(scan=scan,year=year,m1=m1,m2=m2,dname=dnames[scan])
            os.system("mkdir -p /pool/cienciasrw/HeppyTrees/EdgeZ/Edge/Edge_260120/slepton_points/{dname}_{m1}_{m2}_{year}/nanoAODskim/".format(scan=scan,year=year,m1=m1,m2=m2,dname=dnames[scan]))
            outf = r.TFile.Open("/pool/cienciasrw/HeppyTrees/EdgeZ/Edge/Edge_260120/slepton_points//{dname}_{m1}_{m2}_{year}/nanoAODskim/Events.root".format(scan=scan,year=year,m1=m1,m2=m2,dname=dnames[scan]),'recreate')
            cpevents = eval("Events_%s"%year).CopyTree('GenSusyMScan1_mass=={m1}&&GenSusyMScan2_mass=={m2}'.format(m1=m1,m2=m2))
            cpevents.Write()
            eval("runs_%s"%year).CloneTree().Write()
            outf.Close()

for year in '2016,2017,2018'.split(","):
    p = open('susy-edge/mca-includes/mca-sig-%s-%s.txt'%(scan, year),'w')
    p.write(mcas[year])
    p.close()

