"""
Description:
This module contains classes for phonebook management.
- Person: Represents a person with personal information
- Phonebook: Manages collection of Person objects with CSV/Pickle serialization
"""
from validators.validators import get_input, get_string, get_yes_no, get_int
from datetime import date
from task1.mixins import PickleMixin, CSVMixin

class Person:
    """Friend in phonebook"""
    
    def __init__(self, surname: str, name: str, second_name: str, birth_date: date):
        self.surname = surname
        self.name = name
        self.second_name = second_name
        self.birth_date = birth_date
    
    def to_dict(self) -> dict:
        """
        Convert Person object to dictionary for serialization.
        
        Returns:
            dict: {'surname': 'Ivanov', 'name': 'I', 'second_name': 'I', 'birth_date': '1995-05-15'}
        """
        return {
            'surname': self.surname,
            'name': self.name,
            'second_name': self.second_name,
            'birth_date': self.birth_date.isoformat()
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Person':
        """
        Create Person object from dictionary.
        
        Args:
            data: dict with keys 'surname', 'name', 'second_name', 'birth_date'
        
        Returns:
            Person object
        """
        birth_date = date.fromisoformat(data['birth_date'])
        return cls(
            data['surname'],
            data['name'],
            data['second_name'],
            birth_date
        )

    @staticmethod
    def input_birth_date(message="Enter date of birth") -> date:
        """
        Static method to get date of birth from user input.
        Returns datetime.date object.
        """
        def parse_date(date_str: str) -> date:
            try:
                return date.fromisoformat(date_str)
            except ValueError:
                raise ValueError("Use YYYY-MM-DD format")
        
        def validate_date(d: date) -> bool:
            if d > date.today():
                print("Birth date cannot be in the future")
                return False
            if d.year < 1900:
                print("Year must be >= 1900")
                return False
            return True
        
        return get_input(
            message + " (YYYY-MM-DD): ",
            parse_date,
            validate_date,
            "Please enter a valid date (YYYY-MM-DD)"
        )
    
    @classmethod
    def from_input(cls) -> 'Person':
        """Create Person object from user input"""
        surname = get_string("Enter surname: ", allow_empty=False)
        name = get_string("Enter name: ", allow_empty=False)
        second_name = get_string("Enter second name: ", allow_empty=False)
        birth_date = cls.input_birth_date()
        return cls(surname, name, second_name, birth_date)
    

    
    def get_full_name(self) -> str:
        """Return full name with initials"""
        name_init = self.name[0] if self.name else ""
        sec_init = self.second_name[0] if self.second_name else ""
        return f"{self.surname} {name_init}.{sec_init}."
    
    def get_age_this_year(self) -> int:
        """Calculate age this year"""
        today = date.today()
        age = today.year - self.birth_date.year
        if (today.month, today.day) < (self.birth_date.month, self.birth_date.day):
            age -= 1
        return age
    
    def __str__(self) -> str:
        return f"{self.get_full_name()}: {self.birth_date.strftime('%d.%m.%Y')}"
    
    def __repr__(self) -> str:
        return f"Person('{self.surname}', '{self.name}', '{self.second_name}', '{self.birth_date}')"
    
    def __eq__(self, other) -> bool:
        """Compare two persons by surname and name"""
        if not isinstance(other, Person):
            return False
        return self.surname == other.surname and self.name == other.name
    


class Phonebook(CSVMixin, PickleMixin):
    """
    Phonebook that stores list of Person objects.
    
    Supports:
    - Adding persons
    - Finding by age
    - Saving/loading to CSV and Pickle formats
    """
    def __init__(self):
        self._persons = []
    
    def add(self, person: Person) -> None:
        self._persons.append(person)
    
    def add_from_input(self) -> None:
        person = Person.from_input()
        self._persons.append(person)
        print(f"Added: {person}")
    
    def print_all(self) -> None:
        if not self._persons:
            print("Phonebook is empty")
            return
        
        print(f"\nPhonebook ({len(self._persons)} persons):")
        for i, person in enumerate(self._persons, 1):
            age = person.get_age_this_year()
            print(f"{i}. {person} (turns {age} this year)")
    
    def find_by_age_this_year(self, age: int):
        return [p for p in self._persons if p.get_age_this_year() == age]
    
    def print_found_by_age(self, age: int) -> None:
        result = self.find_by_age_this_year(age)
        
        if not result:
            print(f"No persons found who turn {age} this year")
        else:
            print(f"\nPersons who turn {age} this year ({len(result)} found):")
            for person in result:
                print(f"  {person}")
    
    def save_to_csv(self, filename: str) -> None:
        """Save all persons to CSV"""
        if not self._persons:
            print("No data to save")
            return
        
        data = [p.to_dict() for p in self._persons]
        super().save_to_csv(data, filename)  
    
    def load_from_csv(self, filename: str) -> None:
        """Load persons from CSV (replaces current data)"""
        data = super().load_from_csv(filename)  
        self._persons = [Person.from_dict(item) for item in data]
        print(f"Loaded {len(self._persons)} persons from {filename}")
    
    def save_to_pickle(self, filename: str) -> None:
        """Save all persons to Pickle"""
        if not self._persons:
            print("No data to save")
            return
        
        data = [p.to_dict() for p in self._persons]
        super().save_to_pickle(data, filename) 
    
    def load_from_pickle(self, filename: str) -> None:
        """Load persons from Pickle (replaces current data)"""
        data = super().load_from_pickle(filename)  
        self._persons = [Person.from_dict(item) for item in data]
        print(f"Loaded {len(self._persons)} persons from {filename}")
