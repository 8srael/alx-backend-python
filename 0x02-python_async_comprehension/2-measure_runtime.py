#!/usr/bin/env python3
"""
    Task 2. Run time for four parallel comprehensions
"""

import asyncio
import time
from importlib import import_module as async_comprehension_module

async_comprehension = async_comprehension_module('1-async_comprehension')\
                        .async_comprehension


async def measure_runtime() -> float:
    """ Measures the total execution time for wait_n(n, max_delay) """
    start_time = time.time()
    await asyncio.gather(
        *(async_comprehension() for _ in range(4))
    )
    return (time.time() - start_time)
