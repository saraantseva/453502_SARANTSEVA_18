"""
Lab 6: Pandas Basics - Loan Prediction Dataset.
Task A: Series, DataFrame, indexing, display.
Variant 18: Create DataFrame from dict with custom indices.
Author: Student
Date: 2026-04-23
"""

import pandas as pd
import numpy as np
import os


class PandasAnalyzer:
    """
    A class to demonstrate basic Pandas capabilities:
    - Series creation and access (.loc/.iloc)
    - DataFrame creation from dict with custom index
    - Loading and exploring the Loan Prediction dataset
    """

    def __init__(self, dataset_path: str = "train_u6lujuX_CVtuZ9i.csv"):
        self.dataset_path = dataset_path
        self.df = None
        self.load_or_create_dataset()

    def load_or_create_dataset(self):
        """Load real dataset if exists, otherwise create a demo DataFrame."""
        if os.path.exists(self.dataset_path):
            self.df = pd.read_csv(self.dataset_path)
            print(f" Loaded real dataset from '{self.dataset_path}'. Shape: {self.df.shape}")
        else:
            print(f" File '{self.dataset_path}' not found. Creating demo data from the task description.")
            # Create demo data based on the Loan Prediction problem
            data = {
                'ApplicantIncome': [5000, 6000, 7500, 4200, 8000, 3500],
                'LoanAmount': [150, 200, 180, 120, 250, 90],
                'Gender': ['Male', 'Female', 'Male', 'Male', 'Female', 'Male'],
                'Loan_Status': ['Y', 'Y', 'N', 'Y', 'N', 'Y']
            }
            self.df = pd.DataFrame(data)
            print("Demo DataFrame created.")

    # ------------------------------------------------------------------
    # Series demonstrations (points 2,3,4,5)
    # ------------------------------------------------------------------
    def demonstrate_series(self):
        """Create Series, display, and access elements via .loc and .iloc."""
        print("\n" + "=" * 60)
        print("2-5. Pandas Series: creation, display, .loc, .iloc")
        print("=" * 60)

        # Create Series from list
        incomes = [5000, 6000, 7500, 4200]
        series_incomes = pd.Series(incomes, name='ApplicantIncome', index=['a', 'b', 'c', 'd'])
        print("1) Series created from list with custom index:")
        print(series_incomes)

        # Display (using print)
        print("\n2) Displaying Series (same as print):")
        print(series_incomes.to_string())

        # Access via .loc (label-based)
        print("\n3) Access using .loc['b']:")
        print(f"   Value: {series_incomes.loc['b']}")

        # Access via .iloc (position-based)
        print("\n4) Access using .iloc[2]:")
        print(f"   Value: {series_incomes.iloc[2]}")

        # Slicing
        print("\n5) Slicing .iloc[1:3]:")
        print(series_incomes.iloc[1:3])

    # ------------------------------------------------------------------
    # DataFrame from dictionary with custom index (task variant)
    # ------------------------------------------------------------------
    def create_dataframe_with_custom_index(self):
        """Create a DataFrame from a dictionary and set specific index."""
        print("\n")
        print("6. Object DataFrame. Creation from dict with custom indices (variant 18)")
  

        data = {
            'ApplicantIncome': [5000, 6000],
            'LoanAmount': [150, 200]
        }
        df_custom = pd.DataFrame(data, index=['borrower1', 'borrower2'])
        print("DataFrame created from dictionary:")
        print(df_custom)
        print(f"\nIndex names: {df_custom.index.tolist()}")
        print(f"Columns: {df_custom.columns.tolist()}")

    def explore_dataset(self):
        """Display basic info, statistics, and first rows of the dataset."""
        print("\n")
        print("Exploring the Loan Prediction dataset")


        if self.df is None:
            print("No data to explore.")
            return

        print("First 5 rows (head):")
        print(self.df.head())

        print("\nLast 3 rows (tail):")
        print(self.df.tail(3))

        print("\nDataset info (dtypes, non-null counts):")
        self.df.info()

        print("\nStatistical summary for numerical columns:")
        print(self.df.describe())

        # Check for missing values
        missing = self.df.isnull().sum()
        if missing.sum() > 0:
            print("\nMissing values per column:")
            print(missing[missing > 0])

    def run_all(self):
        """Execute all demonstration methods in order."""
        self.demonstrate_series()
        self.create_dataframe_with_custom_index()
        self.explore_dataset()


def task6_a():
    """
    Main function for Lab 6, Task A.
    Demonstrates Pandas Series and DataFrame capabilities,
    including the variant-specific DataFrame creation.
    """
    print("\n" + "-" * 70)
    print("Lab 6 part A: Pandas Basics (Loan Prediction Dataset)")
    print("Variant 18: Create DataFrame with custom indices")
    print("-" * 70)

    # If the dataset file is in a different location, change the path here
    analyzer = PandasAnalyzer("train_u6lujuX_CVtuZ9i.csv")
    analyzer.run_all()


if __name__ == "__main__":
    task6_a()