#!/usr/bin/env python3

"""Task 0. Async Generator"""

import asyncio
import random


async def async_generator() -> float:
    """Yields a random number between 0 and 10"""
    for _ in range(10):
        await asyncio.sleep(1)
        yield random.random() * 10
