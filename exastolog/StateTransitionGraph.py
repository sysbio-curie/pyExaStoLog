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

