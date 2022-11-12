#!/usr/bin/env python

import sys
from kinetix.base import *
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
r_fructose = Reactant('Fructose',2000) #2M
r_NAD = Reactant('NAD',0.5) #0.5mM 
r_NADH = Reactant('NADH',0)  
r_co2 = Reactant('Co2',0)
r_formate = Reactant('foramte',2000) #2M
r_mannitol = Reactant('mannitol',0)

p_fru_man = ReactionParameters(r_fructose,r_mannitol,0.24,21,61,15.9) #substrate,product,km_fwd,km_back,kcat_fwd,kcat_back)
p_NAD_NADH_MDH = ReactionParameters(r_NAD,r_NADH,0.775,0.067,15.9,61)
p_co2_formate = ReactionParameters(r_co2,r_formate,0.43,7.2,0.03,0.3)
p_NAD_NADH_formate_dehydro = ReactionParameters(r_NAD,r_NADH,1.2,0.18,0.3,0.03)

e1 = Enzyme('MDA',0.05)
e1.add_reaction_params(p_fru_man)
e1.add_reaction_params(p_NAD_NADH_MDH)

e2 = Enzyme('Formate dehydrogenase',0.05)
e2.add_reaction_params(p_co2_formate)
e2.add_reaction_params(p_NAD_NADH_formate_dehydro)

reaction = Experiment()
reaction.add_enzyme(e1)
reaction.add_enzyme(e2)

reaction.add_reactant(r_fructose)
reaction.add_reactant(r_NAD)
reaction.add_reactant(r_NADH)
reaction.add_reactant(r_co2)
reaction.add_reactant(r_formate)
reaction.add_reactant(r_mannitol)

result = reaction.run(100000,dt=0.1)

df = pd.DataFrame(result)

sns.lineplot(data=df.melt(id_vars='step'),y='value',x='step',hue='variable')
plt.savefig('test.png')
