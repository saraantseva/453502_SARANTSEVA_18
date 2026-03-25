"""
Lab 3: Standart Data Types, Collections, Functions, Modules
Var: 18
Version: 1.0
Author: Daria Sarantseva
Date: 2026-03-25

"""
from validators import get_yes_no, get_int, print_all_tasks
from task1 import task1
from task2 import task2
from task3 import task3
from task4 import task4
from task5 import task5

work = 1
while(work):

    print_all_tasks()
    task_number = get_int("Please, select task you want to check: ",1,5)
    try:
        match task_number:        
            case 1:
                task1()
            case 2:
                task2()
            case 3:
                task3()
            case 4:
                task4()
            case 5:
                task5()
    except:
        print("govno")
    finally:
        work = get_yes_no("Do you want to continue?")
