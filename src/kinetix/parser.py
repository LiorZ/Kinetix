import yaml
from .base import *
class KinetixParser:
    def __init__(self, filename: str):
        self.filename = filename
        self.data = None
        self.experiment = None

    def parse_experiment(self):
        with open(self.filename, 'r') as f:
            self.data = yaml.safe_load(f)
        self.reaction_name = self.data['name']
        self.reactants = dict()
        for rname,rvalue in self.data['reactants'].items():
            self.reactants[rname] = Reactant(rname, rvalue)
        self.enzymes = dict()
        for ename,econc in self.data['enzymes'].items():
            self.enzymes[ename] = Enzyme(ename, econc)
            if ename not in self.data['reaction'].keys():
                break
            params = self.data['reaction'][ename]
            reaction_param = ReactionParameters(self.reactants[params['back']],self.reactants[params['fwd']],params['km_fwd'],params['km_back'],params['kcat_fwd'],params['kcat_back'])
            self.enzymes[ename].add_reaction_params(reaction_param)
        self.experiment = Experiment()
        for e in self.enzymes.values():
            self.experiment.add_enzyme(e)
        for r in self.reactants.values():
            self.experiment.add_reactant(r)
        return self.experiment

    def get_experiment():
        return self.experiment





