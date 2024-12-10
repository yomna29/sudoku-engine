import random
import time

from colorama import Fore, Style
class SudokuGame:
    def __init__(self, board):
        self.board = board
        self.rows = [0] * 9
        self.cols = [0] * 9
        self.squares = [0] * 9


        for r in range(9):
            for c in range(9):
                num = board[r][c]
                if num != 0:
                    self.add_to_masks(r, c, num)

    def add_to_masks(self, row, col, num):
        bit = 1 << (num - 1)
        self.rows[row] |= bit
        self.cols[col] |= bit
        self.squares[self.get_square_index(row, col)] |= bit
    def check_row(self, row, num):
       # check the existence of this number in the row
        return num not in self.board[row]

    def check_col(self, col, num):
        # check the existence of this number in the col
        for row in range(9):
            if self.board[row][col] == num:
                return False
        return True

    def check_square(self, row, col, num):
        # check the existence of this number in the square
        start_row = (row // 3) * 3
        start_col = (col // 3) * 3
        for r in range(start_row, start_row + 3):
            for c in range(start_col, start_col + 3):
                if self.board[r][c] == num:
                    return False
        return True

    def is_valid_insertion(self, row, col, num):
        #check if the input number can be inserted in the current square
        return (
            self.check_row(row, num) and
            self.check_col(col, num) and
            self.check_square(row, col, num)
        )

    def insert_number(self, row, col, num):
        # add the number the the game board
        if self.is_valid_insertion(row, col, num):
            self.board[row][col] = num
            self.add_to_masks(row, col, num)
            return True
        return False

    def remove_number(self, row, col, num):
        self.board[row][col] = 0
        self._remove_from_masks(row, col, num)

    def get_square_index(self, row, col):
        return (row // 3) * 3 + (col // 3)



    def _remove_from_masks(self, row, col, num):
        bit = ~(1 << (num - 1))
        self.rows[row] &= bit
        self.cols[col] &= bit
        self.squares[self.get_square_index(row, col)] &= bit

    def print_board(self):
        for row in range(9):
            if row % 3 == 0 and row != 0:
                print("-" * 21)
            for col in range(9):
                if col % 3 == 0 and col != 0:
                    print("|", end=" ")
                print(self.board[row][col] if self.board[row][col] != 0 else ".", end=" ")
            print()


class BacktrackingSolver:
    def __init__(self, game):
        self.game = game

    def solve(self):
        """Solve the Sudoku puzzle using backtracking."""
        return self.backtrack({})  # Start with an empty assignment

    def backtrack(self, assignment):
        # If assignment is complete, return assignment
        if len(assignment) == 81:  # All cells filled
            return assignment
        var = self.select_unassigned_variable(assignment)
        if var is None:
            return assignment
        for value in self.order_domain_values(var, assignment):
            if self.is_consistent(var, value, assignment):
                # Add {var = value} to assignment
                assignment[var] = value
                row, col = var
                self.game.board[row][col] = value
                result = self.backtrack(assignment)
                if result:
                    return result
                # Remove {var = value} from assignment
                del assignment[var]
                self.game.board[row][col] = 0

        return False  # return failure

    def select_unassigned_variable(self, assignment):
        for row in range(9):
            for col in range(9):
                if (row, col) not in assignment and self.game.board[row][col] == 0:
                    return (row, col)
        return None  # No unassigned variable found

    def order_domain_values(self, var, assignment):
        row, col = var
        return [num for num in range(1, 10) if self.game.is_valid_insertion(row, col, num)]

    def is_consistent(self, var, value, assignment):
        row, col = var
        return self.game.is_valid_insertion(row, col, value)

    def validate_input(self):
        start_time = time.time()
        original_board = [row[:] for row in self.game.board]
        solvable = bool(self.solve())
        self.game.board = original_board
        end_time = time.time()
        print(f"Validation completed in {end_time - start_time:.6f} seconds.")
        return solvable

    def random_board_generator(self, clues=30):
        """Generate a random solvable Sudoku puzzle."""
        start_time = time.time()
        if not self.solve():
            return False

        # Remove numbers randomly to create the puzzle
        cells = [(r, c) for r in range(9) for c in range(9)]
        random.shuffle(cells)
        removed = 81 - clues
        for i in range(removed):
            row, col = cells[i]
            num = self.game.board[row][col]
            self.game.board[row][col] = 0
            self.game._remove_from_masks(row, col, num)

        end_time = time.time()
        print(f"Puzzle generation completed in {end_time - start_time:.6f} seconds.")
        return True


class ArcConsistency:
    def __init__(self, grid):
        self.grid = grid
        self.variables = {}
        self.arcs = []

    def represent_as_CSP(self):
        """Represent Sudoku grid as CSP variables with domains."""
        self.variables = {
            (row, col): {self.grid[row][col]} if self.grid[row][col] != 0 else set(range(1, 10))
            for row in range(9) for col in range(9)
        }


    def define_arcs(self):
        """Define arcs for Sudoku (row, column, and box constraints)."""
        for row in range(9):
            for col in range(9):
                if self.grid[row][col] == 0:
                    # Row constraints
                    for i in range(9):
                        if i != col:
                            self.arcs.append(((row, col), (row, i)))  # Row constraint
                            print(f"{Fore.RED}Row Arc: {((row, col), (row, i))}{Style.RESET_ALL}")
                    
                    # Column constraints
                    for i in range(9):
                        if i != row:
                            self.arcs.append(((row, col), (i, col)))  # Column constraint
                            print(f"{Fore.BLUE}Column Arc: {((row, col), (i, col))}{Style.RESET_ALL}")
                    # Box constraints
                    box_row, box_col = 3 * (row // 3), 3 * (col // 3)
                    for r in range(box_row, box_row + 3):
                        for c in range(box_col, box_col + 3):
                            if (r, c) != (row, col):
                                self.arcs.append(((row, col), (r, c)))  # Box constraint
                                print(f"{Fore.GREEN}Box Arc: {((row, col), (r, c))}{Style.RESET_ALL}")


    def initial_domain_reduction(self):
        """Reduce domains based on initial grid values."""
        for (row, col), domain in self.variables.items():
            if len(domain) == 1:
                value = next(iter(domain))
                for neighbor in self.get_neighbors(row, col):
                    self.variables[neighbor].discard(value)

    def apply_arc_consistency(self):
        """Apply arc consistency algorithm (AC-3)."""
        queue = self.arcs[:]
        while queue:
            (x1, x2) = queue.pop(0)
            if self.revise(x1, x2):
                if len(self.variables[x1]) == 0:
                    return False  # Failure: domain wiped out
                for neighbor in self.get_neighbors(*x1):
                    if neighbor != x2:
                        queue.append((neighbor, x1))
        return True

    def revise(self, x1, x2):
        """Revise the domain of x1 based on x2."""
        revised = False
        for value in list(self.variables[x1]):
            if all(value == val for val in self.variables[x2]):
                self.variables[x1].remove(value)
                revised = True
        return revised

    def update_sudoku_grid(self):
        """Update the grid with reduced domains."""
        for (row, col), domain in self.variables.items():
            if len(domain) == 1:
                self.grid[row][col] = next(iter(domain))

    def get_neighbors(self, row, col):
        """Get all neighboring cells of (row, col)."""
        neighbors = set()
        for i in range(9):
            if i != col:
                neighbors.add((row, i))  # Row neighbors
            if i != row:
                neighbors.add((i, col))  # Column neighbors
        box_row, box_col = 3 * (row // 3), 3 * (col // 3)
        for r in range(box_row, box_row + 3):
            for c in range(box_col, box_col + 3):
                if (r, c) != (row, col):
                    neighbors.add((r, c))  # Box neighbors
        return neighbors


# Example Usage
if __name__ == "__main__":
    board = [
        [5, 3, 0, 0, 7, 0, 0, 0, 0],
        [6, 0, 0, 1, 9, 5, 0, 0, 0],
        [0, 9, 8, 0, 0, 0, 0, 6, 0],
        [8, 0, 0, 0, 6, 0, 0, 0, 3],
        [4, 0, 0, 8, 0, 3, 0, 0, 1],
        [7, 0, 0, 0, 2, 0, 0, 0, 6],
        [0, 6, 0, 0, 0, 0, 2, 8, 0],
        [0, 0, 0, 4, 1, 9, 0, 0, 5],
        [0, 0, 0, 0, 8, 0, 0, 7, 9],
    ]

    game = SudokuGame(board)
    solver = BacktrackingSolver(game)

    arc_consistency = ArcConsistency(board)
    


    print("Initial Sudoku:")
    game.print_board()
    
    arc_consistency.represent_as_CSP()
    print("\nSudoku represented as CSP variables with domains:")
    for key, value in arc_consistency.variables.items():
        print(f"Cell {key}: {value}")



    print("\nDefined Arcs (constraints between cells):")

    arc_consistency.define_arcs()
    # for arc in arc_consistency.arcs:
    #     print(f"Arc: {arc}")

    arc_consistency.initial_domain_reduction()
    print("\nDomains after initial reduction based on grid values:")
    for key, value in arc_consistency.variables.items():
        print(f"Cell {key}: {value}")

    arc_consistency.apply_arc_consistency()
    print("\nDomains after applying arc consistency (AC-3):")
    for key, value in arc_consistency.variables.items():
        print(f"Cell {key}: {value}")

    arc_consistency.update_sudoku_grid()
    print("\nUpdated Sudoku Grid after applying arc consistency:")
    game.print_board()


    # print("\nValidating input...")
    # if solver.validate_input():
    #     print("The input puzzle is solvable.")
    # else:
    #     print("The input puzzle is not solvable.")

    # print("\nGenerating a random puzzle...")
    # if solver. random_board_generator(clues=25):
    #     print("Generated Random Puzzle:")
    #     game.print_board()
    # else:
    #     print("Failed to generate a random puzzle.")

    
