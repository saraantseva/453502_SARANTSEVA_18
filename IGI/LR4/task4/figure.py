"""
Lab 4: Geometric Figures (Equilateral Triangle)
Variant 18: Equilateral triangle with side length a.
Date: 2026-04-23
"""


import math
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from task4.models import EquilateralTriangle
import os
DATA_DIR = os.path.join(os.getcwd(), r"task4\data")



def get_positive_float(prompt: str, min_val: float = 0.01, max_val: float = 100.0) -> float:
    """Read and validate a positive float within given range."""
    while True:
        try:
            value = float(input(prompt))
            if value < min_val:
                print(f"Value must be at least {min_val}. Try again.")
                continue
            if value > max_val:
                print(f"Value must be at most {max_val}. Try again.")
                continue
            return value
        except ValueError:
            print("Invalid input. Please enter a number.")


def get_color() -> str:
    """Read and validate a color name (CSS4)."""
    while True:
        color_name = input("Enter color (e.g., 'red', 'blue', 'green'): ").strip()
        if color_name in mcolors.CSS4_COLORS:
            return color_name
        print(f"'{color_name}' is not a valid CSS4 color name. Try again.")


def get_caption() -> str:
    """Read a caption text for the figure."""
    return input("Enter caption text for the figure: ").strip()


def draw_triangle(triangle: EquilateralTriangle, caption: str, output_file: str = None):
    """
    Draw the equilateral triangle, fill with its color, add caption,
    and optionally save to file.
    """
    side = triangle.side
    color = triangle.color.color

    # Vertices of the equilateral triangle
    # Place base from (0,0) to (side,0), third vertex at (side/2, height)
    height = side * math.sqrt(3) / 2
    vertices = [
        (0, 0),
        (side, 0),
        (side / 2, height),
        (0, 0)  # close the path
    ]

    fig, ax = plt.subplots(figsize=(6, 5))
    ax.set_aspect('equal')

    # Create and draw the triangle
    triangle_patch = plt.Polygon(vertices, closed=True, facecolor=color, edgecolor='black', linewidth=2)
    ax.add_patch(triangle_patch)

    # Add caption at the center of the triangle
    center_x = side / 2
    center_y = height / 3
    ax.text(center_x, center_y, caption,
            ha='center', va='center',
            fontsize=12, bbox=dict(facecolor='white', alpha=0.7, boxstyle='round,pad=0.5'))

    # Set axis limits and grid
    margin = side * 0.2
    ax.set_xlim(-margin, side + margin)
    ax.set_ylim(-margin, height + margin)
    ax.grid(True, linestyle=':', alpha=0.6)
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_title(f"Equilateral Triangle (side = {side:.2f}, color = {color})")

    # Save to file if requested
    if output_file:
        plt.savefig(output_file, dpi=150, bbox_inches='tight')
        print(f"Figure saved to '{output_file}'")

    plt.show()


def task4():
    """Main interactive function for Task 4."""
    print("\n" + "=" * 50)
    print("EQUILATERAL TRIANGLE DRAWING")
    print("=" * 50)

    # Input side length
    side = get_positive_float("Enter side length (a): ", min_val=0.1, max_val=100.0)

    # Input color
    color_name = get_color()

    # Create triangle object
    triangle = EquilateralTriangle(side, color_name)

    # Display figure info
    print("\n" + triangle.get_params())

    # Input caption
    caption = get_caption()

    # Draw triangle and save to file
    draw_triangle(triangle, caption, output_file=DATA_DIR)



if __name__ == "__main__":
    task4()