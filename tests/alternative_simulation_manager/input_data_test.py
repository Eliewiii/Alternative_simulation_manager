"""

"""

import pytest

from alt_sim_man.alternative_simulation_manager.simulation_step import SimulationStep
from alt_sim_man.alternative_simulation_manager.input_data import InputData

from .simulation_step_test import step1,step2,step3

# Fixture for SimulationStep
@pytest.fixture
def indata_1(step1):
    return step1.generate_input_data("in_1",{"param1":1,"param2":3.5})

@pytest.fixture
def indata_2(step2):
    return step2.generate_input_data("in_2",{"param3":1,"param4":3.5})

@pytest.fixture
def indata_3(step3):
    return step3.generate_input_data("in_3",{"param5":1,"param6":3.5})

# Fixture for SimulationStep
@pytest.fixture
def indata_1_2(step1):
    return step1.generate_input_data("in_1_2",{"param1":1,"param2":4.})

@pytest.fixture
def indata_2_2(step2):
    return step2.generate_input_data("in_2_2",{"param3":1,"param4":4.})

@pytest.fixture
def indata_3_2(step3):
    return step3.generate_input_data("in_3_3",{"param5":1,"param6":4.})

class TestInputData:

    def test_init(self):

        input_data = InputData("test","Step_1", {"param1":1,"param2":3.5})

    def test_init_from_sim_step(self,step1):
        sim_step_1 = step1
        input_data_1 = sim_step_1.generate_input_data("in_test",{"param1":1,"param2":3.5})
        with pytest.raises(ValueError):
            input_data = sim_step_1.generate_input_data("in_test", {"param1": 1, "param3": 3.5})
        # test without optional input
        input_data_1 = sim_step_1.generate_input_data("in_test", {"param1": 1})

    def test_eq(self,step1):
        sim_step_1 = step1
        input_data_1 = sim_step_1.generate_input_data("in_test", {"param1": 1, "param2": 3.5})
        input_data_2 = sim_step_1.generate_input_data("in_test", {"param1": 1, "param2": 3.5})
        input_data_3 = sim_step_1.generate_input_data("in_test", {"param1": 1, "param2": 4.})

        assert input_data_1 == input_data_2
        assert not input_data_1 == input_data_3






