from .InitialState import InitialState
from .StateTransitionSubGraphs import StateTransitionSubGraphs
from .Solution import Solution

class Simulation:
    
    def __init__(self, model, initial_fixed_nodes, initial_fixed_nodes_vals):
        self.initial_state = InitialState(initial_fixed_nodes, initial_fixed_nodes_vals, model.nodes)
        self.stateTransitionSubGraphs = StateTransitionSubGraphs(model.stateTransitionGraph.A_sparse, self.initial_state.x0)
        self.solution = Solution(model.stateTransitionGraph.A_sparse, self.stateTransitionSubGraphs, model.transitionRatesTable, self.initial_state.x0)