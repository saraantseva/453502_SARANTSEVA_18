"""

"""

def print_all_tasks():
    print("All tasks:")
    print("task 1: Displays comparison between Taylor series calculation and math.asin() result.")
    print("task 2: Sum the last digits of entered numbers until stop value is entered.")
    print("task 3: Count the number of digits and vowels in a string.")
    print("task 4: Analyzes a fixed text.")
    print("task 5: Find max absolute element and sum of elements before the last even element.")

def get_input(message, convert, valid, error_msg):
    """
    Universal input function with validation.
    
    Args:
        message: Prompt to show user
        convert: Function to convert input (int, float, str)
        valid: Validation function that returns True if value is valid
        error_msg: Error message to show on invalid input
    """
    while True: 
        try:
            user_input = input(message)
            value = convert(user_input)

            if valid is None or valid(value):
                return value
            else:
                print(error_msg or "Incorrect input. Try again")
                
        except (ValueError, TypeError):
            print(error_msg or f"Incorrect input. Expected {convert.__name__}")


def get_int(message, min_val=None, max_val=None):
    """
    Get integer input with optional range validation.
    
    Args:
        message: Prompt to show user
        min_val: Minimum allowed value (optional)
        max_val: Maximum allowed value (optional)
    """
    def check_range(x):
        """Check if value is within range."""
        if min_val is not None and x < min_val:
            return False
        if max_val is not None and x > max_val:
            return False
        return True
    
    if min_val is not None and max_val is not None:
        error_msg = f"Invalid input. Please enter an integer between {min_val} and {max_val}."
    elif min_val is not None:
        error_msg = f"Invalid input. Please enter an integer >= {min_val}."
    elif max_val is not None:
        error_msg = f"Invalid input. Please enter an integer <= {max_val}."
    else:
        error_msg = "Invalid input. Please enter an integer."
    
    result = get_input(message, int, check_range, error_msg)
    return result


def get_float(message, min_val=None, max_val=None):
    """
    Get float input with optional range validation.
    Args:
        message: Prompt to show user
        min_val: Minimum allowed value (optional)
        max_val: Maximum allowed value (optional)
    
    """
    def check_range(x):
        if min_val is not None and x < min_val:
            return False
        if max_val is not None and x > max_val:
            return False
        return True
    
    if min_val is not None and max_val is not None:
        error_msg = f"Invalid input. Please enter a number between {min_val} and {max_val}."
    elif min_val is not None:
        error_msg = f"Invalid input. Please enter a number >= {min_val}."
    elif max_val is not None:
        error_msg = f"Invalid input. Please enter a number <= {max_val}."
    else:
        error_msg = "Invalid input. Please enter a number."
    
    result = get_input(message, float, check_range, error_msg)
    return result


def get_string(message, allow_empty=True):
    """
    Get string input with optional empty check.
    Args:
        message: Prompt to show user
        allow_empty: allow ampty string or don't
    """
    def check_not_empty(s):
        if not allow_empty and len(s.strip()) == 0:
            return False
        return True
    
    error_msg = "Input cannot be empty." if not allow_empty else None
    
    result = get_input(message, str, check_not_empty, error_msg)
    return result


def get_yes_no(message="Try again? (y/n): "):
    """
    Get yes/no answer. Returns True for yes, False for no.
    Args:
        message: Prompt to show user
    """
    def check_yes_no(answer):
        return answer.lower() in ['y', 'yes', 'n', 'no']
    
    error_msg = "Please enter y (yes) or n (no)"
    mess = message + "(y/n): "
    result = get_input(mess, str, check_yes_no, error_msg)
    return result.lower() in ['y', 'yes']
  
def try_again(func):
    res = 1
    while(res):
        func()
        res = get_yes_no("Do you want to retry?")