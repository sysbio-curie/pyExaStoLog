# BSD 3-Clause License

# Copyright (c) 2020, Institut Curie
# All rights reserved.

# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:

# 1. Redistributions of source code must retain the above copyright notice, this
#    list of conditions and the following disclaimer.

# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.

# 3. Neither the name of the copyright holder nor the names of its
#    contributors may be used to endorse or promote products derived from
#    this software without specific prior written permission.

# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

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