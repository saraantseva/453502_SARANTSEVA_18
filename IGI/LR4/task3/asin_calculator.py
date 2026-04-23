"""
Lab 4 : Taylor series for arcsin(x) with statistics and plotting.
Date: 2026-04-23
Version: 2.0
"""

import math
import matplotlib.pyplot as plt
import os

DATA_DIR = os.path.join(os.getcwd(), "task3", "data")
PLOT_FILE = os.path.join(DATA_DIR, "arcsin_plot.png")


class FunctionCalculator:
    def __init__(self, x: float, eps: float):
        self.__x = x
        self.__eps = eps

    @property
    def x(self) -> float:
        return self.__x

    @x.setter
    def x(self, x: float):
        self.__x = x

    @property
    def eps(self) -> float:
        return self.__eps

    @eps.setter
    def eps(self, eps: float):
        self.__eps = eps

    def series_term(self, n: int, x: float) -> float:
        """Calculate n-th term of Taylor series for arcsin(x)"""
        try:
            numerator = math.factorial(2 * n) * (x ** (2 * n + 1))
            denominator = (4 ** n) * (math.factorial(n) ** 2) * (2 * n + 1)
            return numerator / denominator
        except OverflowError:
            return float('inf')

    def recalc_func(self, x: float) -> float:
        """Calculate arcsin(x) using Taylor series"""
        if abs(x) > 1:
            return float('nan')

        n = 0
        term = self.series_term(n, x)
        total = term

        while abs(term) > self.__eps:
            n += 1
            term = self.series_term(n, x)
            total += term

        return total

    def __get_prec(self, x: float) -> int:
        """Get number of terms used"""
        if abs(x) > 1:
            return 0

        n = 0
        term = self.series_term(n, x)

        while abs(term) > self.__eps:
            n += 1
            term = self.series_term(n, x)

        return n + 1



    def print_table(self, x_arr, values, true_values, n_arr):
        """Print formatted table to console"""
        print("\n" + "=" * 85)
        print(f"{'x':>8} | {'n':>4} | {'Taylor':>12} | {'math.asin':>12} | {'error':>12}")
        print("=" * 85)
        for i in range(len(x_arr)):
            err = abs(values[i] - true_values[i])
            print(f"{x_arr[i]:>8.4f} | {n_arr[i]:>4} | {values[i]:>12.8f} | {true_values[i]:>12.8f} | {err:>12.2e}")
        print("=" * 85)


    def plot_graphs(self):
        count_of_points = 20
        values = []
        true_values = []
        n_arr = []
        x_arr = []

        for i in range(count_of_points + 1):
            x = -1.0 + i * (2.0 / count_of_points)
            if abs(x) <= 1:
                value = self.recalc_func(x)
                true_value = math.asin(x)
                values.append(value)
                true_values.append(true_value)
                n_arr.append(self.__get_prec(x))
                x_arr.append(x)

        # Print table to console
        self.print_table(x_arr, values, true_values, n_arr)

        # Plot only graph (without table inside)
        fig, ax = plt.subplots(figsize=(10, 6))

        ax.plot(x_arr, true_values, 'r--', linewidth=2, label="math.asin(x)")
        ax.plot(x_arr, values, 'b-', linewidth=2, label="Taylor series")

        ax.set_xlabel('x')
        ax.set_ylabel('arcsin(x)')
        ax.set_title(f'arcsin(x) approximation (ε = {self.__eps:.1e})')
        ax.legend()
        ax.grid(True, linestyle=':', alpha=0.7)

        if not os.path.exists(DATA_DIR):
            os.makedirs(DATA_DIR)

        plt.savefig(PLOT_FILE, dpi=150, bbox_inches='tight')
        print(f"Plot saved as '{PLOT_FILE}'")
        plt.show()

def task3():

    print("ARC SIN SERIES ANALYSIS (Taylor vs math.asin)")

    while True:
        try:
            eps = float(input("Enter the required precision: "))
            if eps <= 0 or eps > 1:
                print("Enter a value between 0 and 1")
                continue
            break
        except ValueError:
            print("Enter a valid float value")

    calc = FunctionCalculator(0.5, eps)
    calc.plot_graphs()


def main():
    task3()


if __name__ == "__main__":
    main()