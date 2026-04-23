"""
Module: main.py
Lab 4: Standard Data Types, Collections, Functions, Modules
Task: Interactive menu for 5 different tasks
Var: 18
Version: 1.0
Author: Daria Sarantseva
Date: 2026-04-23

"""
from validators.validators import get_yes_no, get_int, print_all_tasks
from task1.serializer import task1 
from task2.text_analayzer import task2
from task3.asin_calculator import task3
from task4.figure import task4
from task5.matrix_np import task5
from task6.task6_a import task6_a
from task6.task6_b import task6_b

work = 1
while(work):
    print_all_tasks()
    task_number = get_int("Please, select task you want to check: ",1,6)
    match task_number:        
        case 1:
            pass
            task1()
        case 2:
        #C:\Users\darya\Desktop\igi\453502_SARANTSEVA_18\IGI\LR4\task2\data\input2.txt
            task2()
            
        case 3:
            task3()
 
        case 4:
            task4()

        case 5:
            task5()
        case 6:
            task6_a()
            task6_b()
  
    work = get_yes_no("Do you want to continue?")