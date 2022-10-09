import networkx as nx
import itertools as it
class ReactionParameters:
  def __init__(self,substrate,product,km_fwd,km_back,kcat_fwd,kcat_back):
    self.substrate = substrate
    self.product = product
    self.km_fwd = km_fwd
    self.km_back = km_back
    self.kcat_fwd = kcat_fwd
    self.kcat_back = kcat_back

class Enzyme:

  def __init__(self,name,amount):
    self.name = name
    self.amount = amount
    self.reactions = dict()
  
  def add_reaction_params(self,r):
    self.reactions[r.substrate.name+"."+r.product.name] = r
  
class Reactant:
  def __init__(self,name,amount):
    self.name = name
    self.amount = amount

  def __str__(self):
    return self.name

class Experiment:

  def __init__(self):
    self.enzymes = dict()
    self.reactants = dict()


  def add_enzyme(self,enzyme):
    self.enzymes[enzyme.name] = enzyme
  
  def add_reactant(self,reactant):
    self.reactants[reactant.name] = reactant
  
  def _build_reaction_graph(self):
    reaction_graph = nx.DiGraph()
    for k in self.reactants.keys():
      reaction_graph.add_node(self.reactants[k])
    for k,e in self.enzymes.items():
      for name,rt in e.reactions.items():
        reaction_graph.add_edge(rt.substrate,rt.product,enzyme=e)
    return reaction_graph

  # def reversible_mm(self,Vf_max,S,Km_forward,Vb_max,P,Km_back):
  def reversible_mm(self,enzyme,substrate,product,params):
    Km_forward = params.km_fwd
    Km_back = params.km_back
    Vf_max = params.kcat_fwd * enzyme.amount
    Vb_max = params.kcat_back * enzyme.amount
    S = substrate.amount
    P = product.amount

    nom = (Vf_max * S / Km_forward ) - Vb_max * P / Km_back
    denom = 1 + S/Km_forward + P/Km_forward
    return nom/denom

  def iteration(self,reaction_graph,source,dt):
      for rsource, rtarget in it.product(reaction_graph.nodes,reaction_graph.nodes):
        if (rsource.amount == 0 and rtarget.amount == 0) or (rsource == rtarget):
          continue
        if reaction_graph.has_edge(rsource,rtarget):
          enzyme = reaction_graph[rsource][rtarget]['enzyme']
          r_params = enzyme.reactions[rsource.name+'.'+rtarget.name]
          v = self.reversible_mm(enzyme,rsource,rtarget,r_params)
          
          #update the amounts:
          rsource.amount -= max(v*dt,0)
          rtarget.amount += max(v*dt,0)

  def run(self,steps,dt=0.1):
    reaction_graph = self._build_reaction_graph()
    reactants = sorted(list(self.reactants.values()),key=lambda x: -x.amount)
    source = reactants[0]
    results = []
    for i in range(steps):
      self.iteration(reaction_graph,source,dt)
      record = {'step':i}
      for name,obj in self.reactants.items():
        record[name] = obj.amount
      results.append(record)
    return results
