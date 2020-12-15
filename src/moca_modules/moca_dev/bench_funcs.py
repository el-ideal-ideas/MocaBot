# -- Imports --------------------------------------------------------------------------

from typing import (
    List
)
from sympy import simplify, symbols, sqrt

# -------------------------------------------------------------------------- Imports --

# -- Functions --------------------------------------------------------------------------


def fibonacci_loop(n: int) -> int:
    a, b = 0, 1
    if n == 1:
        return a
    elif n == 2:
        return b
    else:
        for _ in range(n - 2):
            a, b = b, a + b
        return b


def fibonacci_sym(n: int) -> int:
    x = symbols('x', nonnegative=True, integer=True)
    fib = 1 / sqrt(5) * (((1+sqrt(5))/2)**(n-1) - ((1-sqrt(5))/2)**(n-1))
    result = fib.subs(x, n)
    result = simplify(result)
    return result


def fibonacci_recursion(n: int) -> int:
    if n == 1:
        return 0
    elif n == 2:
        return 1
    else:
        return fibonacci_recursion(n-1) + fibonacci_recursion(n-2)


def fibonacci_list_loop(n: int) -> List[int]:
    return [fibonacci_loop(i) for i in range(1, n)]


def fibonacci_list_sym(n: int) -> List[int]:
    return [fibonacci_sym(i) for i in range(1, n)]


def fibonacci_list_recursion(n: int) -> List[int]:
    return [fibonacci_recursion(i) for i in range(1, n)]


# -------------------------------------------------------------------------- Functions --
