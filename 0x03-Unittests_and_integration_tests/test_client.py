#!/usr/bin/env python3
"""Unit and integration tests for client.GithubOrgClient."""
import unittest
from parameterized import parameterized, parameterized_class
from unittest.mock import patch, Mock, PropertyMock
from typing import Dict

from client import GithubOrgClient
from fixtures import TEST_PAYLOAD


class TestGithubOrgClient(unittest.TestCase):
    """Unit tests for GithubOrgClient."""

    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
    @patch("client.get_json")
    def test_org(self, org_name: str, mock_get_json: Mock) -> None:
        """Test that org property returns correct value from get_json."""
        expected = {"name": org_name}
        mock_get_json.return_value = expected
        client = GithubOrgClient(org_name)
        self.assertEqual(client.org, expected)
        mock_get_json.assert_called_once_with(
            GithubOrgClient.ORG_URL.format(org=org_name)
        )

    def test_public_repos_url(self) -> None:
        """Test _public_repos_url returns repos_url from org payload."""
        payload = {"repos_url": "http://example.com/org/repos"}
        with patch.object(
            GithubOrgClient,
            "org",
            new_callable=PropertyMock
        ) as mock_org:
            mock_org.return_value = payload
            client = GithubOrgClient("google")
            self.assertEqual(client._public_repos_url, payload["repos_url"])

    @patch("client.get_json")
    def test_public_repos(self, mock_get_json: Mock) -> None:
        """Test public_repos returns repo names and mocks called once."""
        repos_payload = [
            {"name": "repo1", "license": {"key": "mit"}},
            {"name": "repo2", "license": {"key": "apache-2.0"}},
        ]
        mock_get_json.return_value = repos_payload

        with patch.object(
            GithubOrgClient,
            "_public_repos_url",
            new_callable=PropertyMock
        ) as mock_public_url:
            mock_public_url.return_value = "http://example.com/org/repos"
            client = GithubOrgClient("org")
            self.assertEqual(client.public_repos(), ["repo1", "repo2"])
            mock_public_url.assert_called_once()
            mock_get_json.assert_called_once()

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False),
    ])
    def test_has_license(
        self,
        repo: Dict,
        license_key: str,
        expected: bool
    ) -> None:
        """Test has_license returns True/False based on license key."""
        self.assertEqual(
            GithubOrgClient.has_license(repo, license_key),
            expected
        )


@parameterized_class((
    "org_payload",
    "repos_payload",
    "expected_repos",
    "apache2_repos"
), TEST_PAYLOAD)
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Integration tests for GithubOrgClient.public_repos."""

    @classmethod
    def setUpClass(cls):
        """Start patcher for requests.get with side_effect."""
        cls.get_patcher = patch("requests.get")
        cls.mock_get = cls.get_patcher.start()

        def side_effect(url, *args, **kwargs):
            m = Mock()
            if url.endswith("/repos"):
                m.json.return_value = cls.repos_payload
            else:
                m.json.return_value = cls.org_payload
            return m

        cls.mock_get.side_effect = side_effect

    @classmethod
    def tearDownClass(cls):
        """Stop patcher."""
        cls.get_patcher.stop()

    def test_public_repos(self):
        """Test public_repos returns expected list from fixtures."""
        client = GithubOrgClient("google")
        self.assertEqual(client.public_repos(), self.expected_repos)

    def test_public_repos_with_license(self):
        """Test public_repos filtered by license returns apache2_repos."""
        client = GithubOrgClient("google")
        self.assertEqual(
            client.public_repos("apache-2.0"),
            self.apache2_repos
        )
