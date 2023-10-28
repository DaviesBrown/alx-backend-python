#!/usr/bin/env python3
"""
client test module
"""
from client import GithubOrgClient, get_json
import unittest
from unittest.mock import patch
from parameterized import parameterized


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
