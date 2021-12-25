import pytest
from dotenv import load_dotenv
import os

class TestEndpoints:

    def __init__(self):
        load_dotenv()
        self.user_agent_name = "NWSAPy Testing Module"
        self.user_agent_contact = os.getenv("PYTEST_CONTACT_INFO")

    def test_all_endpoints_exist():
        """PyTest to ensure that the endpoints that we need (for development)
        exist in entrypoint.py.
        """
        pass

    def test_endpoints_have_variables():
        """Test to ensure that the variables needed for every endpoint
        is in the class.
        """
        pass