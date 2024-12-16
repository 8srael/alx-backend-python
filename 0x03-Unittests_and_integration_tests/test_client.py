#!/usr/bin/env python3

"""
    Tests for GithubOrgClient class
"""

import unittest
from unittest.mock import patch
from parameterized import parameterized
from client import GithubOrgClient
from unittest.mock import PropertyMock
from typing import Dict

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



    def test_public_repos_url(self) -> None:
        """
            Test that the _public_repos_url method returns the correct value.
        """
        
        with patch('client.GithubOrgClient.org', new_callable=PropertyMock) as mock_org:
            mock_org.return_value = {"repos_url": "http://test.com"}
            client = GithubOrgClient("test")
            self.assertEqual(client._public_repos_url, "http://test.com")
            
    @patch('client.get_json', return_value=[{"name": "repo1"}, {"name": "repo2"}])            
    def test_public_repos(self, mock_get_json) -> None:
        """
            Test that the public_repos method returns the correct value.
        """
        mock_url = "http://api.github.com/orgs/google/repos"
        with patch('client.GithubOrgClient._public_repos_url', new_callable=PropertyMock,
                return_value=mock_url) as mock_public_repos_url:
            client = GithubOrgClient('google')
            repos = client.public_repos()

            # We expect the method to return ['repo1', 'repo2'] based on the mocked payload
            self.assertEqual(repos, ['repo1', 'repo2'])

            # Check that _public_repos_url was accessed once
            mock_public_repos_url.assert_called_once()

            # Check that get_json was called once with the mocked URL
            mock_get_json.assert_called_once_with(mock_url)

    @parameterized.expand([
        ({"key": "my_license"}, "my_license", True),
        ({"key": "other_license"}, "my_license", False),
    ])
    def has_license(self, repo:Dict[str, Dict], license_key:str, expected:bool)-> None:
        """
            Test that the has_license method returns the expected Bool value.
        """
        self.assertEqual(GithubOrgClient.has_license(repo, license_key), expected)
