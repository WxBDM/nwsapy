class ErrorBase(Exception):
    # base class for errors.
    pass

# NOTE: bad queries to the API (i.e. invalid ID, etc) are handled by the API. These here are for only ensuring
#   that the data is correct from the user end.


class ParameterTypeError(ErrorBase):
    """Exception raised for errors in the parameters. Only should be used for dev errors.

    Attributes
    ----------
    message -- explanation of the error
    """

    def __init__(self, parameter = None, expected_type = None, **kwargs):
        if not all(isinstance(ele, type(None)) for ele in (parameter, expected_type)): # backwards compatability
            self.message = f"Parameter must be of type {expected_type}. Got: {type(parameter)}"
            super().__init__(self.message)

        if 'filter_by_test' in kwargs.keys():
            self.message = "All parameter types cannot be none!"
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


class ParameterConflict(ErrorBase):
    """Exception raised for filter_by when 2 or more parameters supplied conflict with constraints.

    Attributes
    ----------
    message -- an explaination of the error
    """

    def __init__(self, parameter_list):
        self.message = f"Parameter conflicts: '{parameter_list}'. These parameters cannot " \
                       "be used together. Use only one. See documentation for more details."
        super().__init__(self.message)
