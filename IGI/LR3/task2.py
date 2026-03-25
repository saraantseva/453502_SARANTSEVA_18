from validators import get_int, get_yes_no


def sum_last_digits(stop=18) -> int:
    """
    Sum the last digits of entered numbers until stop value is entered.
    
    Args:
        stop: number that stops the input (default 18)
    
    Returns:
        int: sum of last digits of all entered numbers (excluding stop value)
    """
    total = 0
    
    while True:
        x = get_int(f"Enter integer (enter {stop} to stop): ")
        
        if x == stop:
            break
        
        last_digit = abs(x) % 10
        total = total + last_digit
        print(f"Last digit: {last_digit}, Total: {total}")
    
    return total


def task2(stop=18) -> int:
    """
    Task 2 main function with retry functionality.
    
    Args:
        stop: number that stops the input (default 18)
    
    Returns:
        int: sum of last digits
    """
    work = 1
    final_result = 0
    
    while work:
        try:
            result = sum_last_digits(stop)
            print("Sum result: ", result)
            final_result = result
            
        except (ValueError, TypeError):
            print("Incorrect input. Try again")
        
        work = get_yes_no("Do you want to try task again?")
    
    return final_result