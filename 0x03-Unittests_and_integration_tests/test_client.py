#!/usr/bin/env python3
"""
client test module
"""
from client import GithubOrgClient, get_json
from fixtures import TEST_PAYLOAD
from parameterized import parameterized, param, parameterized_class
import unittest
from unittest.mock import Mock, PropertyMock, call, patch


class TestGithubOrgClient(unittest.TestCase):
    """ TestGithubOrgClient class"""
    @parameterized.expand([
        ('google', {"google": True}),
        ('abc', {"abc", True})
    ])
    @patch('client.get_json')
    def test_org(self, org, expected, mock_get_json):
        """org test case"""
        mock_get_json.return_value = expected
        g = GithubOrgClient(org)
        self.assertEqual(g.org, expected)
        link = f"https://api.github.com/orgs/{org}"
        mock_get_json.assert_called_once_with(link)

    def test_public_repos_url(self):
        """public repos urls test case"""
        org = "google"
        with patch('client.GithubOrgClient.org', new_callable=PropertyMock) as patched:
            patched.return_value = {"repos_url": f"https://api.github.com/orgs/{org}"}
            g = GithubOrgClient(org)
            self.assertEqual(g._public_repos_url, f"https://api.github.com/orgs/google")
    
    @patch('client.get_json')
    def test_public_repos(self, mock_get_json):
        """public repos test case"""
        org = "google"
        mock_get_json.return_value = [{"name": "google"}]
        with patch('client.GithubOrgClient._public_repos_url', new_callable=PropertyMock) as patched:
            patched.return_value = "https://api.github.com/orgs/google"
            g = GithubOrgClient(org)
            res = g.public_repos()
            self.assertEqual(res, ['google'])
            patched.assert_called_once()
        mock_get_json.assert_called_once()

    @parameterized.expand([
        param(repo={"license": {"key": "my_license"}}, license_key="my_license", expected=True),
        param(repo={"license": {"key": "other_license"}}, license_key="my_license", expected=False)
    ])
    def test_has_license(self, repo, license_key, expected):
        """ has license test case"""
        g = GithubOrgClient('google')
        val = g.has_license(repo, license_key)
        self.assertEqual(val, expected)


@parameterized_class(("org_payload", "repos_payload", "expected_repos", "apache2_repos"), 
                     TEST_PAYLOAD)
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """ Integration test for github org client """

    @classmethod
    def setUpClass(cls):
        """ prepare for testing """
        org = TEST_PAYLOAD[0][0]
        repos = TEST_PAYLOAD[0][1]
        org_mock = Mock()
        org_mock.json = Mock(return_value=org)
        cls.org_mock = org_mock
        repos_mock = Mock()
        repos_mock.json = Mock(return_value=repos)
        cls.repos_mock = repos_mock

        cls.get_patcher = patch('requests.get')
        cls.get = cls.get_patcher.start()

        options = {cls.org_payload["repos_url"]: repos_mock}
        cls.get.side_effect = lambda y: options.get(y, org_mock)

    @classmethod
    def tearDownClass(cls):
        """ unprepare for testing """
        cls.get_patcher.stop()

    def test_public_repos(self):
        """ public repos test """
        y = GithubOrgClient("x")
        self.assertEqual(y.org, self.org_payload)
        self.assertEqual(y.repos_payload, self.repos_payload)
        self.assertEqual(y.public_repos(), self.expected_repos)
        self.assertEqual(y.public_repos("NONEXISTENT"), [])
        self.get.assert_has_calls([call("https://api.github.com/orgs/x"),
                                   call(self.org_payload["repos_url"])])

    def test_public_repos_with_license(self):
        """ public repos test """
        y = GithubOrgClient("x")
        self.assertEqual(y.org, self.org_payload)
        self.assertEqual(y.repos_payload, self.repos_payload)
        self.assertEqual(y.public_repos(), self.expected_repos)
        self.assertEqual(y.public_repos("NONEXISTENT"), [])
        self.assertEqual(y.public_repos("apache-2.0"), self.apache2_repos)
        self.get.assert_has_calls([call("https://api.github.com/orgs/x"),
                                   call(self.org_payload["repos_url"])])
