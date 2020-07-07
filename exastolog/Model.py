import boolean

from .TransRateTable import TransRateTable
from .StateTransitionTable import StateTransitionTable
from .StateTransitionGraph import StateTransitionGraph

class Model:
    
    def __init__(self, bnet_filename):
        self.model = None
        self.nodes = None
        self.stateTransitionTable = None
        self.transitionRatesTable = None
        self.stateTransitionGraph = None
        
        self.readBNet(bnet_filename)
        self.nodes = list(self.model.keys())
        
        self.buildStateTransitionTable()
        self.buildTransitionRateTable()        
        self.buildStateTransitionGraph()
        
    def readBNet(self, filename):
        self.model = {}
        algebra = boolean.BooleanAlgebra()
        with open(filename, 'r') as f:
            lines = f.readlines()
            for line in lines:
                species, formula = [value.strip() for value in line.split(",")]
                if species != "target" and formula != "factors":
                    b_formula = algebra.parse(formula).simplify()
                    self.model.update({species:b_formula})
        
    def buildStateTransitionTable(self):
        self.stateTransitionTable = StateTransitionTable(self.model, self.nodes).stg_table

    def buildTransitionRateTable(self, distr_type='uniform', meanval=1, sd_val=0, chosen_rates=[], chosen_rates_vals=[]):
        self.transitionRatesTable = TransRateTable(
            self.nodes, distr_type, meanval, sd_val, chosen_rates, chosen_rates_vals
        ).table

    def buildStateTransitionGraph(self, kin_matr_flag='yes'):
        self.stateTransitionGraph = StateTransitionGraph(self.stateTransitionTable, self.transitionRatesTable, kin_matr_flag)