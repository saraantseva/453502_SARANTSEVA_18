"""
    This module implements the calculation of arcsin(x) function
    using Taylor series expansion with specified precision.
    The program compares the result with math.asin() function.
"""

import math
from validators import get_float, get_yes_no

MAX_ITERATION_COUNT = 500

def arcsin_Taylor(x, eps):
    """
    Calculate arcsin(x) using Taylor series expansion.
    
    Args:
        x: argument value (must be in range [-1, 1])
        eps: required calculation precision
    
    Returns:
        None: results are printed via print_result function
    
    Raises:
        TimeoutError: when iteration count exceeds MAX_ITERATION_COUNT
    """
    try:
        term_index = 0           
        term = series_member(term_index, x)
        total = term
        terms_used = 1       
        
        while abs(term) > eps:
            term_index += 1
            if term_index > MAX_ITERATION_COUNT:
                raise TimeoutError
            term = series_member(term_index, x)
            total += term
            terms_used += 1
        
        print_result(x, terms_used, eps, total)
    except TimeoutError:
        print(f"Big iteration count (more than {MAX_ITERATION_COUNT}).")


def series_member(n, x) -> float:
    """
    Calculate the n-th term of the Taylor series for arcsin(x).
    
    Formula: a_n = (2n)! * x^(2n+1) / (4^n * (n!)^2 * (2n+1))
    
    Args:
        n: term index (0-based)
        x: argument value
    
    Returns:
        float: value of the n-th term
        float('inf'): in case of overflow
    """
    try:
        a = math.factorial(2 * n) * (x ** (2 * n + 1))
        b = (4 ** n) * (math.factorial(n) ** 2) * (2 * n + 1)
        return a / b
    except OverflowError:
        return float('inf')  


def task1():
    """
    Main interactive interface for Task 1.
    
    Provides user input handling and allows repeated execution
    of the arcsin calculation with different parameters.
    """
    work = 1
    while work:
        try:
            x = get_float("Input x value: ", min_val=-1, max_val=1)
            eps = get_float("Input accuracy of calculations: ", min_val=1e-10, max_val=1.)
            arcsin_Taylor(x, eps)
        except (ValueError, TypeError):
            print("Incorrect input. Try again")
        work = get_yes_no("Do you want to try task again?")


def print_result(x, n, eps, total):
    """
    Print formatted results in a table.
    
    Displays comparison between Taylor series calculation
    and math.asin() function result.
    
    Args:
        x: argument value
        n: number of terms used in series
        eps: calculation precision
        total: calculated value from Taylor series
    """
    true_value = math.asin(x)
    
    print("┌───────────┬─────────┬───────────────┬───────────────┬────────────┐")
    print("│     x     │    n    │      F(x)     │   Math F(x)   │    eps     │")
    print("├───────────┼─────────┼───────────────┼───────────────┼────────────┤")
    print(f"│ {x:>+8.6f} │{n:>6}   │ {total:>+12.8f}  │ {true_value:>+12.8f}  │ {eps:>10.2e} │")
    print("└───────────┴─────────┴───────────────┴───────────────┴────────────┘")
    
    print(f"\n→ Terms used: {n}")
    print(f"→ Error: {abs(true_value - total):.2e}")

