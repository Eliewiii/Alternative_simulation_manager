"""
Class to manage alternatives for simulations with multiple common simulation steps.
"""
import dill
import os
from typing import Callable, Dict, List, Optional

from .simulation_step import SimulationStep


class AlternativeSimulationManager:
    """
    A class to manage and execute alternative simulation workflows using various steps.

    :param steps: A dictionary where keys are step names and values are SimulationStep objects.
    :param alternatives: A dictionary where keys are alternative names and values are lists of step names.
    """

    def __init__(self):
        self.steps: Dict[str, 'SimulationStep'] = {}
        self.alternatives: Dict[str, List[str]] = {}

    def add_step(self, name: str, function: Callable, dependencies: Optional[List[str]] = None) -> None:
        """
        Add a simulation step to the manager.

        :param name: The name of the simulation step.
        :param function: A callable function for the step.
        :param dependencies: A list of dependencies for the step (optional).
        :return: None
        """
        self.steps[name] = SimulationStep(name, function, dependencies)

    def add_alternative(self, alt_name: str, workflow_steps: List[str]) -> None:
        """
        Add an alternative simulation workflow to the manager.

        :param alt_name: The name of the alternative workflow.
        :param workflow_steps: A list of step names that define the workflow.
        :return: None
        """
        self.alternatives[alt_name] = workflow_steps

    def run(self, alt_name: str) -> Dict[str, any]:
        """
        Run a simulation based on the selected alternative.

        :param alt_name: The name of the alternative workflow to run.
        :return: A dictionary with step names as keys and their corresponding results as values.
        :raises ValueError: If the alternative or step names are invalid.
        """
        if alt_name not in self.alternatives:
            raise ValueError(f"❌ Alternative '{alt_name}' not found")

        results = {}
        for step_name in self.alternatives[alt_name]:
            if step_name not in self.steps:
                raise ValueError(f"❌ Step '{step_name}' not found in the manager")

            step = self.steps[step_name]
            inputs = [results[dep] for dep in step.dependencies]
            results[step_name] = step.run(inputs)
        return results

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
