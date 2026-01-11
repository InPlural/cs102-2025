import tkinter as tk
from copy import deepcopy
from tkinter import ttk
from typing import List

from maze import bin_tree_maze, solve_maze, add_path_to_grid


def draw_cell(x, y, color, size: int = 10):
    """Draws a cell."""

    x *= size
    y *= size
    x1 = x + size
    y1 = y + size
    canvas.create_rectangle(x, y, x1, y1, fill=color)


def draw_maze(grid: List[List[str]], size: int = 10):
    """Draws the maze."""

    for x, row in enumerate(grid):
        for y, cell in enumerate(row):
            if cell == " ":
                color = "White"
            elif cell == "■":
                color = "black"
            elif cell == "X":
                color = "#00ddc0"  # miku owns the world
            draw_cell(y, x, color, size)


def is_solvable(grid: List[List[str | int]]) -> bool:
    """Checks if the maze is solvable."""

    new_grid = deepcopy(grid)
    _, path = solve_maze(new_grid)
    return bool(path)


def show_solution():
    """Shows the solution."""

    global GRID

    grid_copy = [row.copy() for row in GRID]
    maze_with_numbers, path = solve_maze(grid_copy)

    if path:
        maze_for_display = [row.copy() for row in GRID]
        maze_with_path = add_path_to_grid(maze_for_display, path)
        draw_maze(maze_with_path, CELL_SIZE)


if __name__ == "__main__":
    global GRID, CELL_SIZE
    N, M = 51, 77

    CELL_SIZE = 10
    GRID = bin_tree_maze(N, M)

    while not is_solvable(GRID):
        GRID = bin_tree_maze(N, M)

    window = tk.Tk()
    window.title("Maze")
    window.geometry("%dx%d" % (M * CELL_SIZE + 100, N * CELL_SIZE + 100))

    canvas = tk.Canvas(window, width=M * CELL_SIZE, height=N * CELL_SIZE)
    canvas.pack()

    draw_maze(GRID, CELL_SIZE)
    ttk.Button(window, text="Solve", command=show_solution).pack(pady=20)

    window.mainloop()
