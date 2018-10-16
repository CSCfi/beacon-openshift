import unittest

# from unittest import mock

from beacon_auth.wsgi import application


class TestSearchAPI(unittest.TestCase):
    """Test beacon-search API functions and endpoints."""

    def setUp(self):
        """Execute this method on start."""
        application.config['TESTING'] = True
        application.config['WTF_CSRF_ENABLED'] = False
        application.config['DEBUG'] = False
        self.app = application.test_client()

    def tearDown(self):
        """Execute this method after each test."""
        pass
