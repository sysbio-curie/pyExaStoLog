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

from .InitialState import InitialState
from .StateTransitionSubGraphs import StateTransitionSubGraphs
from .Solution import Solution
import numpy as np
import pandas as pd

class Simulation:
    
    def __init__(self, model, initial_fixed_nodes, initial_fixed_nodes_vals):
        self.model = model
        self.initial_state = InitialState(initial_fixed_nodes, initial_fixed_nodes_vals, model.nodes)
        self.stateTransitionSubGraphs = StateTransitionSubGraphs(model.stateTransitionGraph.A_sparse, self.initial_state.x0)
        self.solution = Solution(model.stateTransitionGraph.A_sparse, self.stateTransitionSubGraphs, model.transitionRatesTable, self.initial_state.x0)
        self.last_states_probtraj = None
        
    def get_last_states_probtraj(self):
        
        
        probs = np.zeros((len(self.solution.stat_sol.nonzero()[0])))
        states = []
        
        for i, stateval in enumerate(self.solution.stat_sol.nonzero()[0]):
     
            binstate = np.zeros((len(self.model.nodes)))
            c = len(self.model.nodes)-1
            t_stateval = stateval
        
            while t_stateval > 0:
                binstate[c] = t_stateval % 2
                t_stateval = t_stateval // 2
                c -= 1
            
            inds_states, = np.where(np.flip(binstate))
        
            if len(inds_states) > 0:
                t_state = [self.model.nodes[ind] for ind in inds_states]
                states.append(" -- ".join(t_state))
            
            else:
                states.append("<nil>")
            
            probs[i] = self.solution.stat_sol[stateval, 0]
        
        self.last_states_probtraj = pd.DataFrame([probs], columns=states)
        self.last_states_probtraj.sort_index(axis=1, inplace=True)
        
        return self.last_states_probtraj
