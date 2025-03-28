"""
Class to manage alternatives for simulations with multiple common simulation steps.
"""
import dill
import os
import logging
from typing import Callable, Dict, List, Optional

from .simulation_step import SimulationStep
from .alternative import Alternative
from .input_data import InputData


class AlternativeSimulationManager:
    """
    A class to manage and execute alternative simulation workflows using various steps.

    :param steps: A dictionary where keys are step names and values are SimulationStep objects.
    :param alternatives: A dictionary where keys are alternative names and values are lists of step names.
    """

    def __init__(self):
        self._alternative_dict: Dict[str, Alternative] = {}


    @property
    def num_alternatives(self):
        return len(self._alternative_dict)

    @property
    def alternative_id_list(self):
        return list(self._alternative_dict.keys())

    @property
    def _alternative_list(self):
        return list(self._alternative_dict.values())

    def group_alternatives_to_tree(self,alternative_id_list):
        """
        Groups alternatives based on shared simulation steps and input data.
        Each alternative's steps are considered individually, and the tree is built.
        :param alternatives: List of alternatives to group.
        """
        return self._group_alternatives_recursive([self._alternative_dict[id] for id in alternative_id_list],step_index=0)

    def _group_alternatives_recursive(self, alternative_list: List[Alternative], step_index: int = 0) -> list:
        """
        Recursively groups alternatives based on the simulation steps they have and their associated input data.
        If alternatives share the same step and input data, they are grouped together.
        :param alternatives: List of alternatives to group.
        :param step_index: The index of the current step in the simulation process.
        :return: A list of groups, each group contains alternatives sharing the same step and input data.
        """
        if not alternative_list:
            return []

        # # If we have exhausted all steps, return individual alternatives as leaf nodes.
        # if step_index >= max(len(alt.steps) for alt in alternatives):
        #     return [[alt] for alt in alternatives]

        # Group alternatives by the current step and input data
        group_list = []
        for alt in alternative_list:
            if step_index < alt.num_step:
                added_flag = False
                for group in group_list:
                    if Alternative.has_same_simulation_step(alt,group[0],step_index,check_inputdata=True):
                        group.append(alt)
                        added_flag =True
                        break
                if not added_flag:
                    group_list.append([alt])


        # Process to the next step for each group
        tree = []
        for group in group_list:
            # Recursively group the alternatives based on the next step
            sub_groups = self._group_alternatives_recursive(list(group), step_index + 1)
            group_with_next_steps = list(group)
            group_with_next_steps.append(list(sub_groups) if sub_groups !=[] else [])
            tree.append(group_with_next_steps)  # Add step info along with subgroups

        return list(tree)

    def add_alternatives(self, alternative_list: List[Alternative]) -> None:
        """
        Add a list of Alternative to the simulation manager.

        :param alternative_list: The name of the alternative workflow.
        :return: None
        """
        for alternative in alternative_list:
            if not isinstance(alternative,Alternative):
                raise TypeError(f"the object {alternative} is not an Alternative object")
            if alternative.identifier in list[self._alternative_dict.keys()]:
                logging.WARNING(f"The alternative {alternative.identifier} is already in the "
                                 f"AlternativeSurfaceManager, it will not be added a second time")
                return
            self._alternative_dict[alternative.identifier] = alternative

    def set_up(self, path_simulation_folder:str, alternative_id_list: Optional[List[str]] = []) -> Dict[str, any]:
        """
        Run a simulation based on the selected alternative.

        :param alt_name: The name of the alternative workflow to run.
        :return: A dictionary with step names as keys and their corresponding results as values.
        """
        # Set the alternatives to run
        if  alternative_id_list:
            alternative_id_list = set(alternative_id_list) # remove duplicate

            invalid_id = []
            for alternative_id in alternative_id_list:
                if alternative_id not in self._alternative_dict:
                    invalid_id.append(alternative_id)
            if invalid_id:
                raise KeyError(f"The alternatives with ids:'{"', '".join(invalid_id)}' are not part of the "
                               f"AlternativeSimulationManager. Please input only valid alternatives")
        else:
            alternative_id_list = self.alternative_id_list
        # Group alternatives at each simulation steps
        self.group_alternatives_to_tree(alternative_id_list=alternative_id_list)

        # if alt_name not in self.alternatives:
        #     raise ValueError(f"❌ Alternative '{alt_name}' not found")
        #
        # results = {}
        # for step_name in self.alternatives[alt_name]:
        #     if step_name not in self.steps:
        #         raise ValueError(f"❌ Step '{step_name}' not found in the manager")
        #
        #     step = self.steps[step_name]
        #     inputs = [results[dep] for dep in step.dependencies]
        #     results[step_name] = step.run(inputs)
        # return results

    @staticmethod
    def save(obj: 'AlternativeSimulationManager', filename: str) -> None:
        """
        Save an AlternativeSimulationManager object to a file using dill.

        :param obj: The AlternativeSimulationManager object to be saved.
        :param filename: The file path where the AlternativeSimulationManager should be saved.
        :return: None
        """
        try:
            with open(filename, "wb") as f:
                dill.dump(obj, f)
            print(f"✅ AlternativeSimulationManager saved to {filename}")
        except Exception as e:
            print(f"❌ Error saving AlternativeSimulationManager: {e}")

    @staticmethod
    def load(filename: str) -> 'AlternativeSimulationManager':
        """
        Load an AlternativeSimulationManager object from a file using dill.

        :param filename: The file path from which to load the AlternativeSimulationManager.
        :return: The loaded AlternativeSimulationManager object.
        :raises FileNotFoundError: If the file does not exist.
        :raises TypeError: If the loaded object is not of type AlternativeSimulationManager.
        """
        if not os.path.isfile(filename):
            raise FileNotFoundError(f"❌ File not found: {filename}")

        try:
            with open(filename, "rb") as f:
                obj = dill.load(f)
            if not isinstance(obj, AlternativeSimulationManager):
                raise TypeError(f"❌ Loaded object is not of type 'AlternativeSimulationManager'")
            print(f"✅ AlternativeSimulationManager loaded from {filename}")
            return obj
        except Exception as e:
            print(f"❌ Error loading AlternativeSimulationManager: {e}")
            raise

    @classmethod
    def load_from_steps(cls, step_filenames: List[str]) -> 'AlternativeSimulationManager':
        """
        Create an AlternativeSimulationManager instance from pickled SimulationStep objects.

        :param step_filenames: A list of filenames for the pickled SimulationStep objects.
        :return: A new AlternativeSimulationManager instance with the loaded steps.
        :raises FileNotFoundError: If any of the step files do not exist.
        """
        manager = cls()  # Create a new instance of AlternativeSimulationManager

        # Load all steps first and verify that they exist
        for step_filename in step_filenames:
            if not os.path.isfile(step_filename):
                raise FileNotFoundError(f"❌ Step file not found: {step_filename}")

            step = SimulationStep.load(step_filename)
            manager.add_step(step.name, step.function, step.dependencies)

        print("✅ AlternativeSimulationManager created from pickled SimulationSteps.")
        return manager


def to_str_recursive(data):
    """Recursively converts all elements in a list (and sublists) to strings."""
    if isinstance(data, list):
        return [to_str_recursive(item) for item in data]  # Recursively process sublists
    return str(data)  # Convert non-list elements to string
