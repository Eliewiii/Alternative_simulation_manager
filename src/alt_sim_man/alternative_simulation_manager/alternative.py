"""

"""

from typing import List

from .input_data import InputData
from .simulation_step import SimulationStep


class Alternative:
    """
    Represents a specific alternative simulation, which could share steps with other alternatives
    but might have unique parameters for its simulation steps.
    """

    def __init__(self, identifier: str, step_list: List[SimulationStep], input_data_list: List[InputData]):
        """
        :param identifier: unique identifier of the alternative
        :param step_list:
        :param input_data_list:
        """
        self._identifier = identifier
        self._step_list:List[SimulationStep] = []  # List of steps to run for this alternative in order
        self._input_data_list:List[InputData] = []  # List of corresponding input data
        for sim_step, input_data in zip(step_list, input_data_list):
            self.add_simulation_step(sim_step, input_data)

    @property
    def identifier(self):
        return self._identifier

    @property
    def step_list(self):
        return self._step_list

    @property
    def input_data_list(self):
        return self._input_data_list

    @property
    def num_step(self):
        return len(self._step_list)


    def add_simulation_step(self, sim_step: SimulationStep, input_data: InputData):
        """
        Add a SimulationStep and its corresponding InputData object.
        No checks for duplicated simulation steps as it it might be necessary to run steps twice.
        :param sim_step:
        :param input_data:
        """
        if sim_step.is_inputdata_from_self(input_data):
            self._step_list.append(sim_step)
            self._input_data_list.append(input_data)

    def adjust_identifier_from_inputdata_identifier(self):
        """

        """
        if len(self._step_list)>0:
            self._identifier = "_".join([step.prefix + "_" + input_data.identifier for step, input_data in
                           zip(self._step_list, self._input_data_list)])
        else:
            return

    def run(self) -> dict:
        """
        Run the simulation for this alternative.

        :return: A dictionary containing the results of each step.
        """
        # results = {}
        # for step in self.steps:
        #     # Use the shared input data for common parameters,
        #     # and possibly specific parameters for this alternative if any.
        #     step_inputs = self.input_data.__dict__  # Convert the input data into a dict
        #     results[step.name] = step.run(step_inputs)
        # return results
