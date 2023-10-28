#!/usr/bin/env python3
"""
test utils module
"""
from mock import PropertyMock
from parameterized import parameterized, param
import unittest
from unittest.mock import patch
from utils import access_nested_map, get_json, memoize


class TestAccessNestedMap(unittest.TestCase):
    """
    TestAccessNestedMap class that inherits from unittest.TestCas
    """
    @parameterized.expand([
        param(nested_map={"a": 1}, path=("a",), expected=1),
        param(nested_map={"a": {"b": 2}}, path=("a",), expected={"b": 2}),
        param(nested_map={"a": {"b": 2}}, path=("a", "b"), expected=2)
    ])
    def test_access_nested_map(self, nested_map, path, expected):
        """ unit test for utils.access_nested_map"""
        self.assertEqual(access_nested_map(nested_map, path), expected)

    @parameterized.expand([
        param(nested_map={}, path=("a",), expected=KeyError),
        param(nested_map={"a": 1}, path=("a", "b"), expected=KeyError)
    ])
    def test_access_nested_map_exception(self, nested_map, path, expected):
        """ KeyError is raised for the following inputs"""
        with self.assertRaises(expected):
            access_nested_map(nested_map, path)


class TestGetJson(unittest.TestCase):
    """ TestGetJson class"""
    @parameterized.expand([
        param(test_url="http://example.com", test_payload={"payload": True}),
        param(test_url="http://holberton.io", test_payload={"payload": False})
    ])
    def test_get_json(self, test_url, test_payload):
        """ test that utils.get_json returns the expected result"""
        with patch('test_utils.get_json', new_callable=PropertyMock)\
                as mock_get_json:
            mock_get_json.return_value = test_payload
            self.assertEqual(get_json(test_url), test_payload)
            mock_get_json.assert_called_once_with(test_url)


class TestMemoize(unittest.TestCase):
    """ TestMemoize class"""
    def test_memoize(self):
        """ memoized test cases"""
        class TestClass:
            """ Test class"""
            def a_method(self):
                """ a method"""
                return 42

            @memoize
            def a_property(self):
                """a property"""
                return self.a_method()

        with patch.object(TestClass, 'a_method', return_value=42)\
                as mock_a_method:
            testclass = TestClass()
            return_value = testclass.a_property
            self.assertEqual(return_value, 42)
            self.assertEqual(return_value, 42)
            mock_a_method.assert_called_once()
