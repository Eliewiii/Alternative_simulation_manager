"""

"""

import pytest

from alt_sim_man.alternative_simulation_manager.alternative import Alternative

from .simulation_step_test import step1, step2, step3
from .input_data_test import indata_1, indata_2, indata_3


# Fixture for SimulationStep
@pytest.fixture
def alt1(step1,step2,step3,indata_1,indata_2,indata_3):
    return Alternative("test",step_input_data_tuple_list=[(step1,indata_1),(step2,indata_2),(step3,indata_3)])

@pytest.fixture
def alt2(step1,step2,step3,indata_1,indata_2,indata_3):
    return Alternative("test",step_input_data_tuple_list=[(step1,indata_1),(step2,indata_2),(step3,indata_3)])

@pytest.fixture
def alt3(step1,step2,step3,indata_1,indata_2,indata_3):
    return Alternative("test",step_input_data_tuple_list=[(step1,indata_1),(step2,indata_2),(step3,indata_3)])

@pytest.fixture
def alt4(step1,step2,step3,indata_1,indata_2,indata_3):
    return Alternative("test",step_input_data_tuple_list=[(step1,indata_1),(step2,indata_2),(step3,indata_3)])

@pytest.fixture
def alt5(step1,step2,step3,indata_1,indata_2,indata_3):
    return Alternative("test",step_input_data_tuple_list=[(step1,indata_1),(step2,indata_2),(step3,indata_3)])

@pytest.fixture
def alt1(step1,step2,step3,indata_1,indata_2,indata_3):
    return Alternative("test",step_input_data_tuple_list=[(step1,indata_1),(step2,indata_2),(step3,indata_3)])


class TestInputData:

    def test_init(self,step1,step2,indata_1,indata_2):
        # Init with 1 simulation step
        alt_0 = Alternative("test",step_input_data_tuple_list=[(step1,indata_1),(step2,indata_2)])
        assert alt_0.num_step == 2


    def test_add_steps(self,step1,step2,step3,indata_1,indata_2,indata_3):
        alt_0 = Alternative("test",step_input_data_tuple_list=[(step1,indata_1),(step2,indata_2)])
        alt_0.add_simulation_step(step3,indata_3)
        assert alt_0.num_step == 3

        with pytest.raises(ValueError):
            alt_0.add_simulation_step(step2, indata_1)

        alt_0.add_simulation_step(step1, indata_1)
        assert alt_0.num_step == 4






