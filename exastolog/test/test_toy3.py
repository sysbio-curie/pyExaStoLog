from unittest import TestCase
from ..Model import Model
from ..Simulation import Simulation
from os.path import dirname, join
import numpy as np
import math

    
class TestToy3(TestCase):
    
    def test_toy3(self):
        
        model = Model(join(dirname(__file__), "../../notebooks/model_files/toy3.bnet"))
        simulation = Simulation(model, ['A','B'], [0, 0])
        result = simulation.get_last_states_probtraj()
                
        self.assertAlmostEqual(result.iloc[0, :].sum(), 1.0)
        self.assertAlmostEqual(result.loc[0, '<nil>'], 0.25)
        self.assertAlmostEqual(result.loc[0, 'A'], 0.25)
        self.assertAlmostEqual(result.loc[0, 'A'], 0.25)
        self.assertAlmostEqual(result.loc[0, 'A -- B'], 0.25)
 