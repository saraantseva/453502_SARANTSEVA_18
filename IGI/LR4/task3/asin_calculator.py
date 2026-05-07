"""
Lab 4 : Taylor series for arcsin(x) with statistics and plotting.
Date: 2026-04-23
Version: 2.0
"""

from task3.models import FunctionCalculator

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
    
    x_values = [-0.9, -0.5, 0, 0.3, 0.7, 0.9]
    results = [calc.recalc_func(x) for x in x_values]
    calc.print_statistics(results)




def main():
    task3()


if __name__ == "__main__":
    main()