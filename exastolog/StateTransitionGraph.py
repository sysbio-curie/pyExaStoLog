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

class StateTransitionGraph:
    
    def __init__(self, state_transition_table, transition_rates_table, kin_matr_flag="yes"):
        self.A_sparse = None
        self.K_sparse = None
        self.fcn_build_trans_matr(state_transition_table, transition_rates_table, kin_matr_flag)
        
    def fcn_build_trans_matr(self,stg_table, transition_rates_table, kin_matr_flag):

        dim_matr = pow(2, transition_rates_table.shape[1])
        
        rate_inds = ((stg_table[:, 2])*2)+stg_table[:, 3]

        # Here we reshape the transition_rates_table to a list
        reshaped_trt = np.reshape(transition_rates_table, (1, np.product(transition_rates_table.shape)), order="F")[0, :]

        B = sparse.csr_matrix(
            (
                reshaped_trt[rate_inds]/np.sum(transition_rates_table),
                (stg_table[:, 0], 
                stg_table[:, 1])
            ),
            shape=(dim_matr, dim_matr)
        )

        self.A_sparse = B + (sparse.eye(B.shape[0]) - sparse.diags(np.array(sparse.csr_matrix.sum(B, axis=1).transpose())[0]))

        if len(kin_matr_flag) > 0:
            self.K_sparse = (self.A_sparse.transpose() - sparse.eye(self.A_sparse.shape[0]))*np.sum(transition_rates_table)

        else:
            self.K_sparse = []

