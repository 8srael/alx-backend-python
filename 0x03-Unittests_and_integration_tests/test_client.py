#!/usr/bin/env python3

"""
    Tests for GithubOrgClient class
"""

import unittest
from unittest.mock import patch
from parameterized import parameterized
from client import GithubOrgClient
from unittest.mock import PropertyMock

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



    def test_publc_repos_url(self) -> None:
        """
            Test that the _public_repos_url method returns the correct value.
        """
        
        with patch('client.GithubOrgClient.org', new_callable=PropertyMock) as mock_org:
            mock_org.return_value = {"repos_url": "http://test.com"}
            client = GithubOrgClient("test")
            self.assertEqual(client._public_repos_url, "http://test.com")
