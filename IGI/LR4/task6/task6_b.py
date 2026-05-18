"""
Lab 6, Part B: Statistical analysis and indexing on Loan Prediction dataset.
Task: Determine how many times the average ApplicantIncome of borrowers with
      max LoanAmount exceeds that of borrowers with min LoanAmount.
Author: Student
Date: 2026-04-23
"""

import pandas as pd
import numpy as np
import os


class LoanDataAnalyzer:
    """
    Perform basic DataFrame info, indexing, and statistical comparisons.
    """

    def __init__(self, file_path: str = "train_u6lujuX_CVtuZ9i.csv"):
        self.file_path = file_path
        self.df = None
        self._load_or_create_data()

    def _load_or_create_data(self):
        """Load real dataset or create a realistic demo DataFrame."""
        if os.path.exists(self.file_path):
            self.df = pd.read_csv(self.file_path)
            print(f"Loaded dataset from '{self.file_path}'. Shape: {self.df.shape}")
        else:
            print(f"File '{self.file_path}' not found. Creating a demo dataset.")
            # Create demo data similar to Loan Prediction problem
            np.random.seed(42)
            n = 100
            data = {
                'ApplicantIncome': np.random.randint(2000, 12000, n),
                'LoanAmount': np.random.randint(50, 400, n),
                'Gender': np.random.choice(['Male', 'Female'], n),
                'Loan_Status': np.random.choice(['Y', 'N'], n, p=[0.7, 0.3])
            }
            self.df = pd.DataFrame(data)
            # Introduce some realistic correlation: higher income -> higher loan amount
            self.df['LoanAmount'] = self.df['LoanAmount'] + (self.df['ApplicantIncome'] // 1000) * 20
            self.df['LoanAmount'] = self.df['LoanAmount'].clip(50, 600)
            print("Demo DataFrame created with 100 rows.")


    def dataframe_info(self):
        """Display comprehensive information about the DataFrame."""
        print("\n")
        print("DATAFRAME INFORMATION")
        print(f"Shape: {self.df.shape} (rows, columns)")
        print(f"Columns: {self.df.columns.tolist()}")
        print(f"Index: {self.df.index}")
        print("\nData types:")
        print(self.df.dtypes)
        print("\nFirst 5 rows:")
        print(self.df.head())
        print("\nStatistical summary (numerical columns):")
        print(self.df.describe())
        print("\nMissing values per column:")
        print(self.df.isnull().sum())

    def compare_income_by_loan_extremes(self) -> float:
        """
        Calculate the ratio:
        mean(ApplicantIncome where LoanAmount == max) /
        mean(ApplicantIncome where LoanAmount == min)
        Returns the ratio rounded to two decimal places.

        во сколько раз средний доход (ApplicantIncome) заемщиков 
            c максимальным размером кредита (LoanAmount = max) 
            больше, чем y заемщиков c минимальным размером кредита. 
        """
        
        # Find max and min LoanAmount
        max_loan = self.df['LoanAmount'].max()
        min_loan = self.df['LoanAmount'].min()
        print(f"\nMax LoanAmount: {max_loan}")
        print(f"Min LoanAmount: {min_loan}")

        # Subset for max and min loan amounts
        borrowers_max = self.df[self.df['LoanAmount'] == max_loan]
        borrowers_min = self.df[self.df['LoanAmount'] == min_loan]

        # Compute mean ApplicantIncome
        mean_income_max = borrowers_max['ApplicantIncome'].mean()
        mean_income_min = borrowers_min['ApplicantIncome'].mean()
        print(f"Mean ApplicantIncome for borrowers with max loan: {mean_income_max:.2f}")
        print(f"Mean ApplicantIncome for borrowers with min loan: {mean_income_min:.2f}")

        # Avoid division by zero
        if mean_income_min == 0:
            print("Warning: Minimum mean income is zero. Cannot compute ratio.")
            return float('inf')

        ratio = mean_income_max / mean_income_min
        print(f"Ratio (max/min): {ratio:.4f}")
        return round(ratio, 2)


    def additional_stats(self):
        """Demonstrate other statistical operations."""
        print("\n")
        print("ADDITIONAL STATISTICS")
        # Correlation between ApplicantIncome and LoanAmount
        corr = self.df['ApplicantIncome'].corr(self.df['LoanAmount'])
        print(f"Correlation between ApplicantIncome and LoanAmount: {corr:.4f}")
        # Group by Loan_Status (if exists) and show mean income
        if 'Loan_Status' in self.df.columns:
            print("\nMean ApplicantIncome by Loan_Status:")
            print(self.df.groupby('Loan_Status')['ApplicantIncome'].mean())


    def run_analysis(self):
        """Execute all required steps for part B."""
        self.dataframe_info()
        ratio = self.compare_income_by_loan_extremes()
        print("\n" + "-" * 60)
        print(f"RESULT: The average income for borrowers with max loan is {ratio} times "
              f"higher than for borrowers with min loan.")
        print("-" * 60)


def task6_b():
    """
    Main function for Lab 6, Part B.
    Demonstrates DataFrame information retrieval and statistical comparison.
    """
    print("\n" + "-" * 70)
    print("# Lab 6 – Part B: Statistical Analysis (Loan Prediction Dataset)")
    print("# Task: Compare average ApplicantIncome for max vs min LoanAmount")
    print("-" * 70)

    # Initialize analyzer (will try to load real dataset or create demo)
    analyzer = LoanDataAnalyzer("train_u6lujuX_CVtuZ9i.csv")
    analyzer.run_analysis()


if __name__ == "__main__":
    task6_b()