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
class Solution:
    
    def __init__(self, A_sparse, subgraphs, transitionRatesTable, x0):

        self.stat_sol = None
        self.term_verts_cell = None
        self.cell_subgraphs= None
        self.split_calc_inverse(A_sparse, subgraphs, transitionRatesTable, x0)
    
    
    def fcn_block_inversion(self, K_sp_sub_reord, sorted_vertices_terminal_bottom, x0, submatrix_inds):
        """
            This function calculate kernels and stationary solution if all terminal
        """
        
        
        # Construct kernels from matrix blocks
        dim_kernel = sum(K_sp_sub_reord.diagonal() == 0)
        dim_matr = K_sp_sub_reord.shape[0]
        
        colnum_r_null_array = range(dim_kernel)
        term_block_inds = range(dim_matr - dim_kernel, dim_matr)
        nonterm_block_inds = range(dim_matr - dim_kernel)
        term_block = sparse.eye(dim_kernel)
    
        # Right kernel
        r0_blocks = sparse.lil_matrix((dim_matr, dim_kernel), dtype=np.float32)
        r0_blocks[np.ix_(term_block_inds, colnum_r_null_array)] = term_block    
        
        # Left kernel
        l0_blocks = sparse.lil_matrix((r0_blocks.shape[0], r0_blocks.shape[1]), dtype=np.float32).transpose()
        nonzeros = r0_blocks.nonzero()
        l0_blocks[(nonzeros[1], nonzeros[0])] = 1
        
        X_block = (
            -r0_blocks[np.ix_(term_block_inds, colnum_r_null_array)]
            *K_sp_sub_reord[np.ix_(term_block_inds, nonterm_block_inds)]
        )
        
        # Solution 6
        # https://stackoverflow.com/questions/1007442/mrdivide-function-in-matlab-what-is-it-doing-and-how-can-i-do-it-in-python
        #TL;DR: A/B = np.linalg.solve(B.conj().T, A.conj().T).conj().T
        # import time
        # import scipy
        # Here we have 3 solutions : scipy sparse, scipy dense, numpy
        # And numpy is faster on the kras example
        # Using sparse solve
        
        # t0 = time.time()
        # X_block = sparse.linalg.spsolve(
        #     K_sp_sub_reord[np.ix_(nonterm_block_inds,nonterm_block_inds)].tocsr().conj().transpose(),
        #     X_block.conj().transpose()
        # ).conj().transpose()
        
        # Using scipy solve
        # t1 = time.time()
        # X_block = scipy.linalg.solve(
        #     K_sp_sub_reord[np.ix_(nonterm_block_inds,nonterm_block_inds)].todense().conj().transpose(),
        #     X_block.todense().conj().transpose()
        # ).conj().transpose()
        
        # Using numpy's solve
        # t2 = time.time()
        X_block = np.linalg.solve(
            K_sp_sub_reord[np.ix_(nonterm_block_inds,nonterm_block_inds)].toarray().conj().transpose(),
            X_block.toarray().conj().transpose()
        ).conj().transpose()
        # print("1 : %.2gs, 2 : %.2gs, 3 : %.2gs" % (t1-t0, t2-t1, time.time()-t2))
        
        l0_blocks[np.ix_(colnum_r_null_array, nonterm_block_inds)] = X_block;

        stat_sol_submatr_blocks = r0_blocks * l0_blocks * x0[submatrix_inds[sorted_vertices_terminal_bottom]]
        
        return stat_sol_submatr_blocks

    def fcn_adjug_matrix(self, A, col_arg):
        
        size_array = np.array(list(range(A.shape[0])))
        size_vect = len(size_array)
        adj_matrix = None
        if A.shape[0] == A.shape[1]:

            if len(col_arg) == 0:
                print("NOT IMPLEMENTED")

                #if a is a double

                #else if a is symbolic

                #end

                #for k in range(size_vect):
                #    for l in range(size_vect):
                #        adj_matrix = truc

                #if a is symbolic, we simplify

                pass

            else:
                import scipy
                
    #             adj_matrix
                adj_matrix = []
                for k in size_array:
                    adj_matrix.append(
                        pow(-1, k)*
                        scipy.linalg.det(
                            A[np.ix_(
                                range(1,size_vect), 
                                size_array[np.where(size_array != k)[0]]
                            )].todense()
                        )
                    )

        else: #non square matrix
            adj_matrix = []
            print("non-square matrix")
            
        
        return adj_matrix

    def fcn_left_kernel(self, K_sp_sub_reord, r0_blocks, dim_matr):
        
        print("Constructing left kernel")

        if len(r0_blocks.shape) > 1:
            dim_kernel = np.sum(np.logical_not(np.isin(np.sum(r0_blocks, axis=1), 0)))
            colnum_r_null_array = range(r0_blocks.shape[1])
            size_r0_blocks = r0_blocks.shape
        else:
            print("Here we have a problem, the r0_blocks is actually 1D. Trying... RESULTS NEED TO BE CHECKED !!!")
        
    #         dim_kernel = np.sum(np.logical_not(np.isin(r0_blocks, 0)))
    #         colnum_r_null_array = [0]
    #         size_r0_blocks = [r0_blocks.shape[0], 1]

        term_block_inds = range(dim_matr -dim_kernel,dim_matr)
        nonterm_block_inds = range(dim_matr-dim_kernel)
        
        l0_blocks = sparse.lil_matrix((size_r0_blocks[0], size_r0_blocks[1])).transpose()
        t_inds = np.where(np.logical_not(np.isin(r0_blocks, 0)).transpose())
        
        l0_blocks[t_inds] = 1
        
        X_block = (
            -l0_blocks[np.ix_(colnum_r_null_array,term_block_inds)]
            *K_sp_sub_reord[np.ix_(term_block_inds, nonterm_block_inds)]
        )
        
        # Using numpy's solve
        X_block = np.linalg.solve(
            K_sp_sub_reord[np.ix_(nonterm_block_inds,nonterm_block_inds)].toarray().conj().transpose(),
            X_block.toarray().conj().transpose()
        ).conj().transpose()
        
        l0_blocks[np.ix_(colnum_r_null_array, nonterm_block_inds)] = X_block
        
        return l0_blocks

    def split_calc_inverse(self, A_sparse, subgraphs, transition_rates_table, x0):
        
        # is the STG disconnected?
        self.stat_sol=sparse.lil_matrix((x0.shape[0], 1))
        # A_digraph=digraph(A_sparse,'omitselfloops'); 
        num_subnets = len(subgraphs.subnetws)
        # preallocate cell of term vertices and of subgraphs
        self.term_verts = []
        self.cell_subgraphs = []

        if num_subnets>1:
            print('STG has multiple subgraphs')

        counter_subgraphs=0
        
        for i in subgraphs.nonempty_subgraphs:
            
            submatrix_inds = np.array(subgraphs.subnetws[i])
            self.cell_subgraphs.append(submatrix_inds)

            if num_subnets > 1:
                print("Calculating subgraph #%d of %d" % (i+1, num_subnets))
                
            A_sparse_sub = A_sparse[subgraphs.subnetws[i], :][:, subgraphs.subnetws[i]]
            dim_matr = A_sparse_sub.shape[0]
            scc_submat = subgraphs.scc_submats[i]
            
            # IF all SCCs are single vertices (ie. no cycles)
            if len(set([tuple(t_submat) for t_submat in scc_submat])) == dim_matr:
                
                # function to reorder vertices and keep ordering
                terminal_nodes = np.where(A_sparse_sub.diagonal() == 1)
    #             print(terminal_nodes)
                # this is a consistent ordering but terminals are not necessarily in lower right corner of matrix
                A_orig_reordered = A_sparse_sub[subgraphs.sorted_vertices[counter_subgraphs], :][:, subgraphs.sorted_vertices[counter_subgraphs]]

                
                # but we want to have terminal states acolnum_r_null_arrayt the bottom
                #print(sorted_vertices[counter_subgraphs])
                # This weird assignment syntax is because it returns a tuple of length one. This is valid, and it works
                terminal_indices, = np.where(np.isin(subgraphs.sorted_vertices[counter_subgraphs], terminal_nodes))
                terminal_rem_inds, = np.where(np.logical_not(np.isin(subgraphs.sorted_vertices[counter_subgraphs], terminal_nodes)))
                t_inds, = np.where(np.logical_not(np.isin(subgraphs.sorted_vertices[counter_subgraphs], terminal_nodes)))
                
                array_sorted_vertices = np.array(subgraphs.sorted_vertices[counter_subgraphs])

                sorted_vertices_terminal_bottom = (
                    list(array_sorted_vertices[t_inds]) + list(array_sorted_vertices[terminal_indices])
    #                 axis=1
                )
                    
                reordered_terminal_inds = list(terminal_rem_inds) + list(terminal_indices)
                
                A_sparse_sub_reordered_terminal = A_orig_reordered[reordered_terminal_inds, :][:, reordered_terminal_inds]
                
                K_sp_sub_reord = (A_sparse_sub_reordered_terminal.transpose() - sparse.eye(dim_matr)) * sum(transition_rates_table.flatten())

                stat_sol_submatr_blocks = self.fcn_block_inversion(K_sp_sub_reord, sorted_vertices_terminal_bottom, x0, submatrix_inds)

                self.stat_sol[submatrix_inds[sorted_vertices_terminal_bottom]] = stat_sol_submatr_blocks
                self.term_verts.append(set(self.stat_sol.nonzero()[0]).intersection(set(submatrix_inds)))
                
            else:
            
                print('cycles in STG')
                if len(scc_submat) == 1:
    #             % if entire graph is one connected component, no reordering needed
                    K_sp_sub_reord = (A_sparse_sub.transpose() - sparse.eye(dim_matr, dim_matr)) * sum(transition_rates_table.flatten())
                    kernel_col = np.dot(pow(-1, (dim_matr-1)), self.fcn_adjug_matrix(K_sp_sub_reord, 'col'))
                    # normalization
                    r0_blocks = (kernel_col.transpose()/np.sum(kernel_col))
                    if len(r0_blocks.shape) == 1:
                        r0_blocks = r0_blocks.reshape(r0_blocks.shape[0], 1)
                        
                    l0_blocks = self.fcn_left_kernel(K_sp_sub_reord, r0_blocks, dim_matr)
                    
                    #stat sol
                    stat_sol_submatr_blocks = np.dot(r0_blocks*l0_blocks,x0[submatrix_inds])
                    
                    self.stat_sol[submatrix_inds] = stat_sol_submatr_blocks
                    self.term_verts.append(submatrix_inds)
                    
                    

                else:
                    print("Not a unique connected component")
                
                    vert_topol_sort = subgraphs.cyclic_sorted_subgraphs[counter_subgraphs][0]
                    term_cycles_ind = subgraphs.cyclic_sorted_subgraphs[counter_subgraphs][1]
                    term_cycle_bounds = subgraphs.cyclic_sorted_subgraphs[counter_subgraphs][2]
                
                    A_sparse_sub_reordered_terminal = A_sparse_sub[vert_topol_sort,:][:, vert_topol_sort]
                    K_sp_sub_reord = (A_sparse_sub_reordered_terminal.transpose() - sparse.eye(dim_matr, dim_matr))*sum(transition_rates_table.flatten())


                    # if cycles are non-terminal, stat sol can be calculated by block inversion, sames as for acyclic graphs
                    if len(term_cycles_ind) == 0:
                        print("Empty term cycles ind")
                        print(" NEEDS TO BE TESTED")
    #                      % here make sure if 'vert_topol_sort' is the right ordering...
                        stat_sol_submatr_blocks = self.fcn_block_inversion(K_sp_sub_reord, vert_topol_sort, x0, submatrix_inds)
                        self.stat_sol[submatrix_inds[vert_topol_sort]] = stat_sol_submatr_blocks
                        self.term_verts_cell.append(submatrix_inds[vert_topol_sort[np.where(K_sp_sub_reord.diagonal() == 0)]])

                    else:
                        print("Non empty term cycles ind")
                        
                        # if there are terminal cycles, stat sol calc a bit more complicated
                        # need to identify terminal cycles, for corresponding columns of
                        # kernel we'll need to calculate adjugate matrix

                        # probably we don't want it in symbolic form, but just in case
                        if K_sp_sub_reord.dtype == np.float64:
                            r_null_cycles = sparse.lil_matrix((dim_matr, len(term_cycle_bounds)))
                        
                        else:
                            print("NOT IMPLEMENTED")
                            return

                        for k, term_cycle_bound in enumerate(term_cycle_bounds):
                            cycle_inds = range(term_cycle_bound[0], term_cycle_bound[-1]+1)
                    
                            #calc kernel of scc
                            scc_cycle = K_sp_sub_reord[cycle_inds, :][:, cycle_inds]
                            # adjugate_matrix -> kernel
                            n = len(cycle_inds)
                            
                            kernel_col = np.dot(pow(-1, n-1) , self.fcn_adjug_matrix(scc_cycle, 'col'))
                            
                            r_null_cycles[cycle_inds,k] = kernel_col/sum(kernel_col)
                            
                        # if there are single-vertex terminal states too
                        if np.sum(np.isin(K_sp_sub_reord.diagonal(), 0)) > 0:
                            
                            print("single vertex terminal states")
                            print(" NOT IMPLEMENTED")
    #                          n_terminal=find(ismember(diag(K_sp_sub_reord),0))'; 
    #                         r_null_single_vert = sparse(dim_matr,numel(n_terminal)); 
    #                         % (1:numel(n_terminal)-1)*2 + n_terminal
    #                         r_null_single_vert( sub2ind(size(r_null_single_vert), n_terminal, 1:numel(n_terminal)) )=1;
    #                         % does the order of columns in the kernel matter? I think not, if l0_blocks consistent w r0_blocks
    #                         r0_blocks=[r_null_cycles r_null_single_vert];
                            return
                        else:
                            print("no single vertex terminal states")
                            r0_blocks = r_null_cycles
                            
                        # calculate kernel
                        l0_blocks = self.fcn_left_kernel(K_sp_sub_reord, r0_blocks, dim_matr)
                        
                        # stat sol
                        stat_sol_submatr_blocks = r0_blocks*l0_blocks*x0[submatrix_inds[vert_topol_sort]]
                        self.stat_sol[submatrix_inds[vert_topol_sort]] = stat_sol_submatr_blocks
                        row, col = r0_blocks.nonzero()
                        
                        pre_term_verts = []
                        
                        for k in range(len(set(col))):
                            pre_term_verts.append(
                                submatrix_inds[vert_topol_sort[row[np.where(col == k)]]]
                            )
                        self.term_verts.append(pre_term_verts)

            counter_subgraphs +=1

