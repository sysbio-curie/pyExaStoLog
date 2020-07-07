from unittest import TestCase
from ..Model import Model
from ..Simulation import Simulation
from os.path import dirname, join

class TestZanudo2017(TestCase):
    
    def test_zanudo_2017(self):
        
        model = Model(join(dirname(__file__), "../../notebooks/model_files/breast_cancer_zanudo2017.bnet"))
        simulation = Simulation(
            model, 
            ['Alpelisib', 'Everolimus','PIM','Proliferation','Apoptosis'], 
            [0, 1, 0, 0, 0]
        )
        
        self.assertAlmostEqual(simulation.solution.stat_sol[278706,0], 0.1863802656007465)
        self.assertAlmostEqual(simulation.solution.stat_sol[278714,0], 0.19011373881949112)
        self.assertAlmostEqual(simulation.solution.stat_sol[540850,0], 0.06361973446473712)
        self.assertAlmostEqual(simulation.solution.stat_sol[540858,0], 0.05988626143698639)
        self.assertAlmostEqual(simulation.solution.stat_sol[637954,0], 0.25)
        self.assertAlmostEqual(simulation.solution.stat_sol[637962,0], 0.25)