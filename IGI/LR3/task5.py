"""
Task 5: List Processing
Find max absolute element and sum of elements before the last even element.

"""

import random
from validators import get_int, get_yes_no


def generate_random_list(size, min_val=-100, max_val=100):
    """
    Generate a list of random integers (generator function).
    
    Args:
        size: number of elements
        min_val: minimum value (inclusive)
        max_val: maximum value (inclusive)
    
    Returns:
        list: list of random integers
    """
    return [random.randint(min_val, max_val) for _ in range(size)]

def generate_numbers(size, min_val=-100, max_val=100):
    """
    Generator function using yield - yields numbers one by one.
    
    Args:
        size: number of elements
        min_val: minimum value (inclusive)
        max_val: maximum value (inclusive)
    
    Yields:
        int: random integer values one at a time
    """
    for _ in range(size):
        yield random.randint(min_val, max_val)


def input_user_list(size):
    """
    Input list elements from user.
    
    Args:
        size: number of elements
    
    Returns:
        list: list of user-entered integers
    """
    lst = []
    print(f"\nEnter {size} integer(s):")
    for i in range(size):
        value = get_int(f"  Element {i+1}: ")
        lst.append(value)
    return lst


def print_list(lst, title="Current list"):
    """
    Print list on screen.
    
    Args:
        lst: list to print
        title: title before printing
    """
    print(f"\n{title}: {lst}")


def max_abs_element(lst):
    """
    Find element with maximum absolute value.
    
    Args:
        lst: list of integers
    
    Returns:
        tuple: (max_abs_value, index)
    """
    max_val = lst[0]
    max_idx = 0
    
    for i, val in enumerate(lst):
        if abs(val) > abs(max_val):
            max_val = val
            max_idx = i
    
    return max_val, max_idx


def sum_before_last_even(lst):
    """
    Sum all elements before the last even element.
    
    Args:
        lst: list of integers
    
    Returns:
        int: sum of elements before last even element, 0 if no even or first element
    """
    last_even_idx = -1
    for i in range(len(lst) - 1, -1, -1):
        if lst[i] % 2 == 0:
            last_even_idx = i
            break
    if last_even_idx <= 0:
        return 0
    
    return sum(lst[:last_even_idx])


def process_list(lst):
    """
    Process list and print results.
    
    Args:
        lst: list of integers
    """
    print_list(lst, "Original list")
    
    max_val, max_idx = max_abs_element(lst)
    sum_before = sum_before_last_even(lst)
    
    print(f"\nResults:")
    print(f"  Maximum by absolute value: {max_val} (at index {max_idx})")
    print(f"  Sum of elements before last even: {sum_before}")


def task5(max_v=20):
    """
    Main function for Task 5.
    Provides list initialization options and processes the list.
    """
    while True:
        # Get list size.
        size = get_int(f"Enter list size (1-{max_v}): ", min_val=1, max_val=max_v)

        choice = get_yes_no("Do you want do generate list?")
        if choice == True:
            min_val = get_int("Enter minimum value: ")
            max_val = get_int("Enter maximum value: ", min_val=min_val)
            #  lst = generate_random_list(size, min_val, max_val)
            #  print_list(lst, "Generated list")
            generator = generate_numbers(size, min_val, max_val)
            lst = list(generator) 
            
            print_list(lst, "Generated list")
        else:
            lst = input_user_list(size)            

        process_list(lst)
 
        if not get_yes_no("\nDo you want to process another list?"):
            break
