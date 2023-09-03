#!/usr/bin/env python3

""" Test utils module"""

import unittest
from parameterized import parameterized
from utils import access_nested_map
from typing import Dict, Tuple, List, Union


class TestAccessNestedMap(unittest.TestCase):
    """ Class for testing nested map function"""

    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2),
    ])
    def test_access_nested_map(
        self,
        nested_map: Dict,
        path: Tuple[str],
        expected: Union[Dict, int]) -> None:
        """ Test access nested map function"""
        self.assertEqual(access_nested_map(nested_map, path), expected)