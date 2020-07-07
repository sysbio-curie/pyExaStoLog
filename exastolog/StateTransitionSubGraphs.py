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

import networkx as nx
import numpy as np
import scipy.sparse as sparse

class StateTransitionSubGraphs:
    
    def __init__(self, A_sparse, x0):
        
        self.subnetws = None
        self.scc_submats = None
        self.nonempty_subgraphs = None
        self.sorted_vertices = None
        self.cyclic_sorted_subgraphs = None
        
        self.fcn_scc_subgraphs(A_sparse, x0)
            
    def fcn_metagraph_scc(self, A_sparse_sub):
        
        matr_size = A_sparse_sub.shape[0]

        g_sub = nx.from_scipy_sparse_matrix(A_sparse_sub, create_using=nx.DiGraph())
        g_sub.remove_edges_from(nx.selfloop_edges(g_sub))
        
        # Here we reverse it only for debugging purpose
        # The order shouldn't matter, but it's nice to have the same as matlab
        scc_list = list(reversed(list(nx.strongly_connected_components(g_sub))))
        print("%d connected components" % len(scc_list))

        
        num_verts_per_scc = []
        scc_memb_per_vert = np.zeros((matr_size, 1))

        for i, scc in enumerate(scc_list):
            num_verts_per_scc.append(len(scc))
            scc_memb_per_vert[list(scc),:] = i
            
        # row, col = np.where((A_sparse_sub - np.diag(A_sparse_sub.diagonal())) > 0)
        # Yet another trick to get the exact same results as matlab
        # The difference is returning the list from parsing via columns or via rows, hopefully nothing critical
        col, row = np.where((A_sparse_sub - np.diag(A_sparse_sub.diagonal())).transpose() > 0)

        diff = scc_memb_per_vert[row] != scc_memb_per_vert[col]
        
        row_sel = row[np.where(diff[:, 0])]
        col_sel = col[np.where(diff[:, 0])]

        A_metagraph = sparse.csr_matrix(
            (np.array(A_sparse_sub[row_sel, col_sel]).flatten(), 
            (scc_memb_per_vert[row_sel][:, 0], scc_memb_per_vert[col_sel][:, 0])),
            shape=(len(num_verts_per_scc), len(num_verts_per_scc))
        )

        metagraph = nx.from_scipy_sparse_matrix(A_metagraph, create_using=nx.DiGraph())
        metagraph_ordering=np.array(list(nx.topological_sort(metagraph)))
        
        terminal_scc_ind, _ = np.where(A_metagraph.sum(axis=1) == 0)
        terminal_scc_pos = np.isin(metagraph_ordering, terminal_scc_ind)
        
        nonterm_scc_num = len(num_verts_per_scc) - len(terminal_scc_ind)

        scc_sup1 = [i for i, scc in enumerate(scc_list) if len(scc) > 1]
        
        term_cycles_ind = set(scc_sup1).intersection(set(terminal_scc_ind))
        where_terminal_scc_pos, = np.where(terminal_scc_pos)

        if np.sum(np.logical_not(where_terminal_scc_pos>(nonterm_scc_num-1))) > 0:
            nonterm_scc_inds = np.logical_not(np.isin(metagraph_ordering, terminal_scc_ind))
            metagraph_ordering_terminal_bottom = np.concatenate([
                metagraph_ordering[nonterm_scc_inds],
                metagraph_ordering[terminal_scc_pos]
            ])

        else:
            metagraph_ordering_terminal_bottom = metagraph_ordering


        if len(term_cycles_ind) > 0:
            
            scc_cell_reordered = [scc_list[i] for i in metagraph_ordering_terminal_bottom]
            # index of cells containing term cycles after reordering
            term_cycles_ind, = np.where(np.isin(metagraph_ordering_terminal_bottom, np.array(list(term_cycles_ind))))

            # we need a cell of the indices of certices withing whese
            scc_cell_reordered_lengths = np.array([len(scc) for scc in scc_cell_reordered])
            scc_cell_reordered_cumsum = np.cumsum(scc_cell_reordered_lengths)
            
            cycle_first_verts = scc_cell_reordered_cumsum[term_cycles_ind] - scc_cell_reordered_lengths[term_cycles_ind];
            cycle_last_verts = scc_cell_reordered_cumsum[term_cycles_ind] - 1
            
            term_cycles_bounds = [np.concatenate([cycle_first_verts, cycle_last_verts])]
            
        else:
            term_cycles_ind = []
            term_cycles_bounds = []
            

        # reordered original vertices
        vert_topol_sort = np.concatenate([list(scc_list[i]) for i in metagraph_ordering_terminal_bottom])
        
        return vert_topol_sort, term_cycles_ind, A_metagraph, scc_list, term_cycles_bounds


    def fcn_scc_subgraphs(self, A_sparse, x0):
        
        print("Indentifying SCCs")
        G = nx.from_scipy_sparse_matrix(A_sparse, create_using=nx.DiGraph())
        G.remove_edges_from(nx.selfloop_edges(G))
        
        # Here we get a generator. Do I really need to compute it now ?
        self.subnetws = [list(g) for g in nx.weakly_connected_components(G)]
        cell_subgraphs = []
        self.scc_submats = []
        self.nonempty_subgraphs = []
        # print(len(self.subnetws))
        print("Identifying SCCs in subgraphs")
        for i, subnet in enumerate(self.subnetws):
            cell_subgraphs.append(subnet)
            
            # Slicing done it two steps : First the rows, which is the most efficient for csr sparse matrix
            # then columns. I should probably dig deeper
            t_sparse = A_sparse[subnet, :][:, subnet]
            
            t_g = nx.from_scipy_sparse_matrix(t_sparse, create_using=nx.DiGraph())
            t_g.remove_edges_from(nx.selfloop_edges(t_g))
            
            # Again, do I really need to compute it ?
            self.scc_submats.append([list(g) for g in nx.strongly_connected_components(t_g)])

            if sum(x0[subnet]) > 0:
                self.nonempty_subgraphs.append(i)
        
        self.sorted_vertices = []
        self.cyclic_sorted_subgraphs = []
        counter = 0
        
        for nonempty_subgraph in self.nonempty_subgraphs:
            
            A_sparse_sub = A_sparse[self.subnetws[nonempty_subgraph], :][:, self.subnetws[nonempty_subgraph]]
        
            if A_sparse_sub.shape[0] == len(self.scc_submats[nonempty_subgraph]):
                t_g = nx.from_scipy_sparse_matrix(A_sparse_sub, create_using=nx.DiGraph())
                t_g.remove_edges_from(nx.selfloop_edges(t_g))
                self.sorted_vertices.append(list(nx.topological_sort(t_g)))
                # print("toposort results")
                # print(list(nx.topological_sort(t_g)))
            else:
                print("Cycles in STG")
                
                # If entire graph is only one connected component, no need for re-ordering
                if len(self.scc_submats[nonempty_subgraph]) == 1:
                    self.sorted_vertices.append(self.scc_submats[nonempty_subgraph])
                else:
                    vert_topol_sort,term_cycles_ind,_,scc_cell,term_cycle_bounds=self.fcn_metagraph_scc(A_sparse_sub)
                    cycle_lengths = [len(scc) for scc in scc_cell]
                    
                    a = np.zeros((max(cycle_lengths)))
                    for i in range(max(cycle_lengths)):
                        for j in cycle_lengths:
                            if j == i+1:
                                a[j-1] += 1
                        
                    print('Cycles of lenth: %s (%s times)' % (set(cycle_lengths), a[np.where(a>0)]) )
                    self.cyclic_sorted_subgraphs.append((vert_topol_sort, term_cycles_ind, term_cycle_bounds))

            counter += 1
                