from CMGTools.TTHAnalysis.plotter.susy_edge.scan_server import Scan
whichscan = 'slepton'
asimov= "" # " --asimov background " 
outputfile = "cards/slepton_feb20"

scan = Scan(whichscan)

for region,regops in scan.regions:
    print '''sbatch -c 64 -p short --wrap "python makeShapeCardsNewScan.py --outdir {outputfile} -P /pool/ciencias/HeppyTrees/EdgeZ/Edge/Edge_260120/ -P /pool/ciencias/HeppyTrees/EdgeZ/Edge/Edge_260120/slepton_points/ -f -j 88 -l 35.9,41.4,59.7 --year 2016,2017,2018 -L susy-edge/functions-edge.cc --tree nanoAODskim --split-factor=-1 {mca} {cutfile} -W 'LepSF(Lep1_pt_Edge,Lep1_eta_Edge,Lep1_pdgId_Edge,year)*LepSF(Lep2_pt_Edge,Lep2_eta_Edge,Lep2_pdgId_Edge,year)' 1 1,0.5,1.5 --obj Events --genWeightName genWeight_Edge --Fs {{P}}/1_trigger --FMCs {{P}}/2_btags {asimov} --scanregex \\"{signalregex}\\" --categorize {categorize} --params m1,m2 --unc susy-edge/systUnc.txt --binname {region} --bbb mcstat --FMCs {{P}}/4_kfactor --FMCs {{P}}/6_flavsym {regops}  "'''.format(outputfile=outputfile,signalregex=scan.signalregex, categorize=scan.categorize[region], regops=regops, region=region, cutfile=scan.cutfile, mca=scan.mca, asimov=asimov)
