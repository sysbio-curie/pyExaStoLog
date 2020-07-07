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
        
        print(simulation.solution.stat_sol)