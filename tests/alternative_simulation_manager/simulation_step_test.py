"""

"""

import pytest

from alt_sim_man.alternative_simulation_manager.simulation_step import SimulationStep

# Fixture for SimulationStep
@pytest.fixture
def step1():
    return SimulationStep(
        name="Step 1",
        function= max,
        required_params=[{"name":"param1","type":int}, {"name":"param2","type":float,"optional":True}]
    )

def step2():
    return SimulationStep(
        name="Step 2",
        function= max,
        required_params=[{"name":"param3","type":int}, {"name":"param4","type":float,"optional":True}]
    )

def step3():
    return SimulationStep(
        name="Step 3",
        function= max,
        required_params=[{"name":"param5","type":int}, {"name":"param6","type":float,"optional":True}]
    )