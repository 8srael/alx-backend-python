#!/usr/bin/env python3

"""
    Tests for GithubOrgClient class
"""

import unittest
from unittest.mock import patch
from parameterized import parameterized
from client import GithubOrgClient

class TestGithubOrgClient(unittest.TestCase):
    """ Class for testing GithubOrgClient """

    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
    @patch('client.get_json', return_value={"payload": True})
    def test_org(self, org_name: str, mock_get_json) -> None:
        """
            Test that GithubOrgClient.org returns the correct value.
        """
        # Create a GithubOrgClient instance
        client = GithubOrgClient(org_name)

        # Check that the .org property returns the mock response
        self.assertEqual(client.org, {"payload": True})

        # Verify that get_json was called once with the expected URL
        mock_get_json.assert_called_once_with(f"https://api.github.com/orgs/{org_name}")

        