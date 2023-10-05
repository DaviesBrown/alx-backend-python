#!/usr/bin/env python3
"""
100-safe_first_element
"""
from typing import Any, Optional, Sequence


def safe_first_element(lst: Sequence[Any]) -> Optional[Any]:
    """
    safe first element
    """
    if lst:
        return lst[0]
    else:
        return None
