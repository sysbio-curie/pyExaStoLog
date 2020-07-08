from unittest import TestCase
from ..Model import Model
from ..Simulation import Simulation
from os.path import dirname, join

class TestToy(TestCase):
    
    def test_toy(self):
        
        model = Model(join(dirname(__file__), "../../notebooks/model_files/toy.bnet"))
        simulation = Simulation(model, ['A','C','D'], [0, 0, 0])
        result = simulation.get_last_states_probtraj()
        
        self.assertAlmostEqual(result.iloc[0, :].sum(), 1.0)
        self.assertAlmostEqual(result.loc[0, 'C'], 0.5)
        self.assertAlmostEqual(result.loc[0, 'D'], 0.5)
