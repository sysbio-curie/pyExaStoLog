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


class TransRateTable:
    
    def __init__(self, nodes, uniform_or_rand, meanval, sd_val, chosen_rates, chosen_rates_vals):
        self.table = self.fcn_trans_rates_table(nodes, uniform_or_rand, meanval, sd_val, chosen_rates, chosen_rates_vals)
        
        
    def fcn_trans_rates_table(self, nodes, uniform_or_rand, meanval, sd_val, chosen_rates, chosen_rates_vals):
        n = len(nodes)

        if uniform_or_rand == "uniform":
            rate_vals_num = np.ones((1, 2*n)).astype(np.int64)

        elif uniform_or_rand == "random":
            rate_vals_num = np.random.normal(meanval, sd_val, (1, 2*n))
            if np.any(rate_vals_num < 0):
                neg_cnt = 0
                while np.any(rate_vals_num < 0):
                    rate_vals_num = np.random.normal(meanval, sd_val, (1, 2*n))
                    neg_cnt += 1
                    if neg_cnt > 100:
                        break
                        
        else:
            print("Choose 'uniform' or 'random' to generate transition rates", file=sys.stderr)
            return

        for k, chosen_rate in enumerate(chosen_rates):
            split_rate = chosen_rate.split("_")
            if len(split_rate) > 2:
                node_mod_ind = "_".join(split_rate[1:])
            else:
                node_mod_ind = split_rate[1]

            if split_rate[0] == "d":
                rate_vals_num[:, nodes.index(node_mod_ind)+n] = chosen_rates_vals[k]
            elif split_rate[0] == "u":
                rate_vals_num[:, nodes.index(node_mod_ind)] = chosen_rates_vals[k]
            else:
                print("Wrong name for transition rate, has to be 'u_nodename' or 'd_nodename'", file=sys.stderr)
                return
        
        return np.reshape(rate_vals_num, (n, 2)).transpose()
