#!/usr/bin/env python3
"""
9-element_length
"""
from typing import Any, Iterable, List, Sequence, Tuple


def element_length(lst: Iterable[Sequence]) -> List[Tuple[Sequence, int]]:
    """
    takes a iterable of sequence and returns a list
    of tuple containing the sequence and length of seq
    """
    return [(i, len(i)) for i in lst]
