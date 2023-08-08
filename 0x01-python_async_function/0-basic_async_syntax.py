#!/usr/bin/env python3
"""Waits for a random number of seconds"""

import asyncio
import random


async def wait_random(max_delay: int = 10) -> float:
    """Waits for a random number of seconds."""
    random_number = random.random() * max_delay
    await asyncio.sleep(random_number)
    return random_number