import matplotlib
matplotlib.use('Qt4Agg')

import matplotlib.pyplot as plt 
import numpy as np 
from differential_variables import all_vars


for what in "dR_ll,HT,mindr_lep1_jet25,dR_lbloose".split(","):
    gen=np.array(eval(all_vars[what].CATBINS))
    reco=np.array(eval(all_vars[what].CATBINS_Gen))

    plt.plot( reco,np.zeros_like(reco),'.',  label='Reco')
    plt.plot( gen, 0.05*np.ones_like(gen),'.', label='Gen')
    ax = plt.gca()
    ax.set_ylim([-0.2, 0.5])
    plt.savefig('check_%s.png'%what)
    plt.legend()
    plt.clf()



