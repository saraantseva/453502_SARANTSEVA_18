from validators import get_string, get_yes_no
from decorator import *
@timer
@logger
def calculate_numbers_and_vowels(user_str):
    """
    Count the number of digits and vowels in a string.
    
    Args:
        user_str: input string to analyze
    
    Returns:
        tuple: (digit_count, vowel_count)
    """
    n_count = 0
    v_count = 0
    VOWELS = "aeiouyAEIOUYаеёиоуыэюяАЕЁИОУЫЭЮЯ"
    NUMBER=('1234567890')
    for i in user_str:
        if i in NUMBER:
            n_count = n_count + 1
        elif i.lower() in VOWELS:
            v_count = v_count + 1
    return (n_count, v_count)

def task3():
    """
    Main function for Task 3.
    Accepts a string from the user and counts digits and vowels.
    Allows repeated execution until the user chooses to exit.
    """
    work = 1
    while work:
        try:
            user_input = get_string("Print your string: ")
            n, v = calculate_numbers_and_vowels(user_input)
            print(f"In string {n} numbers and {v} vowels")
            work = get_yes_no("Do you want to try task again?")
        except (ValueError, TypeError):
            print("Incorrect input. Try again")     