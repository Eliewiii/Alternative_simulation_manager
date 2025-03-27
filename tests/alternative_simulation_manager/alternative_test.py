"""

"""

import pytest

from alt_sim_man.alternative_simulation_manager.alternative import Alternative

from .simulation_step_test import step1, step2, step3
from .input_data_test import indata_1, indata_2, indata_3




class TestInputData:

    def test_init(self,step1,step2,indata_1,indata_2):
        # Init with 1 simulation step
        alt_0 = Alternative("test",step_list=[step1],input_data_list=[indata_1])
        assert alt_0.num_step == 1
        alt_0.add_simulation_step(step2,indata_2)
        assert alt_0.num_step == 2

        with pytest.raises(ValueError):
            alt_0.add_simulation_step(step2, indata_1)






