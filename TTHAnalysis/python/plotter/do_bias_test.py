import os
import subprocess

#variations = "Nominal TTln_cQq13_up TTln_cQq13_dn TTln_cQq83_up TTln_cQq83_dn TTln_cQq11_up TTln_cQq11_dn TTln_cQq18_up TTln_cQq18_dn TTln_ctQ1_up TTln_ctQ1_dn TTln_ctQ8_up TTln_ctQ8_dn TTln_cpt_up TTln_cpt_dn TTln_cpQM_up TTln_cpQM_dn"
variations = "Nominal TTln_cQq13_up "
years = ["2016"]#, "2016APV", "2017", "2018"]
vars = ["njets"]

RED = '\033[0;31m'
GREEN = '\033[0;32m'
BLUE = '\033[0;33m'
NC = '\033[0m'  # No Color

for year in years:
    print("{GREEN}>> Submitting for year {year}{NC}".format(GREEN = GREEN, year = year, NC = NC))
    for variable in vars:
        print("{BLUE}  * Submitting for variable {variable}{NC}".format(BLUE = BLUE, variable = variable, NC = NC))
        for variation in variations.split():
            print("{RED}    + Submitting for variation {variation}{NC}".format(RED = RED, variation = variation, NC = NC))
            python_command = "python ttW_multilepton/make_cards_new.py bias_test_{variable}_{variation} {year} 2lss {variable}".format(variable = variable, variation = variation, year = year)
            additional = ""
            if "Nominal" not in variation:
                additional = " --use-alternative-signal {variation} --use-alternative-mca ttW_multilepton/mca-includes/mca-2lss-EFT.txt".format(variation = variation)
            
            cmd = subprocess.check_output(python_command, shell=True, universal_newlines=True)
            print("{cmd}".format(cmd = cmd.replace("mcc-METchoice-prefiring.txt", "mcc-METchoice-prefiring.txt %s"%additional)))
            print("{RED}-------------------{NC}".format(RED = RED, NC = NC))
