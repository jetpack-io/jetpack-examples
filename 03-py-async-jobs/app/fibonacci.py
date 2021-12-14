import asyncio
from typing import Tuple
from jetpack import function

# Note: Please do not run with n > 6!!
@function
async def fibonacci(n: int) -> int:
    print("Fibonacci called!")
    if n < 0:
        print("Incorrect input")
        raise ValueError
    # First Fibonacci number is 0
    elif n == 0:
        return 0
    # Second Fibonacci number is 1
    elif n == 1:
        return 1
    else:
        r: Tuple[int, int] = await asyncio.gather(
            fibonacci(n - 1), 
            fibonacci(n - 2)
        )
        return r[0] + r[1]
