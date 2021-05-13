class ErrorBase(Exception):
    # base class for errors.
    pass

# NOTE: bad queries to the API (i.e. invalid ID, etc) are handled by the API. These here are for only ensuring
#   that the data is correct from the user end.


class ParameterTypeError(ErrorBase):
    """Exception raised for errors in the parameters. Only should be used for user-end, not dev.

    Attributes
    ----------
    message -- explanation of the error
    """

    def __init__(self, parameter, expected_type):
        self.message = f"Parameter must be of type {expected_type}. Got: {type(parameter)}"
        super().__init__(self.message)


class DataValidationError(ErrorBase):
    """Exception raised for data validation. Only should be used for user identification, not dev.

    Attributes
    ----------
    message -- explanation of the error
    """

    def __init__(self, incorrect_data, more_info = ""):
        self.message = f"Invalid data input: '{incorrect_data}'. See documentation for valid inputs.\n{more_info}"
        super().__init__(self.message)