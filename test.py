import hashlib
import json
from unittest import TestCase
import requests
from noclist import get_auth_checksum, get_auth_token, get_user_ids


# A TestCase-based class to run a test on the api
class TestAuth(TestCase):
    

    def test_get_checksum(self):
        url = url = "http://127.0.0.1:8888"
        token = get_auth_token(url=url)
        checksum = get_auth_checksum(token=token)
        users = get_user_ids(url=url, checksum=checksum)
        response = json.dumps(users.splitlines())
        self.assertEqual(type(response), str)
