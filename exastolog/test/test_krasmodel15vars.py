from unittest import TestCase
from ..Model import Model
from ..Simulation import Simulation
from os.path import dirname, join

class TestKRasModel15Vars(TestCase):
    
    def test_krasmodel15vars(self):
        
        model = Model(join(dirname(__file__), "../../notebooks/model_files/krasmodel15vars.bnet"))
        simulation = Simulation(
            model,
            ['cc','KRAS','DSB','cell_death'], #krasmodel15vars
            [1, 1, 1, 0], # krasmodel15vars: [1 1] is cell cycle ON, KRAS mutation ON
        )
        
        self.assertAlmostEqual(simulation.solution.stat_sol[35, 0], 0.16982301660209487)
        self.assertAlmostEqual(simulation.solution.stat_sol[67, 0], 0.01069429074391337)
        self.assertAlmostEqual(simulation.solution.stat_sol[291, 0], 0.25817666968396225)
        self.assertAlmostEqual(simulation.solution.stat_sol[323, 0], 0.01918748778666668)
        self.assertAlmostEqual(simulation.solution.stat_sol[16159, 0], 0.3131778050428693)
        self.assertAlmostEqual(simulation.solution.stat_sol[16387, 0], 0.09025865387229715)
        self.assertAlmostEqual(simulation.solution.stat_sol[16643, 0], 0.1386820789120975)
