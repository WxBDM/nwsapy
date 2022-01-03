"""Class to define custom errors for NWSAPy.
"""

class DataValidationError(Exception):
    """Exception raised for a bad data validation. Direct users to the
    data validation tables listed in documentation.
    """
    def __init__(self, incorrect_data, more_info = ""):
        self.message = f"Invalid data input: `{incorrect_data}`. " \
            f"See documentation for valid inputs.\n{more_info}"
        super().__init__(self.message)

class KwargValidationError(Exception):
    
    def __init__(self, bad_kwarg, more_info = ""):
        self.message = f"Invalid key word argument: `{bad_kwarg}`. " \
            f"See the documentation for valid key word arguments."