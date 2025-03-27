"""

"""




class Alternative:
    """
    Represents a specific alternative simulation, which could share steps with other alternatives
    but might have unique parameters for its simulation steps.
    """
    def __init__(self, name: str, input_data: InputData, steps: List[SimulationStep]):
        self.name = name
        self.input_data = input_data  # The shared input data instance
        self.steps = steps  # List of steps relevant to this alternative

    def run(self) -> dict:
        """
        Run the simulation for this alternative.

        :return: A dictionary containing the results of each step.
        """
        results = {}
        for step in self.steps:
            # Use the shared input data for common parameters,
            # and possibly specific parameters for this alternative if any.
            step_inputs = self.input_data.__dict__  # Convert the input data into a dict
            results[step.name] = step.run(step_inputs)
        return results