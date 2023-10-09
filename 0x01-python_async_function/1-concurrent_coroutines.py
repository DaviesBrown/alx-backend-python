#!/usr/bin/python3
"""
concurrent coroutines
"""
import asyncio
from typing import List
wait_random = __import__('0-basic_async_syntax').wait_random


async def wait_n(n: int, max_delay: int) -> List[float]:
    """
    waits for a delay amount and returns the list of n delay amount
    """
    list_of_delays = await asyncio.gather(*((wait_random(max_delay)) for i in range(n)))

    return sorted(list_of_delays)
