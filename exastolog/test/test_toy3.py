from unittest import TestCase
from ..Model import Model
from ..Simulation import Simulation
from os.path import dirname, join

class TestToy3(TestCase):
    
    def test_toy3(self):
        
        model = Model(join(dirname(__file__), "../../notebooks/model_files/toy3.bnet"))
        simulation = Simulation(model, ['A','B'], [0, 0])
        
        self.assertAlmostEqual(simulation.solution.stat_sol[0, 0], 0.25)
        self.assertAlmostEqual(simulation.solution.stat_sol[1, 0], 0.25)
        self.assertAlmostEqual(simulation.solution.stat_sol[2, 0], 0.25)
        self.assertAlmostEqual(simulation.solution.stat_sol[3, 0], 0.25)