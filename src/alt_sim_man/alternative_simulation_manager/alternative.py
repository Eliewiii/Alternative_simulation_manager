"""

"""
import os
import json

from copy import deepcopy
from typing import List, Tuple, Optional

from .input_data import InputData
from .simulation_step import SimulationStep
from ..utils.utils_folder_manipulation import check_dir_exist, check_file_exist, create_dir


class Alternative:
    """
    Represents a specific alternative simulation, which could share steps with other alternatives
    but might have unique parameters for its simulation steps.
    """
    NAME_PROGRESS_FILE = "progress.json"
    EMPTY_STEP_DICT_PROGRESS_FILE = {
        "step_id": None,
        "input_data_id": None,
        "has_run": False,
        "duration": None,
        "parent_alternative": None
    }

    def __init__(self, identifier: str, step_input_data_tuple_list: List[Tuple[SimulationStep, InputData]]):
        """
        :param identifier: unique identifier of the alternative
        :param step_list:
        :param input_data_list:
        """
        self._identifier = identifier
        self._step_list: List[SimulationStep] = []  # List of steps to run for this alternative in order
        self._input_data_list: List[InputData] = []  # List of corresponding input data
        for sim_step, input_data in step_input_data_tuple_list:
            self.add_simulation_step(sim_step, input_data)

    def __repr__(self):
        return self._identifier

    def __str__(self):
        return self._identifier

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

    def _path_alternative_dir(self, path_simulation_dir):
        return os.path.join(path_simulation_dir, self.identifier)

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
        if len(self._step_list) > 0:
            self._identifier = "_".join([step.prefix + "_" + input_data.identifier for step, input_data in
                                         zip(self._step_list, self._input_data_list)])
        else:
            return

    @classmethod
    def has_same_simulation_step(cls, alternative_1: 'Alternative', alternative_2: 'Alternative', step_index: int,
                                 check_inputdata: bool = False):
        """

        :param alternative_1:
        :param alternative_2:
        :param step_index:
        :param check_inputdata:
        :return:
        """
        if not isinstance(alternative_1, cls) or not isinstance(alternative_2, cls):
            raise TypeError(f"Expected Alternative objects, got {type(alternative_1)} and {alternative_2}")

        if step_index >= alternative_1.num_step or step_index >= alternative_2.num_step:
            raise IndexError(
                f"Expected more than {step_index} steps, got {alternative_1.num_step} and {alternative_2.num_step} steps")

        if not alternative_1._step_list[step_index] == alternative_2.step_list[step_index]:
            return False
        if check_inputdata and not alternative_1._input_data_list[step_index] == alternative_2._input_data_list[
            step_index]:
            return False

        return True

    def make_alternative_dir(self, path_simulation_dir: str, overwrite: bool = False):
        """

        :param path_simulation_dir: str, path to the simulation folder containing all the alternative sub-folders
        :param overwrite: bool, True if the alternative directory needs to be overwritten if it exists
        """
        check_dir_exist(path_simulation_dir)
        create_dir(path_dir=self._path_alternative_dir(path_simulation_dir), overwrite=overwrite)

    def init_progress_json_file(self, path_simulation_dir: str):
        """
        Create the file to track the progress
        :param path_simulation_dir: str, path to the simulation folder containing all the alternative sub-folders
        :return:
        """
        check_dir_exist(path_dir=self._path_alternative_dir(path_simulation_dir))
        path_progress_file = os.path.join(self._path_alternative_dir(path_simulation_dir), self.NAME_PROGRESS_FILE)
        progress_dict = {i: deepcopy(self.EMPTY_STEP_DICT_PROGRESS_FILE) for i in range(self.num_step)}
        for i in range(self.num_step):
            progress_dict[i]["step_id"] = self._step_list[i].name
            progress_dict[i]["input_data_id"] = self._input_data_list[i].identifier
        with open(path_progress_file, "w") as f:
            json.dump(progress_dict, f, indent=4)

    def update_progress_json_file_after_run_step(self, path_simulation_dir: str, step_index: int, duration: float,
                                                 parent_alternative: Optional[str | None] = None):
        """

        :param path_simulation_dir: str, path to the simulation folder containing all the alternative sub-folders
        :param step_index: int,
        :param duration: float,
        :param parent_alternative: str or None,
        :return:
        """
        if step_index >= self.num_step:
            raise IndexError(f"Try to update progress file step number {step_index} for Alternative "
                             f"'{self.identifier}' while it has only {self.num_step}")
        path_progress_file = os.path.join(self._path_alternative_dir(path_simulation_dir), self.NAME_PROGRESS_FILE)
        check_file_exist(path_progress_file)
        # Load the config file as a dictionary
        with open(path_progress_file, 'r') as f:
            progress_dict = json.load(f)
        progress_dict[step_index]["has_run"] = True
        progress_dict[step_index]["duration"] = duration
        progress_dict[step_index]["parent_alternative"] = parent_alternative
        with open(path_progress_file, "w") as f:
            json.dump(progress_dict, f, indent=4)

    def run(self, path_simulation_dir: str, step_index: int) -> dict:
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
