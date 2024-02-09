import ROOT as r 
import os,sys

folder = sys.argv[1] #folder to run
var = sys.argv[2]    #diff var (is a name for files)
region = sys.argv[3] # 3l or 2lss
todo = sys.argv[4]   #step of the fitting to run
variation = sys.argv[5]
print(todo)
cards = [file for file in os.listdir(folder) if ".txt" in file and "Gen" not in file and region in file]
print("Found the following Cards:")
print(cards)



#Read the Card and get the pois
f = open(folder+"/"+cards[0], "r")
print(folder+"/"+cards[0])
signals = []
for l in f.readlines():
    if "process" in l:
        p = l.split(" ")
        for item in p:
            if "TTW_" in item and not "ooa" in item:
                signals.append(item)
        
if todo == "0":
   print("I'm combining them")
   os.chdir(folder)
   #Combine Cards
   c = "combineCards.py "
   for item in cards:
        c += item+" "
   c += " ../../cr3l/{var}/ttW_cr*.txt".format(var = variation)
   c += " ../../cr4l/{var}/ttW_cr*.txt".format(var = variation) 
#   c += " ../cr3l/ttW_cr*.txt"
#   c += " ../cr3l/ttW_cr*.txt"
   c += " > combined_"+var+"_"+region+".dat"

   print(c)
   if p: 
      os.system(c)


#Run workspace
if todo == "1":
   pois = ""
   for signal in signals:
       pois += " --PO 'map=.*/%s:r_%s[1,-5,10]'"%(signal,signal)

   ws = "text2workspace.py {CARD} -o {WS_NAME} -P  HiggsAnalysis.CombinedLimit.PhysicsModel:multiSignalModel --PO verbose {POIS}".format(CARD = "combined_"+var+"_"+region+".dat", WS_NAME = "ws_"+var+"_"+region+".root",POIS = pois)
   os.chdir(folder)
   
   print(ws)
   if p: 
      os.system(ws)
   

#Run fit
if todo == "2":
   
   params = ""
   for signal in signals:
       params += "r_%s=1,"%(signal)

   rf = "combine -M FitDiagnostics {WS_NAME} -m 125  --freezeParameters MH  -n nominal_{VAR} --robustFit 1 --cminDefaultMinimizerStrategy 0 --X-rtd MINIMIZER_analytic  --X-rtd MINIMIZER_MaxCalls=5000000 --saveWorkspace --saveShapes --saveWithUncertainties".format(WS_NAME ="ws_"+var+"_"+region+".root", VAR= var+"_"+region )
   

   #Run fit for stat
   #--saveWorkspace --saveShapes --saveWithUncertainties
   rff = "combine -M FitDiagnostics %s -m 125 --freezeParameters MH,'rgx{lumi.*}','rgx{CMS_eff.*}','rgx{CMS_ttWl.*}','rgx{CMS_ttHl.*}','rgx{CMS_scale_j.*}',CMS_jesHEMIssue,'rgx{CMS_res_j.*}','rgx{QCDscale_.*}','rgx{pdf_.*}','rgx{BR_.*}',CMS_ttWl_UnclusteredEn   -n freezing_%s --robustFit 1 --cminDefaultMinimizerStrategy 0  --X-rtd MINIMIZER_analytic --X-rtd MINIMIZER_MaxCalls=5000000 --saveWorkspace --saveShapes --saveWithUncertainties"%("ws_"+var+"_"+region+".root", var+"_"+region )
   os.chdir(folder)

   rfff = "combine -M FitDiagnostics %s -m 125 --freezeParameters MH,'rgx{lumi.*}','rgx{CMS_eff.*}','rgx{CMS_ttWl.*}','rgx{CMS_ttHl.*}','rgx{CMS_scale_j.*}',CMS_jesHEMIssue,'rgx{CMS_res_j.*}','rgx{QCDscale_.*}','rgx{pdf_.*}','rgx{BR_.*}','rgx{prop.*}',CMS_ttWl_UnclusteredEn   -n freezing_all_%s --robustFit 1 --cminDefaultMinimizerStrategy 0  --X-rtd MINIMIZER_analytic --X-rtd MINIMIZER_MaxCalls=5000000 --saveWorkspace --saveShapes --saveWithUncertainties"%("ws_"+var+"_"+region+".root", var+"_"+region )

   print('sbatch -c 1 -p batch --wrap "'+rf+'"')
   print('sbatch -c 1 -p batch --wrap "'+rff+'"')
   print('sbatch -c 1 -p batch --wrap "'+rfff+'"')
   if p: 
      os.system('sbatch -c 1 -p batch --wrap "'+rf+'"')
      os.system('sbatch -c 1 -p batch --wrap "'+rff+'"')
      os.system('sbatch -c 1 -p batch --wrap "'+rfff+'"')
   #os.system(rf)
   #os.system(rff)
