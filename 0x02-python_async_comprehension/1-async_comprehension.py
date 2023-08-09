#!/usr/bin/env python3
""" Task 1. Async Comprehensions """

import asyncio
from typing import List

async_generator = __import__('0-async_generator').async_generator


async def async_comprehension() -> List[float]:
    """ Collects ten(10) random numbers using async comprehensions
        using async_generator function in 0-async_generator.py
    """
    return [j async for j in async_generator()]
