import os, re
from susy_edge.scan_server import Scan
whichscan = 'slepton'
cardDirectory="cards_apr1"
outputDirectory="cards_apr1_sigscan"




scan = Scan(whichscan)
cardRegex = scan.cardRegex
scanName  = scan.name
os.system('mkdir -p ' + outputDirectory ) 
def runIt(command, debug=True, batch=True):
    if batch: 
        command = 'sbatch -p  cpupower --wrap "%s"'%command
    if debug: 
        print command
        return
    os.system(command)
        


cards = {}
pattern = re.compile( cardRegex ) 
for card in os.listdir(cardDirectory + '/'): 
    match = pattern.search( card )
    if not match: continue
    point = (match.group('m1'), match.group('m2'))
    if point in cards: 
        cards[point].append( cardDirectory + '/' + card ) 
    else: 
        cards[point] = [cardDirectory + '/' + card]
nsrs = -1
for point in cards: 
    m1 = point[0]
    m2 = point[1]
    if nsrs < 0: 
        nsrs = len(cards[point])
    if nsrs != len(cards[point]):
        raise RuntimeError("Number of cards for point (%s,%s) is different"%(point[0],point[1]))
    name = "%s_%s_%s"%(scanName, m1,m2)
    if whichscan == "slepton":
        command = "combineCards.py %s >  %s/%s.dat;"%(" ".join( ['%s=%s'%(os.path.basename(x).replace('_m1_%s_m2_%s.card.txt'%(m1,m2),''),x) for x in cards[point] ]),outputDirectory,name)
        command+= "echo 'dy_nojet_high_rate rateParam slepton_*_nojets_high DY 1 [0,10000]'   >> %s/%s.dat;"%(outputDirectory,name)
        command+= "echo 'dy_nojet_low_rate rateParam slepton_*_nojets_low DY 1 [0,10000]'         >> %s/%s.dat;"%(outputDirectory,name)
        command+= "echo 'dy_nojet_med_rate rateParam slepton_*_nojets_med DY 1 [0,10000]'         >> %s/%s.dat;"%(outputDirectory,name)
        command+= "echo 'dy_nojet_vhigh_rate rateParam slepton_*_nojets_vhigh DY 1 [0,10000]' >> %s/%s.dat;"%(outputDirectory,name)

        command+= "echo 'dy_withjet_high_rate rateParam slepton_*_withjets_high DY 1 [0,10000]'   >> %s/%s.dat;"%(outputDirectory,name)
        command+= "echo 'dy_withjet_low_rate rateParam slepton_*_withjets_low DY 1 [0,10000]'         >> %s/%s.dat;"%(outputDirectory,name)
        command+= "echo 'dy_withjet_med_rate rateParam slepton_*_withjets_med DY 1 [0,10000]'         >> %s/%s.dat;"%(outputDirectory,name)
        command+= "echo 'dy_withjet_vhigh_rate rateParam slepton_*_withjets_vhigh DY 1 [0,10000]' >> %s/%s.dat;"%(outputDirectory,name)

        command+= 'text2workspace.py %s/%s.dat --channel-masks -o %s/%s_wps.root;'%(outputDirectory,name,outputDirectory,name)
        command+= 'combineTool.py %s/%s_wps.root -M MultiDimFit --setParameters mask_slepton_offz_nojets_med=1,mask_slepton_offz_nojets_low=1,mask_slepton_offz_nojets_high=1,mask_slepton_offz_nojets_vhigh=1,mask_slepton_offz_withjets_med=1,mask_slepton_offz_withjets_low=1,mask_slepton_offz_withjets_high=1,mask_slepton_offz_withjets_vhigh=1,r=0 --saveWorkspace   --freezeParameter r  -n sidebandfit_%s;'%(outputDirectory,name,name)
        command+= "mv higgsCombinesidebandfit_%s.MultiDimFit.mH120.root %s/.; "%(name,outputDirectory)
        command+= "combineTool.py %s/higgsCombinesidebandfit_%s.MultiDimFit.mH120.root --setParameters mask_slepton_offz_nojets_med=0,mask_slepton_offz_nojets_low=0,mask_slepton_offz_nojets_high=0,mask_slepton_offz_nojets_vhigh=0,mask_slepton_offz_withjets_med=0,mask_slepton_offz_withjets_low=0,mask_slepton_offz_withjets_high=0,mask_slepton_offz_withjets_vhigh=0  -M AsymptoticLimits --snapshotName MultiDimFit -n fit_%s; "%(outputDirectory,name,name)
        command+= "mv higgsCombinefit_%s.AsymptoticLimits.mH120.root %s/.;"%(name,outputDirectory)
        command+= "combineTool.py %s/higgsCombinesidebandfit_%s.MultiDimFit.mH120.root --setParameters mask_slepton_offz_nojets_med=0,mask_slepton_offz_nojets_low=0,mask_slepton_offz_nojets_high=0,mask_slepton_offz_nojets_vhigh=0,mask_slepton_offz_withjets_med=0,mask_slepton_offz_withjets_low=0,mask_slepton_offz_withjets_high=0,mask_slepton_offz_withjets_vhigh=0  -M Significance --snapshotName MultiDimFit -n fit_%s;  --uncapped 1 --rMin -4 "%(outputDirectory,name,name)
        command+= "mv higgsCombinefit_%s.Significance.mH120.root %s/.;"%(name,outputDirectory)
    else:
        command = 'combineCards.py  ' + " ".join( cards[point] ) + ' > %s/%s.dat; '%(outputDirectory,name)
        command+= 'combine -M AsymptoticLimits --name {name} {dir}/{name}.dat;'.format(name=name, dir=outputDirectory)
        command+= 'mv higgsCombine{name}.AsymptoticLimits.mH120.root {dir}/'.format(name=name, dir=outputDirectory)
    runIt( command ) 
    

    
