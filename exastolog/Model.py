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

import boolean, time

from .TransRateTable import TransRateTable
from .StateTransitionTable import StateTransitionTable
from .StateTransitionGraph import StateTransitionGraph

class Model:
    
    def __init__(self, bnet_filename, profiling=False):
        self.model = None
        self.nodes = None
        self.profiling = profiling
        self.stateTransitionTable = None
        self.transitionRatesTable = None
        self.stateTransitionGraph = None
        
        self.readBNet(bnet_filename)
        self.nodes = list(self.model.keys())
        
        trans_table = self.buildStateTransitionTable()
        self.buildTransitionRateTable()        
        self.buildStateTransitionGraph(trans_table)
        
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
        if self.profiling:
            t0 = time.time()
        stateTransitionTable = StateTransitionTable(self.model, self.nodes)
        if self.profiling:
            print("Size of state transition table : %s" % stateTransitionTable.memsize())
            print("Computed in %.2gs" % (time.time()-t0))
        return stateTransitionTable

    def buildTransitionRateTable(self, distr_type='uniform', meanval=1, sd_val=0, chosen_rates=[], chosen_rates_vals=[]):
        if self.profiling:
            t0 = time.time()
        self.transitionRatesTable = TransRateTable(
            self.nodes, distr_type, meanval, sd_val, chosen_rates, chosen_rates_vals
        )
        if self.profiling:
            # print(self.transitionRatesTable)
            print("Size of transition rates table : %s" % self.transitionRatesTable.memsize())
            print("Computed in %.2gs" % (time.time()-t0))


    def buildStateTransitionGraph(self, trans_table, kin_matr_flag=False):
        if self.profiling:
            t0 = time.time()
        self.stateTransitionGraph = StateTransitionGraph(trans_table.stg_table, self.transitionRatesTable.table, kin_matr_flag)
        if self.profiling:
            print("Size of state transition graph : %s" % self.stateTransitionGraph.memsize())
            print("Computed in %.2gs" % (time.time()-t0))
