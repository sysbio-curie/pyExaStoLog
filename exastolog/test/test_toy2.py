from unittest import TestCase
from ..Model import Model
from ..Simulation import Simulation
from os.path import dirname, join

class TestToy2(TestCase):
    
    def test_toy2(self):
        
        model = Model(join(dirname(__file__), "../../notebooks/model_files/toy2.bnet"))
        simulation = Simulation(model, ['A', 'B', 'C'], [0, 0, 0])
        result = simulation.get_last_states_probtraj()
                
        self.assertAlmostEqual(result.iloc[0, :].sum(), 1.0)
        self.assertAlmostEqual(result.loc[0, '<nil>'], 0.1666667)
        self.assertAlmostEqual(result.loc[0, 'A'], 0.1666667)
        self.assertAlmostEqual(result.loc[0, 'B'], 0.1666667)
        self.assertAlmostEqual(result.loc[0, 'A -- C'], 0.1666667)
        self.assertAlmostEqual(result.loc[0, 'B -- C'], 0.1666667)
        self.assertAlmostEqual(result.loc[0, 'A -- B -- C'], 0.1666667)
