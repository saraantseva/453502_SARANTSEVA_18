
from task1.models import Phonebook
from task1.mixins import CSVMixin, PickleMixin
from validators.validators import get_input, get_string, get_yes_no, get_int
import os

# Test data for CSV
CSV_TEST_DATA = [
    {"surname": "Ivanov", "name": "I", "second_name": "I", "birth_date": "1995-05-15"},
    {"surname": "Petrov", "name": "P", "second_name": "P", "birth_date": "1990-03-10"},
    {"surname": "Sidorov", "name": "S", "second_name": "S", "birth_date": "2000-07-20"},
]

# Test data for Pickle
PICKLE_TEST_DATA = [
    {"surname": "Kuznetsova", "name": "K", "second_name": "K", "birth_date": "1995-11-05"},
    {"surname": "Smirnov", "name": "S", "second_name": "S", "birth_date": "1988-01-25"},
    {"surname": "Volkov", "name": "V", "second_name": "V", "birth_date": "1992-09-30"},
]

# Default files
default = os.curdir  
CSV_DEFAULT = os.path.join(default,"task1", "data", "phonebook.csv")
PICKLE_DEFAULT = os.path.join(default,"task1", "data", "phonebook.pkl")

def load_test_data(phonebook: Phonebook) -> None:
    """Load test data into phonebook (only if empty)"""
    if len(phonebook._persons) == 0:
        phonebook.load_from_csv(CSV_DEFAULT)
        
        if len(phonebook._persons) == 0:
            csv_mixin = CSVMixin()
            pickle_mixin = PickleMixin()
            csv_mixin.save_to_csv(CSV_TEST_DATA, CSV_DEFAULT)
            pickle_mixin.save_to_pickle(PICKLE_TEST_DATA, PICKLE_DEFAULT)
            phonebook.load_from_csv(CSV_DEFAULT)

def task1():
    """Main function for Lab 18 - Phonebook (Birthday Book)"""
    
    phonebook = Phonebook()
    load_test_data(phonebook)

   # phonebook.load_from_csv(CSV_DEFAULT)  
    work = 1
    while work:
        print("PHONEBOOK (BIRTHDAY BOOK)")
        print("-" * 30)
        print("1. Add new person")
        print("2. View all persons")
        print("3. Find persons by age")
        print("4. Save to CSV")
        print("5. Load from CSV")
        print("6. Save to Pickle")
        print("7. Load from Pickle")
        print("0. Exit")

        
        choice = get_int("Your choice: ", 0, 7)
        
        match choice:
            case 1:
                phonebook.add_from_input()
            
            case 2:
                phonebook.print_all()
            
            case 3:
                age = get_int("Enter age to search: ", 0, 150)
                phonebook.print_found_by_age(age)
            
            case 4:
                phonebook.save_to_csv(CSV_DEFAULT)
            
            case 5:
                phonebook.load_from_csv(CSV_DEFAULT)
            
            case 6:
                phonebook.save_to_pickle(PICKLE_DEFAULT)
            
            case 7:
                phonebook.load_from_pickle(PICKLE_DEFAULT)
            
            case 0:
                print("Goodbye!")
                work = 0
        
        if work:
            work = get_yes_no("Do you want to continue?")

def main():
    task1()


if __name__ == "main":
    main()