"""

"""

import pytest

from alt_sim_man.alternative_simulation_manager.alternative_simulation_manager import AlternativeSimulationManager

from .simulation_step_test import step1, step2, step3
from .input_data_test import indata_1, indata_2, indata_3, indata_1_2, indata_2_2, indata_3_2
from .alternative_test import alt1,alt2,alt3,alt4,alt5,alt6




class TestAlternativeSimulationManager:

    def test_init(self,alt1,alt2,alt3):
        # Init with 1 simulation step
        alt_sim_manager = AlternativeSimulationManager()
        alt_sim_manager.add_alternatives([alt1,alt2,alt3])
        assert alt_sim_manager.num_alternatives==3
        alt_sim_manager.add_alternatives([alt1])
        assert alt_sim_manager.num_alternatives==3

    def test_group_alternatives_to_tree(self,alt1,alt2,alt3,alt4,alt5,alt6):
        alt_sim_manager = AlternativeSimulationManager()
        alt_sim_manager.add_alternatives([alt1, alt2, alt3,alt4,alt5,alt6])
        alt_sim_manager.group_alternatives_to_tree()

        print("ok")



