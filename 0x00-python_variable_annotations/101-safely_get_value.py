#!/usr/bin/env python3
"""
101-safe;y_get_values
"""
from typing import Any, Mapping, Optional, TypeVar, Union

T = TypeVar('T')


def safely_get_value(dct: Mapping,
                     key: Any,
                     default: Optional[T] = None) -> Union[Any, T]:
    """
    safely get value
    """
    if key in dct:
        return dct[key]
    else:
        return default
