"""

"""

import dill
import os
from typing import Callable, List, Optional, Dict, Any

from .input_data import InputData


class SimulationStep:
    """
    A class to represent a simulation step.

    :param name: The name of the simulation step.
    :param function: A callable function that represents the logic of this step.
            :param required_params: A list of dictionaries, each defining the parameter's name, type, and whether it is optional.
    :param dependencies: A list of other step names that this step depends on (optional).
    """

    def __init__(self, name: str, function: Callable,required_params: List[Dict[str, Any]] ,dependencies: Optional[List[str]] = None):
        self.name = name
        self.function = function
        self.required_params = required_params
        self.dependencies = dependencies or []
        self.result = None

    def run(self, inputs: List) -> any:
        """
        Run the simulation step.

        :param inputs: The inputs required for the simulation step.
        :return: The result of the simulation step.
        """
        if self.result is None:  # Caching mechanism
            self.result = self.function(*inputs)
        return self.result

    def generate_input_data(self, identifier: str, **params: dict) -> InputData:
        """
        Generate InputData for this simulation step.

        :param identifier: Unique identifier for the InputData instance.
        :param params: Parameters to initialize the InputData for this step.
        :return: An InputData instance.
        """
        missing_params = []
        invalid_params = []

        # Validate each required parameter
        for param in self.required_params:
            param_name = param["name"]
            param_type = param["type"]
            param_optional = param.get("optional", False)

            # Check if the parameter is provided
            if param_name not in params:
                if not param_optional:
                    missing_params.append(param_name)
            else:
                # Check if the type matches
                if not isinstance(params[param_name], param_type):
                    invalid_params.append(param_name)

        if missing_params:
            raise ValueError(f"Missing required parameters for step {self.name}: {', '.join(missing_params)}")
        if invalid_params:
            raise ValueError(f"Invalid types for parameters in step {self.name}: {', '.join(invalid_params)}")

        # Generate and return InputData
        input_data = InputData(identifier, self.name, **params)
        return input_data



    @staticmethod
    def save(obj: 'SimulationStep', filename: str) -> None:
        """
        Save a SimulationStep object to a file using dill.

        :param obj: The SimulationStep object to be saved.
        :param filename: The file path where the SimulationStep should be saved.
        :return: None
        """
        try:
            with open(filename, "wb") as f:
                dill.dump(obj, f)
            print(f"✅ SimulationStep saved to {filename}")
        except Exception as e:
            print(f"❌ Error saving SimulationStep: {e}")

    @staticmethod
    def load(filename: str) -> 'SimulationStep':
        """
        Load a SimulationStep object from a file using dill.

        :param filename: The file path from which to load the SimulationStep.
        :return: The loaded SimulationStep object.
        :raises FileNotFoundError: If the file does not exist.
        :raises TypeError: If the loaded object is not of type SimulationStep.
        """
        if not os.path.isfile(filename):
            raise FileNotFoundError(f"❌ File not found: {filename}")

        try:
            with open(filename, "rb") as f:
                obj = dill.load(f)
            if not isinstance(obj, SimulationStep):
                raise TypeError(f"❌ Loaded object is not of type 'SimulationStep'")
            print(f"✅ SimulationStep loaded from {filename}")
            return obj
        except Exception as e:
            print(f"❌ Error loading SimulationStep: {e}")
            raise

    def __eq__(self, other: object) -> bool:
        """
        Compare two InputData objects for equality. They are considered equal if they have the same identifier,
        step name, and parameters.

        :param other: The other object to compare against.
        :return: True if the objects are considered equal, False otherwise.
        """
        if not isinstance(other, SimulationStep):
            return False  # Ensure we are comparing InputData objects

        # Compare identifier, step_name, and params (dictionary)
        return (
                self.name == other.name and
                self.required_params == other.required_params and
                self.function.__name__ == other.function.__name__
        )