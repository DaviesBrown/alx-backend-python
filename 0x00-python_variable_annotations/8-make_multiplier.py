#!/usr/bin/env python3
"""
8-make_multiplier
"""


from typing import Callable


def make_multiplier(multiplier: float) -> Callable[[float], float]:
    """
    make_multiplier that takes a float multiplier as argument and returns
    a function that multiplies a float by multiplier.
    """
    return lambda f: f * multiplier
