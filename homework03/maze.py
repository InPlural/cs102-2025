from random import choice, randint
from typing import List, Optional, Tuple, Union

import pandas as pd


def create_grid(rows: int = 15, cols: int = 15) -> List[List[Union[str, int]]]:
    return [["■"] * cols for _ in range(rows)]


def remove_wall(grid: List[List[Union[str, int]]], coord: Tuple[int, int]) -> List[List[Union[str, int]]]:
    """

    :param grid:
    :param coord:
    :return:
    """

    row, col = coord
    index_last_col = len(grid[0]) - 1
    directions = ["up", "right"]
    decision = choice(directions)

    if decision == "up":
        if row > 1:
            grid[row - 1][col] = " "
        elif col < index_last_col - 1:
            grid[row][col + 1] = " "

    else:
        if col < index_last_col - 1:
            grid[row][col + 1] = " "
        elif row > 1:
            grid[row - 1][col] = " "
    return grid


def bin_tree_maze(rows: int = 15, cols: int = 15, random_exit: bool = True) -> List[List[Union[str, int]]]:
    """

    :param rows:
    :param cols:
    :param random_exit:
    :return:
    """

    grid = create_grid(rows, cols)
    empty_cells = []
    for x, row in enumerate(grid):
        for y, _ in enumerate(row):
            if x % 2 == 1 and y % 2 == 1:
                grid[x][y] = " "
                empty_cells.append((x, y))

    # 1. выбрать любую клетку
    # 2. выбрать направление: наверх или направо.
    # Если в выбранном направлении следующая клетка лежит за границами поля,
    # выбрать второе возможное направление
    # 3. перейти в следующую клетку, сносим между клетками стену
    # 4. повторять 2-3 до тех пор, пока не будут пройдены все клетки

    for cell in empty_cells:
        grid = remove_wall(grid, cell)

    # генерация входа и выхода
    if random_exit:
        x_in, x_out = randint(0, rows - 1), randint(0, rows - 1)
        y_in = randint(0, cols - 1) if x_in in (0, rows - 1) else choice((0, cols - 1))
        y_out = randint(0, cols - 1) if x_out in (0, rows - 1) else choice((0, cols - 1))
    else:
        x_in, y_in = 0, cols - 2
        x_out, y_out = rows - 1, 1

    grid[x_in][y_in], grid[x_out][y_out] = "X", "X"

    return grid


def get_exits(grid: List[List[Union[str, int]]]) -> List[Tuple[int, int]]:
    """

    :param grid:
    :return:
    """

    exits = [(x, y) for x, row in enumerate(grid) for y, element in enumerate(row) if element == "X"]
    return exits


def make_step(grid: List[List[Union[str, int]]], k: int) -> List[List[Union[str, int]]]:
    """

    :param grid:
    :param k:
    :return:
    """

    for i, row in enumerate(grid):
        for j, cell in enumerate(row):
            if cell == k:
                if i + 1 < len(grid) and grid[i + 1][j] == 0:
                    grid[i + 1][j] = k + 1
                if i - 1 >= 0 and grid[i - 1][j] == 0:
                    grid[i - 1][j] = k + 1
                if j + 1 < len(row) and grid[i][j + 1] == 0:
                    grid[i][j + 1] = k + 1
                if j - 1 >= 0 and grid[i][j - 1] == 0:
                    grid[i][j - 1] = k + 1
    return grid


def shortest_path(
    grid: List[List[Union[str, int]]], exit_coord: Tuple[int, int]
) -> Optional[Union[Tuple[int, int], List[Tuple[int, int]]]]:
    """

    :param grid:
    :param exit_coord:
    :return:
    """

    row, col = exit_coord

    if not (0 <= row < len(grid) and 0 <= col < len(grid[0])):
        return None

    cell = grid[row][col]

    if not isinstance(cell, int) or cell < 1:
        return None

    path = [(row, col)]

    while cell > 1:
        cell -= 1

        if row > 0 and grid[row - 1][col] == cell:
            row -= 1
        elif row < len(grid) - 1 and grid[row + 1][col] == cell:
            row += 1
        elif col > 0 and grid[row][col - 1] == cell:
            col -= 1
        elif col < len(grid[0]) - 1 and grid[row][col + 1] == cell:
            col += 1

        path.append((row, col))

    path.reverse()

    return path


def encircled_exit(grid: List[List[Union[str, int]]], coord: Tuple[int, int]) -> bool:
    """

    :param grid:
    :param coord:
    :return:
    """

    row, col = coord

    if row == 0 and grid[row + 1][col] == "■":
        return True
    if col == 0 and grid[row][col + 1] == "■":
        return True
    if row == len(grid) - 1 and grid[row - 1][col] == "■":
        return True
    if col == len(grid[row]) - 1 and grid[row][col - 1] == "■":
        return True
    return False


def solve_maze(
    grid: List[List[Union[str, int]]],
) -> Tuple[List[List[Union[str, int]]], Optional[Union[Tuple[int, int], List[Tuple[int, int]]]]]:
    """

    :param grid:
    :return:
    """

    exits = get_exits(grid)
    if len(exits) < 2:
        return grid, exits

    for el in exits:
        if encircled_exit(grid, el):
            return grid, None

    grid[exits[0][0]][exits[0][1]] = 1
    grid[exits[1][0]][exits[1][1]] = 0
    for i, row in enumerate(grid):
        for j, col in enumerate(row):
            if col == " ":
                grid[i][j] = 0
    k = 0
    while grid[exits[1][0]][exits[1][1]] == 0:
        k += 1
        make_step(grid, k)
    path = shortest_path(grid, exits[1])
    return grid, path


def add_path_to_grid(
    grid: List[List[Union[str, int]]], path: Optional[Union[Tuple[int, int], List[Tuple[int, int]]]]
) -> List[List[Union[str, int]]]:
    """

    :param grid:
    :param path:
    :return:
    """

    if path:
        for i, row in enumerate(grid):
            for j, _ in enumerate(row):
                if (i, j) in path:
                    grid[i][j] = "X"
    return grid


if __name__ == "__main__":
    print(pd.DataFrame(bin_tree_maze(15, 15)))
    GRID = bin_tree_maze(15, 15)
    print(pd.DataFrame(GRID))
    _, PATH = solve_maze(GRID)
    MAZE = add_path_to_grid(GRID, PATH)
    print(pd.DataFrame(MAZE))
