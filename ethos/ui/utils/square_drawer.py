from rich.text import Text
from rich.console import Console

def draw_square(size):
    """
    Draws a square of solid color in the terminal using Rich and returns it.
    
    Args:
        size (int): The width and height of the square.
        color (str): The color name or hex code for the square.
    
    Returns:
        Text: A Rich Text object representing the square.
    """
    square = Text()

    # Build the square as a series of lines
    for _ in range(size):
        square.append(" " * (2 * size))
        square.append("\n")
    
    return square

