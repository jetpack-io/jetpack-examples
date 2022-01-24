import random
import time
from jetpack import jetroutine

# Diamond Example:#

###################
#      A
#    /  \
#  B     C
#   \   /
#     D
################


@jetroutine
async def flip_coin(label: str) -> str:
    flip = "heads" if random.randint(0, 1) == 0 else "tails"
    time.sleep(1)
    print(f'For Job {label}: {flip}')
    time.sleep(1)
    return flip
