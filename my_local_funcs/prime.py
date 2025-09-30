import math
from math import sqrt
from math import floor

def prime(n):
    max = floor(sqrt(n))
    for div in range(2, max + 1):
        if n % div == 0:
            return False #se não entar nesse if, n é um primo certeza
        return True
