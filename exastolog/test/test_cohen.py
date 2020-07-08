from unittest import TestCase
from ..Model import Model
from ..Simulation import Simulation
from os.path import dirname, join

class TestCohen(TestCase):
    
    def test_cohen(self):
        
        model = Model(join(dirname(__file__), "../../notebooks/model_files/EMT_cohen_ModNet.bnet"))
        simulation = Simulation(
            model, 
            ['ECMicroenv','DNAdamage','Metastasis','Migration','Invasion','EMT','Apoptosis','Notch_pthw','p53'], 
            [1, 1, 0, 0, 0, 0, 0, 1, 0], 
        )
        
        self.assertAlmostEqual(simulation.solution.stat_sol[206719,0], 0.6644136756213966)
        self.assertAlmostEqual(simulation.solution.stat_sol[790915,0], 0.1986146978998941)
        self.assertAlmostEqual(simulation.solution.stat_sol[803203,0], 0.13697162647870864)