import hashlib
from unittest import TestCase
import requests

# A TestCase-based class to run a test on the api
class TestAuth(TestCase):
    def test_get_checksum(self):
        url = "http://0.0.0.0:8888"
        response = requests.get("0.0.0.0:8000/auth")
        token = response.headers["Badsec-Authentication-Token"]
        user_checksum = hashlib.sha256(f"{token}/users").hexdigest()
