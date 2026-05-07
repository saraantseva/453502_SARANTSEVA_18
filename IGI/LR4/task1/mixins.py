'''
Task: Serialization mixins for CSV and Pickle formats

Description:
This module provides mixin classes for serializing and deserializing data
to/from CSV and Pickle file formats. These mixins are designed to be used
with classes that need persistent storage capabilities.
'''

import csv
import pickle

class CSVMixin:
    """CSV saver - works with list of dicts"""
    
    def save_to_csv(self, data: list, filename: str):
        """Save list of dicts to CSV"""
        if not data:
            return
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=data[0].keys())
            writer.writeheader()
            writer.writerows(data)
        print(f"Saved to {filename}")
    
    def load_from_csv(self, filename: str) -> list:
        """Load list of dicts from CSV"""
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                return list(reader)
        except FileNotFoundError:
            print(f"File {filename} not found")
            return []


class PickleMixin:
    """Pickle saver - works with list of dicts"""
    
    def save_to_pickle(self, data: list, filename: str):
        """Save list of dicts to Pickle"""
        with open(filename, 'wb') as f:
            pickle.dump(data, f)
        print(f"Saved to {filename}")
    
    def load_from_pickle(self, filename: str) -> list:
        """Load list of dicts from Pickle"""
        try:
            with open(filename, 'rb') as f:
                return pickle.load(f)
        except FileNotFoundError:
            print(f"File {filename} not found")
            return []
