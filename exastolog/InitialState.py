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

import numpy as np
import scipy.sparse as sparse

class InitialState:
    
    def __init__(self, initial_fixed_nodes, initial_fixed_nodes_vals, nodes, dom_prob=1, distrib_type="uniform"):
        
        self.x0 = self.fcn_define_initial_states(
            initial_fixed_nodes, initial_fixed_nodes_vals, dom_prob, nodes, distrib_type
        )
        
    def fcn_define_initial_states(self, initial_fixed_nodes,initial_fixed_nodes_vals,dom_prob,nodes,distrib_type):
                
        n_nodes = len(nodes)
        
        truth_table_inputs = np.remainder(
            np.floor(
                np.multiply(
                    np.array([range(pow(2, n_nodes))]).transpose(), 
                    np.array([np.power([2.0]*n_nodes, np.array(range(0, -n_nodes, -1)))])
                )
            ), 2
        ).astype(bool)
        
        # define initial values
        x0 = np.zeros((int(pow(2, n_nodes)), 1))
        
        # defining a dominant initial state (eg. dom_prob=0.8, ie. 80% probability
        initial_on_nodes_inds = [node in initial_fixed_nodes for node in nodes]                                  

        statespace_decim = np.sum(
            truth_table_inputs[:, initial_on_nodes_inds]*np.power(
                2, 
                np.array(
                    list(reversed(range(np.sum(initial_on_nodes_inds))))
                )
            ), axis=1
        )

        initial_fixed_nodes_vals_decim = np.sum(
            initial_fixed_nodes_vals*np.power(
                2, 
                np.array(
                    list(reversed(range(len(initial_fixed_nodes_vals))))
                )
            )
        )

        inds_condition = np.isin(statespace_decim, initial_fixed_nodes_vals_decim)

        if distrib_type == "uniform":
            x0[inds_condition] = np.array([[dom_prob/sum(inds_condition)]*sum(inds_condition)]).transpose()
            x0[np.logical_not(inds_condition)] = np.array([[(1-dom_prob)/(len(x0)-sum(inds_condition))]*(len(x0)-sum(inds_condition))]).transpose()
        
        elif distrib_type == "random":
            x0[inds_condition] = np.random.uniform(0, 1, (sum(inds_condition), 1))
            x0 = dom_prob*x0/sum(x0)

            x0[np.logical_not(inds_condition)] = np.random.uniform(0, 1, (len(x0)-sum(inds_condition), 1))
            x0[np.logical_not(inds_condition)] = (1-dom_prob)*x0[np.logical_not(inds_condition)]/sum(x0[np.logical_not(inds_condition)])
        
        else:
            print("distrib type should be 'uniform' or 'random'", file=sys.stderr)
        
        # rounding precision
        n_prec=3

        if round(sum(x0)[0],n_prec) == 1:
            print('sum(x0)=1, OK.')
        
        else:
            print('sum(x0)~=1, something wrong!')

    #     if ~isempty(plot_flag)
    #     bar(x0); set(gca,'yscale','log'); xlim([1 2^n_nodes]); % ylim([(1-dom_prob)/2^n_nodes 1])
    #     % subplot(2,1,2); x0=fcn_define_initial_states(initial_on_nodes,dom_prob,nodes,'broad'); 
    #     % bar(x0); xlim([1 2^13]);set(gca,'yscale','log'); ylim([(1-dom_prob)/2^n_nodes 1])
    #     end

        return x0