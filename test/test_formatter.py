# -*- coding: utf-8 -*-
"""
:author: Pawel Chomicki
"""
import unittest
from datetime import datetime

from pytest_spec.formatter import format_in_safe


class TestFormatInSafe(unittest.TestCase):
    def test_it_returns_formatted_string_just_same_as_format_function(self):
        result = format_in_safe('{val}', val=10)
        self.assertEqual(result, '10')

        result = format_in_safe('{val:.2%}', val=0.1)
        self.assertEqual(result, '10.00%')

        result = format_in_safe('{val:,}', val=1234567890)
        self.assertEqual(result, '1,234,567,890')

        result = format_in_safe('{val:%Y-%m-%d %H:%M:%S}', val=datetime(2010, 7, 4, 12, 15, 58))
        self.assertEqual(result, '2010-07-04 12:15:58')

    def test_it_ignores_unspecified_placeholder(self):
        result = format_in_safe('{val}', value=10)
        self.assertEqual(result, '{val}')

    def test_it_ignores_unspecified_placeholder_even_if_it_has_spec(self):
        result = format_in_safe('{val:.2%}', value=10)
        self.assertEqual(result, '{val:.2%}')

