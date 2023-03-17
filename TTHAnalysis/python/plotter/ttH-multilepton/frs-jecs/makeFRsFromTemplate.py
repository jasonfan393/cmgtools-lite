
#fake_rates_to_add=["jer%d"%i for i in range(6)]
fake_rates_to_add=["jesHEMIssue"]

for side in ["Up","Down"]:
    for fr in fake_rates_to_add:
        template = open("fr-template.txt").read()
        out=template.replace("template",fr+side)
        outf=open("fr_%s.txt"%(fr+side),'w')
        outf.write(out)
        outf.close()
