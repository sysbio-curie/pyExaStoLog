from unittest import TestCase
from ..Model import Model
from ..Simulation import Simulation
from os.path import dirname, join

class TestToy(TestCase):
    
    def test_toy(self):
        
        model = Model(join(dirname(__file__), "../../notebooks/model_files/toy.bnet"))
        simulation = Simulation(model, ['A','C','D'], [0, 0, 0])
        
        self.assertEqual(simulation.solution.stat_sol[0, 0], 0.0)
        self.assertEqual(simulation.solution.stat_sol[1, 0], 0.0)
        self.assertEqual(simulation.solution.stat_sol[2, 0], 0.5)
        self.assertEqual(simulation.solution.stat_sol[3, 0], 0.0)
        self.assertEqual(simulation.solution.stat_sol[4, 0], 0.5)
        self.assertEqual(simulation.solution.stat_sol[5, 0], 0.0)
        self.assertEqual(simulation.solution.stat_sol[6, 0], 0.0)
        self.assertEqual(simulation.solution.stat_sol[7, 0], 0.0)
        
