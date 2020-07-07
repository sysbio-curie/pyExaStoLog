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
