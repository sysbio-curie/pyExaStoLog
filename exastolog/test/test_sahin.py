from unittest import TestCase
from ..Model import Model
from ..Simulation import Simulation
from os.path import dirname, join

class TestSahin(TestCase):
    
    def test_sahin(self):
        
        model = Model(join(dirname(__file__), "../../notebooks/model_files/sahin_breast_cancer_refined.bnet"))
        simulation = Simulation(
            model, 
            ['EGF','ERBB1','ERBB2','ERBB3','p21','p27'], 
            [1, 0, 0, 0, 1, 1]
        )
                
        self.assertAlmostEqual(simulation.solution.stat_sol[655231,0], 1.0)