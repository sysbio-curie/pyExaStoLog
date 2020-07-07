from unittest import TestCase
from ..Model import Model
from ..Simulation import Simulation
from os.path import dirname, join

class TestMammalianCC(TestCase):
    
    def test_mammalian_cc(self):
        
        model = Model(join(dirname(__file__), "../../notebooks/model_files/mammalian_cc.bnet"))
        simulation = Simulation(
            model, 
            ['CycE','CycA','CycB','Cdh1','Rb_b1','Rb_b2','p27_b1','p27_b2'], 
            [0, 0, 0, 1, 1, 1, 1, 1],
        )
        
        print(simulation.solution.stat_sol)
        # self.assertEqual(simulation.solution.stat_sol[0, 0], 0.0)
        # self.assertEqual(simulation.solution.stat_sol[1, 0], 0.0)
        # self.assertEqual(simulation.solution.stat_sol[2, 0], 0.5)
        # self.assertEqual(simulation.solution.stat_sol[3, 0], 0.0)
        # self.assertEqual(simulation.solution.stat_sol[4, 0], 0.5)
        # self.assertEqual(simulation.solution.stat_sol[5, 0], 0.0)
        # self.assertEqual(simulation.solution.stat_sol[6, 0], 0.0)
        # self.assertEqual(simulation.solution.stat_sol[7, 0], 0.0)
        
