"""

"""

class InputData:
    """
    This class represents the input data for a specific simulation step.
    It holds parameters that are specific to the step, and can be preprocessed before assignment.
    """
    def __init__(self, identifier: str, step_name: str, **params: dict):
        """
        Initialize the InputData with a unique identifier, the name of the associated step, and parameters.

        :param identifier: Unique identifier for the InputData instance.
        :param step_name: The name of the simulation step to which this InputData is tied.
        :param params: Parameters specific to the simulation step.
        """
        self.identifier = identifier
        self.step_name = step_name
        self.params = params

    def preprocess(self) -> None:
        """
        Preprocess the input data if needed (e.g., validate, modify, or compute derived values).
        This method can be extended with any specific preprocessing logic.

        :return: None
        """
        pass

    def get_params(self) -> dict:
        """
        Return the parameters as a dictionary.

        :return: A dictionary of parameters for the simulation step.
        """
        return self.params

    def __repr__(self) -> str:
        return f"InputData(identifier={self.identifier}, step_name={self.step_name}, params={self.params})"

    def __eq__(self, other: object) -> bool:
        """
        Compare two InputData objects for equality. They are considered equal if they have the same identifier,
        step name, and parameters.

        :param other: The other object to compare against.
        :return: True if the objects are considered equal, False otherwise.
        """
        if not isinstance(other, InputData):
            return False  # Ensure we are comparing InputData objects

        # Compare identifier, step_name, and params (dictionary)
        return (
                self.identifier == other.identifier and
                self.step_name == other.step_name and
                self.params == other.params
        )