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

@pytest.fixture
def step2():
    return SimulationStep(
        name="Step 2",
        function= max,
        required_params=[{"name":"param3","type":int}, {"name":"param4","type":float,"optional":True}]
    )

@pytest.fixture
def step3():
    return SimulationStep(
        name="Step 3",
        function= max,
        required_params=[{"name":"param5","type":int}, {"name":"param6","type":float,"optional":True}]
    )

class TestSimulationStep:

    def test_init(self):

        sim_step = SimulationStep("test",max, [{"name":"param1","type":int}, {"name":"param2","type":float,"optional":True}])

    def test_equality(self):
        sim_step_1 = SimulationStep("test",max, [{"name":"param1","type":int}, {"name":"param2","type":float,"optional":True}])

        sim_step_2 = SimulationStep("test",max, [{"name":"param1","type":int}, {"name":"param2","type":float,"optional":True}])

        assert sim_step_1==sim_step_2

        sim_step_2 = SimulationStep("test",max, [{"name":"param3","type":int}, {"name":"param2","type":float,"optional":True}])

        assert not sim_step_1 == sim_step_2

