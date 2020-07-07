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
import boolean

class StateTransitionTable:
    
    
    def __init__(self, model, nodes):
        
        self.model = model
        self.nodes = nodes
        self.n = len(nodes)
        
        self.stg_table = self.fcn_build_stg_table()
    
    def fcn_gen_node_update(self, formula, list_binary_states):

        if isinstance(formula, boolean.boolean.Symbol):
            return list_binary_states[:, self.nodes.index(str(formula))]
        
        elif isinstance(formula, boolean.boolean.NOT):
            return np.logical_not(
                self.fcn_gen_node_update(formula.args[0], list_binary_states)
            )
        
        elif isinstance(formula, boolean.boolean.OR):
            ret = self.fcn_gen_node_update(formula.args[0], list_binary_states)
            for i in range(1, len(formula.args)):
                ret = np.logical_or(ret, 
                    self.fcn_gen_node_update(formula.args[i], list_binary_states)
                )
            return ret
        
        elif isinstance(formula, boolean.boolean.AND):
            ret = self.fcn_gen_node_update(formula.args[0], list_binary_states)
            for i in range(1, len(formula.args)):
                ret = np.logical_and(ret, 
                    self.fcn_gen_node_update(formula.args[i], list_binary_states)
                )
            return ret
        
        else:
            print("Unknown boolean operator : %s" % type(formula))
        
        
    def fcn_build_update_table(self, list_binary_states):
        update_matrix = np.array(
            [
                self.fcn_gen_node_update(self.model[node], list_binary_states) 
                for node in self.nodes
            ]
        ).transpose()
        
        return update_matrix
        
    def fcn_states_inds(self, yes_no, n_isl_exp):
    
        n_series_exp = self.n - 1
        yes_no = yes_no - 1
        
        f_mat = np.array(
            range(
                1, 
                pow(2, (self.n-n_isl_exp))+1
            )
        ) + yes_no

        t_repmat = np.array([f_mat]*int(pow(2, n_isl_exp)))
            
        t_reshaped = np.reshape(t_repmat, (1, int(pow(2, self.n))), order='F')
        
        t_mult = t_reshaped*pow(2, n_isl_exp)
        t_last = np.array(
            range(
                1, 
                pow(2, self.n)+1
            )
        )
        
        return np.sum([t_last, t_mult])-1
        
    def fcn_build_stg_table(self):
        list_binary_states = np.remainder(
            np.floor(
                np.multiply(
                    np.array([range(pow(2, self.n))]).transpose(), 
                    np.array([np.power([2.0]*self.n, np.array(range(0, -self.n, -1)))])
                )
            ), 2
        ).astype(bool)
        
        update_table = self.fcn_build_update_table(list_binary_states)
        
        up_trans_source = [
            np.intersect1d(
                np.nonzero(update_table[:, x])[0],
                self.fcn_states_inds(0, x)[0, :]
            ) 
            for x in range(self.n)
        ]
            
        down_trans_source = [
            np.intersect1d(
                np.nonzero(np.logical_not(update_table[:, x]))[0],
                self.fcn_states_inds(1, x)[0, :]
            ) 
            for x in range(self.n)
        ]
        
        down_trans_target = [
            np.concatenate(
                (
                    np.array([down_trans_source[x]-pow(2, x)]).transpose(), 
                    np.repeat(np.array([[x,1]]), len(down_trans_source[x]), axis=0)
                ), axis=1
            )
            for x in range(len(down_trans_source))
        ]
        
        up_trans_target = [
            np.concatenate(
                (
                    np.array([up_trans_source[x]+pow(2, x)]).transpose(), 
                    np.repeat(np.array([[x,0]]), len(up_trans_source[x]), axis=0)
                ), axis=1
            )
            for x in range(len(up_trans_source))
        ]
        
        source = np.concatenate([
            np.concatenate(down_trans_source, axis=0),
            np.concatenate(up_trans_source, axis=0)
        ])

        target = np.concatenate([
            np.concatenate(down_trans_target, axis=0),
            np.concatenate(up_trans_target, axis=0)
        ])
        
        stg_table = np.concatenate((np.array([source]).transpose(), target), axis=1)
        
        return stg_table