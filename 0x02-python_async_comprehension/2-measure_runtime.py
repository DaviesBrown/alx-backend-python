#!/usr/bin/env python3
"""
measure runtime
"""
import asyncio
import time
async_comprehension = __import__('1-async_comprehension').async_comprehension


async def measure_runtime() -> float:
    start = time.perf_counter()
    await asyncio.gather(async_comprehension())
    finish = time.perf_counter() - start
    return finish
