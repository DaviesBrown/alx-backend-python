#!/usr/bin/env python3
"""
task wait random
"""
import asyncio
import random
from typing import List
task_wait_random = __import__('3-tasks').task_wait_random


async def task_wait_n(n: int, max_delay: int) -> List[float]:
    """
    waits for n task random
    """
    list_of_delays = await asyncio.gather(
        *((task_wait_random(max_delay)) for i in range(n)))

    return sorted(list_of_delays)
