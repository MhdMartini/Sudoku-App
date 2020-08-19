import random
from itertools import combinations, product
import numpy as np
from time import time
import sys
from analyzer import validate_sudoku


class SudokuGenerator:
    # Start with a Sudoku solution. Perform operations that result in different valid solutions
    base_sudoku = np.array(
        [
            [1, 8, 6, 3, 5, 7, 9, 4, 2],  # Top Third
            [7, 4, 2, 8, 6, 9, 3, 1, 5],  # .
            [5, 9, 3, 2, 4, 1, 6, 7, 8],  # .
            [3, 6, 4, 9, 1, 5, 2, 8, 7],  # Middle Third
            [8, 7, 1, 4, 3, 2, 5, 6, 9],  # .
            [2, 5, 9, 7, 8, 6, 4, 3, 1],  # .
            [4, 2, 8, 1, 9, 3, 7, 5, 6],  # Bottom Third
            [6, 3, 7, 5, 2, 8, 1, 9, 4],  # .
            [9, 1, 5, 6, 7, 4, 8, 2, 3]  # .
        ]
    )

    patterns = []

    def generate_sln(self):
        self.sudoku = self.base_sudoku
        self.sudoku = self.shuffle_sudoku_1()       # Exchange numbers
        self.sudoku = self.shuffle_sudoku_2()       # Shuffle bands and strips
        self.sudoku_copy = np.copy(self.sudoku)
        self.starting_grid = self.make_puzzle()
        self.add_more(50-18)
        return self.starting_grid, self.sudoku

    def shuffle_sudoku_1(self):
        # Exchange numbers
        new_solution = self.sudoku
        # Create a random list of tuples for numbers to be swapped, e.g. [(2, 8), (5, 1), ..., ..., ...]
        # Five paris of numbers are swapped.
        exchanged_numbers = random.sample(list(combinations(range(1, 10), 2)), 7)
        for a, b in exchanged_numbers:
            new_solution = self.swapper(a, b, new_solution)

        return new_solution

    def swapper(self, a, b, solution):
        # Swap a and b
        for row, sublist in enumerate(solution):
            for column, num in enumerate(sublist):
                if num == a:
                    solution[row][column] = b
                elif num == b:
                    solution[row][column] = a

        return solution

    def shuffle_sudoku_2(self):
        # Shuffle rows and columns within bands and strips
        solution = self.sudoku
        for _ in range(2):
            for i in range(0, 9, 3):
                solution[i: i + 3] = np.array(random.sample(solution[i: i + 3].tolist(), 3))
            solution = solution.transpose()

        return solution

    def make_puzzle(self):
        # Create a rotationally symmetrical Sudoku puzzle
        # Minimum number of clues for rotational symmetry is 18
        starting_grid = np.zeros(81).reshape(9, 9)

        # display initial 18 values
        added = 0
        mid_point = 4
        while added != 18:
            # Change a number from 0 to 80 to a coordinate from (0,0) to (8,8)
            rand = random.choice(range(81))
            y, x = divmod(rand, 9)
            if starting_grid[y, x] != 0:
                continue

            starting_grid[y, x] = self.sudoku[y, x]

            # Find the symmetrical point to the randomly selected point
            x_diff = (mid_point - x) * 2
            y_diff = (mid_point - y) * 2
            new_x = x + x_diff
            new_y = y + y_diff

            starting_grid[new_y, new_x] = self.sudoku[new_y, new_x]

            added += 2

        return starting_grid

    def add_more(self, n):
        # Add additional clues to the starting 18
        added = random.sample(range(81), n)
        for point in added:
            y, x = divmod(point, 9)
            while self.starting_grid[y, x] != 0:
                y, x = divmod(random.choice(range(81)), 9)
            self.starting_grid[y, x] = self.sudoku[y, x]


if __name__ == '__main__':
    t = time()
    for _ in range(1):
        SudokuGenerator().generate_sln()

    print(time() - t)
