# DRAFT
from random import random

def p_change(x: int, y: int) -> float:
    p = 0.6
    return p


def p_up_stay_down(x: int, y: int, summit: int) -> (float, float, float):
    if y < summit:
        return 0.2, 0.2, 0.6
    else:
        return 0.6, 0.2, 0.2


def go_up_stay_down(x: int, y: int, last: int,summit: int) -> int:
    if random() > p_change(x, y):
        return last
    else:
        r2 = random()
        d, s, u = p_up_stay_down(x, y,summit)
        if r2 < d:
            return -1
        elif r2 < s:
            return 0
        else:
            return 1
