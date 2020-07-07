from unittest import TestCase
from ..Model import Model
from ..Simulation import Simulation
from os.path import dirname, join

class TestToy2(TestCase):
    
    def test_toy2(self):
        
        model = Model(join(dirname(__file__), "../../notebooks/model_files/toy2.bnet"))
        simulation = Simulation(model, ['A', 'B', 'C'], [0, 0, 0])
        
        self.assertAlmostEqual(simulation.solution.stat_sol[0, 0], 0.1666667)
        self.assertAlmostEqual(simulation.solution.stat_sol[1, 0], 0.1666667)
        self.assertAlmostEqual(simulation.solution.stat_sol[2, 0], 0.1666667)
        self.assertAlmostEqual(simulation.solution.stat_sol[3, 0], 0.0)
        self.assertAlmostEqual(simulation.solution.stat_sol[4, 0], 0.0)
        self.assertAlmostEqual(simulation.solution.stat_sol[5, 0], 0.1666667)
        self.assertAlmostEqual(simulation.solution.stat_sol[6, 0], 0.1666667)
        self.assertAlmostEqual(simulation.solution.stat_sol[7, 0], 0.1666667)