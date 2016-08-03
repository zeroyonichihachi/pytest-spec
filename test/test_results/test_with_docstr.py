# -*- coding: utf-8 -*-
"""
:author: Takafumi Yamaguchi
:e-mail: tkfm.yamaguchi@gmail.com
"""
import pytest


def fibonacci(n):
    if n < 3:
        return 1

    return fibonacci(n - 1) + fibonacci(n - 2)

#
# @pytest.mark.parametrize('arg, expect', [
#     (1, 1),
#     (2, 1),
#     (10, 55),
# ])
# def test_fibonacci(arg, expect):
#     """
#     If {arg} is given, fibonacci() should return {expect}.
#     """
#     assert fibonacci(arg) == expect

@pytest.fixture
def dummy_val():
    return 10

@pytest.mark.skip(reason="This should be skipped.")
@pytest.mark.parametrize('arg', [1])
def test_skip(arg, dummy_val):
    """
    {arg} and {dummy_val} would be replaced, but {this:,} must not be replaced.
    """
    assert True

# def test_fail():
#     """
#     {this:.2%} also must not be replaced.
#     """
#     assert False
