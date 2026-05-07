"""
Lab 5: NumPy arrays, mathematical and statistical operations.
Variant 18:
1. Find the minimum row sum.
2. Find the correlation coefficient between elements with even and odd indices.

Author: Student
Date: 2026-04-23
"""

import numpy as np


class MatrixAnalyzer:
    """
    A class to demonstrate NumPy capabilities:
    - array creation, indexing, slicing
    - universal functions
    - statistical functions: mean, median, var, std, corrcoef
    - variant-specific tasks: minimum row sum, correlation between even/odd index elements
    """

    def __init__(self, n: int, m: int, low: int = 0, high: int = 100):
        """
        Initialize with a random integer matrix of size n x m.

        Args:
            n: number of rows
            m: number of columns
            low: lower bound for random integers (inclusive)
            high: upper bound for random integers (exclusive)
        """
        self.n = n
        self.m = m
        # 1. Creating array with random integers
        self.matrix = np.random.randint(low, high, size=(n, m))
        print(f"Generated {n}x{m} integer matrix:\n{self.matrix}\n")
        #np.random.uniform(low, high, size)

    def demonstrate_array_creation(self):
        """Show different ways to create arrays."""
        print("=== Array creation ===")
        # from list
        a = np.array([1, 2, 3])
        print("np.array([1,2,3]) ->", a)
        # zeros, ones, full, arange, linspace
        print("np.zeros((2,3)):\n", np.zeros((2,3)))
        print("np.ones((2,3)):\n", np.ones((2,3)))
        print("np.full((2,3),7):", np.full((2,3),7))
        print("np.arange(5):", np.arange(5))
        print("np.linspace(0,1,5):", np.linspace(0,1,5))
        # identity matrix
        print("np.eye(3):\n", np.eye(3))
        print()

    def demonstrate_indexing_slicing(self):
        """Show indexing and slicing of the matrix."""
        print("=== Indexing and slicing ===")
        print("First row:", self.matrix[0, :])
        print("First column:", self.matrix[:, 0])
        print("Submatrix (rows 1..2, cols 1..2):\n", self.matrix[1:3, 1:3])
        # Boolean indexing
        mask = self.matrix > 50
        print("Elements > 50:", self.matrix[mask])
        print()

    def demonstrate_universal_functions(self):
        """Show universal (element-wise) functions."""
        print("=== Universal functions ===")
        print("Square root (element-wise):\n", np.sqrt(self.matrix))
        print("Exponential (element-wise):\n", np.exp(self.matrix[:2, :2]))
        print("Trigonometric sin:\n", np.sin(self.matrix[:2, :2]))
        # Comparison
        print("Matrix > 50:\n", self.matrix > 50)
        print()

    def statistical_summary(self):
        """Compute and print mean, median, variance, std deviation."""
        print("=== Statistical operations ===")
        flat = self.matrix.flatten()
        cor1 = np.array([1, 2, 3, 4, 5])
        cor2 = np.array([1, 2, 3, 4, 5])
        print(f"Mean  : {np.mean(flat):.3f}")
        print(f"Median: {np.median(flat):.3f}")
        print(f"Corrcoef: {np.corrcoef(cor1, cor2)}")
        print(f"Variance : {np.var(flat):.3f}")
        print(f"Std dev  : {np.std(flat):.3f}")
        print()

    def min_row_sum(self) -> float:
        """
        Find the minimum value among the sums of all rows.
        """
        row_sums = np.sum(self.matrix, axis=1)
        print("Row sums:", row_sums)
        min_sum = np.min(row_sums)
        print(f"Minimum row sum: {min_sum}")
        return min_sum

    def correlation_even_odd_indices(self) -> float:
        """
        Compute correlation between elements with even and odd indices.
        We flatten the matrix row‑wise and split into two vectors:
        - elements at even positions (0,2,4,...)
        - elements at odd positions (1,3,5,...)
        Then compute Pearson correlation coefficient.
        """
        flat = self.matrix.flatten()
        even_elements = flat[0::2] 
        odd_elements  = flat[1::2]   

        # Ensure both vectors have the same length
        # If sizes differ, we truncate to the smaller length
        min_len = min(len(even_elements), len(odd_elements))
        even_elements = even_elements[:min_len]
        odd_elements  = odd_elements[:min_len]

        if min_len < 2:
            print("Not enough data to compute correlation.")
            return np.nan

        corr_matrix = np.corrcoef(even_elements, odd_elements)
        # corr_matrix is [[1, r], [r, 1]]
        correlation = corr_matrix[0, 1]
        print(f"Correlation between even‑indexed and odd‑indexed elements: {correlation:.4f}")
        return correlation
    
    def run_all_demonstrations(self):
        """Run all demonstrations and the two specific tasks."""
        self.demonstrate_array_creation()
        self.demonstrate_indexing_slicing()
        self.demonstrate_universal_functions()
        self.statistical_summary()
        print("=== Variant 18 specific tasks ===")
        self.min_row_sum()
        self.correlation_even_odd_indices()


def task5():
    """Main entry point: create matrix and run analysis."""
    # Parameters for the matrix 
    rows = 4
    cols = 5
    print(f"Creating a {rows}x{cols} matrix of random integers (0..99).")
    analyzer = MatrixAnalyzer(rows, cols, low=0, high=100)
    analyzer.run_all_demonstrations()


if __name__ == "__main__":
    task5()