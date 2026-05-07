
import abc
import matplotlib.colors as mcolors
from math import sqrt

class Shape(abc.ABC):
    """Abstract base class for geometric shapes."""

    def __init__(self):
        print("Initializing geometric shape")

    @abc.abstractmethod
    def area(self) -> float:
        """Calculate area of the shape."""
        pass


class Color:
    """Class to store and validate color names."""

    def __init__(self, color: str):
        if color not in mcolors.CSS4_COLORS:
            raise ValueError(f"'{color}' is not a valid CSS4 color name.")
        self.__color = color

    @property
    def color(self) -> str:
        return self.__color

    @color.setter
    def color(self, color: str):
        if color not in mcolors.CSS4_COLORS:
            raise ValueError(f"'{color}' is not a valid CSS4 color name.")
        self.__color = color

    @color.deleter
    def color(self):
        self.__color = ""


class EquilateralTriangle(Shape):
    """Equilateral triangle with side length a and a color."""

    __figure_name = "Equilateral Triangle"

    @classmethod
    def info(cls) -> None:
        """Print the name of the figure."""
        print(f"Figure type: {cls.__figure_name}")

    def __init__(self, side: float, color: str):
        super().__init__()
        self.__side = side
        try:
            self.__color = Color(color)
        except ValueError as e:
            print(e)
            print("Using default color: black")
            self.__color = Color("black")

    @property
    def side(self) -> float:
        return self.__side

    @property
    def color(self) -> Color:
        return self.__color

    def area(self) -> float:
        """Area of equilateral triangle: (sqrt(3)/4) * a^2."""
        return (sqrt(3) / 4) * (self.__side ** 2)

    def get_params(self) -> str:
        """Return formatted string with figure parameters, color and area."""
        return "Figure: {}\nColor: {}\nSide length: {:.2f}\nArea: {:.3f}".format(
            self.__figure_name,
            self.__color.color,
            self.__side,
            self.area()
        )
