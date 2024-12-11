import pygame
import sys
from pygame.locals import *
import random
import time
from colorama import Fore, Style
class SudokuGame:
    def __init__(self, board):
        # Flatten the 2D board into a 1D array
        self.board = [num for row in board for num in row]
        self.rows = [0] * 9
        self.cols = [0] * 9
        self.squares = [0] * 9

        for index, num in enumerate(self.board):
            if num != 0:
                self.add_to_masks(index, num)

    def add_to_masks(self, index, num):
        row, col = self.get_row_col(index)
        square = self.get_square_index(row, col)
        bit = 1 << (num - 1)
        self.rows[row] |= bit
        self.cols[col] |= bit
        self.squares[square] |= bit

    def _remove_from_masks(self, index, num):
        row, col = self.get_row_col(index)
        square = self.get_square_index(row, col)
        bit = ~(1 << (num - 1))
        self.rows[row] &= bit
        self.cols[col] &= bit
        self.squares[square] &= bit

    def get_row_col(self, index):
        """Map 1D index to 2D row and column."""
        return index // 9, index % 9

    def get_square_index(self, row, col):

        return (row // 3) * 3 + (col // 3)

    def check_row(self, row, num):

        return all(self.board[row * 9 + col] != num for col in range(9))

    def check_col(self, col, num):

        return all(self.board[row * 9 + col] != num for row in range(9))

    def check_square(self, row, col, num):

        start_row = (row // 3) * 3
        start_col = (col // 3) * 3
        for r in range(start_row, start_row + 3):
            for c in range(start_col, start_col + 3):
                if self.board[r * 9 + c] == num:
                    return False
        return True

    def is_valid_insertion(self, index, num):
        row, col = self.get_row_col(index)
        return (
            self.check_row(row, num)
            and self.check_col(col, num)
            and self.check_square(row, col, num)
        )

    def insert_number(self, index, num):
        """Insert a number into the board if valid."""
        if self.is_valid_insertion(index, num):
            self.board[index] = num
            self.add_to_masks(index, num)
            return True
        return False

    def remove_number(self, index, num):
        """Remove a number from the board."""
        self.board[index] = 0
        self._remove_from_masks(index, num)

    def print_board(self):

        for i in range(9):
            if i % 3 == 0 and i != 0:
                print("-" * 21)
            for j in range(9):
                index = i * 9 + j
                if j % 3 == 0 and j != 0:
                    print("|", end=" ")
                print(self.board[index] if self.board[index] != 0 else ".", end=" ")
            print()

class BacktrackingSolver:
    def __init__(self, game):
        self.game = game

    def backtracking_search(self):
        return self.backtrack({})  # Start with an empty assignment

    def backtrack(self, assignment):
        if len(assignment) == 81:
            return assignment
        var = self.select_unassigned_variable(assignment)
        if var is None:
            return assignment
        for value in self.order_domain_values(var, assignment):
            if self.is_consistent(var, value, assignment):
                # Add {var = value} to assignment
                assignment[var] = value
                row, col = var
                index = row * 9 + col
                self.game.board[index] = value
                result = self.backtrack(assignment)
                if result:
                    return result
                del assignment[var]
                self.game.board[index] = 0

        return False  # return failure

    def select_unassigned_variable(self, assignment):
        for row in range(9):
            for col in range(9):
                index = row * 9 + col
                if (row, col) not in assignment and self.game.board[index] == 0:
                    return (row, col)
        return None

    def order_domain_values(self, var, assignment):
        row, col = var
        index = row * 9 + col
        return [num for num in range(1, 10) if self.game.is_valid_insertion(index, num)]

    def is_consistent(self, var, value, assignment):
        row, col = var
        index = row * 9 + col
        return self.game.is_valid_insertion(index, value)

    def validate_input(self):
        start_time = time.time()
        original_board = self.game.board[:]
        solvable = bool(self.backtracking_search())
        self.game.board = original_board
        end_time = time.time()
        print(f"Validation completed in {end_time - start_time:.6f} seconds.")
        return solvable

    def random_board_generator(self, clues):
        if not self.backtracking_search():
            return False

        indices_to_be_filled = list(range(81))
        random.shuffle(indices_to_be_filled)
        removed = 81 - clues

        for i in range(removed):
            index = indices_to_be_filled[i]
            num = self.game.board[index]
            self.game.board[index] = 0
            self.game._remove_from_masks(index, num)

        return True

    def create_easy_board(self, clues):
        return self.random_board_generator(36)

    def create_intermediate_board(self):
        return self.random_board_generator(27)

    def create_hard_board(self):
        return self.random_board_generator(19)

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

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 700
GRID_SIZE = 540  # Size of the Sudoku grid
CELL_SIZE = GRID_SIZE // 9

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
BLUE = (0, 0, 255)
RED = (255, 0, 0)

# Fonts
FONT = pygame.font.Font(None, 40)
SMALL_FONT = pygame.font.Font(None, 30)

# Create screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Sudoku Solver")

class SudokuGUI:
    def __init__(self, solver, game):
        self.solver = solver
        self.game = game
        self.board = self.game.board[:]
        self.selected_cell = None
        self.manual_mode = False
        self.invalid_cells = set()  # Track invalid cell positions
        self.show_solve_button = False

    def draw_grid(self):
        """Draw the Sudoku grid."""
        for row in range(10):
            line_width = 3 if row % 3 == 0 else 1
            pygame.draw.line(screen, BLACK, (0, row * CELL_SIZE), (GRID_SIZE, row * CELL_SIZE), line_width)
            pygame.draw.line(screen, BLACK, (row * CELL_SIZE, 0), (row * CELL_SIZE, GRID_SIZE), line_width)

    def draw_numbers(self):
        """Draw numbers on the grid."""
        for row in range(9):
            for col in range(9):
                index = row * 9 + col
                num = self.board[index]
                if num != 0:
                    color = RED if (row, col) in self.invalid_cells else BLACK
                    text = FONT.render(str(num), True, color)
                    x = col * CELL_SIZE + CELL_SIZE // 3
                    y = row * CELL_SIZE + CELL_SIZE // 4
                    screen.blit(text, (x, y))

    def select_cell(self, pos):
        """Select a cell based on mouse position."""
        x, y = pos
        if x < GRID_SIZE and y < GRID_SIZE:
            row, col = y // CELL_SIZE, x // CELL_SIZE
            self.selected_cell = row * 9 + col

    def update_board(self, num):
        """Update the board manually with real-time validation."""
        if self.selected_cell is not None and self.manual_mode:
            row, col = self.selected_cell // 9, self.selected_cell % 9
            index = self.selected_cell

            # Check if the number is valid
            if self.game.is_valid_insertion(index, num):
                self.board[index] = num
                self.invalid_cells.discard((row, col))  # Remove from invalid cells
            else:
                self.invalid_cells.add((row, col))  # Mark as invalid
                print(f"Number {num} at ({row + 1}, {col + 1}) violates constraints!")

    def reset_board(self):
        """Reset the board for manual mode."""
        self.board = [0] * 81
        self.manual_mode = True
        self.invalid_cells = set()  # Clear invalid cells
        self.show_solve_button = True

    def set_generated_board(self, difficulty):
        """Generate a board based on difficulty."""
        if difficulty == "Easy":
            self.solver.create_easy_board(36)
        elif difficulty == "Intermediate":
            self.solver.create_intermediate_board()
        elif difficulty == "Hard":
            self.solver.create_hard_board()

        self.board = self.game.board[:]
        self.manual_mode = False
        self.show_solve_button = True

    def solve_puzzle(self):
        """Solve the puzzle."""
        self.solver.backtracking_search()
        self.board = self.game.board[:]
        self.invalid_cells = set()  # Clear invalid cells after solving
    def draw_buttons(self):
        """Draw buttons on the screen."""
        if self.show_solve_button:
            solve_button = pygame.Rect(200, 600, 200, 50)
            pygame.draw.rect(screen, BLUE, solve_button)
            text = FONT.render("Solve", True, WHITE)
            screen.blit(text, (solve_button.x + 50, solve_button.y + 10))
            return solve_button
        return None

    def main_menu(self):
        """Display the main menu."""
        screen.fill(WHITE)
        manual_button = pygame.Rect(100, 200, 400, 50)
        ai_button = pygame.Rect(100, 300, 400, 50)

        pygame.draw.rect(screen, BLUE, manual_button)
        pygame.draw.rect(screen, BLUE, ai_button)

        manual_text = FONT.render("Manual Board Generator", True, WHITE)
        ai_text = FONT.render("AI Board Generator", True, WHITE)

        screen.blit(manual_text, (manual_button.x + 50, manual_button.y + 10))
        screen.blit(ai_text, (ai_button.x + 100, ai_button.y + 10))

        pygame.display.update()
        return manual_button, ai_button

    def difficulty_menu(self):
        """Display the difficulty selection menu."""
        screen.fill(WHITE)
        easy_button = pygame.Rect(100, 200, 400, 50)
        medium_button = pygame.Rect(100, 300, 400, 50)
        hard_button = pygame.Rect(100, 400, 400, 50)

        pygame.draw.rect(screen, BLUE, easy_button)
        pygame.draw.rect(screen, BLUE, medium_button)
        pygame.draw.rect(screen, BLUE, hard_button)

        easy_text = FONT.render("Easy", True, WHITE)
        medium_text = FONT.render("Intermediate", True, WHITE)
        hard_text = FONT.render("Hard", True, WHITE)

        screen.blit(easy_text, (easy_button.x + 150, easy_button.y + 10))
        screen.blit(medium_text, (medium_button.x + 140, medium_button.y + 10))
        screen.blit(hard_text, (hard_button.x + 150, hard_button.y + 10))

        pygame.display.update()
        return easy_button, medium_button, hard_button


def main():
    game = SudokuGame([[0] * 9 for _ in range(9)])
    solver = BacktrackingSolver(game)
    gui = SudokuGUI(solver, game)

    in_menu = True
    in_difficulty_menu = False
    running = True

    while running:
        screen.fill(WHITE)

        if in_menu:
            manual_button, ai_button = gui.main_menu()
        elif in_difficulty_menu:
            easy_button, medium_button, hard_button = gui.difficulty_menu()
        else:
            gui.draw_grid()
            gui.draw_numbers()
            solve_button = gui.draw_buttons()

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if event.type == MOUSEBUTTONDOWN:
                if in_menu:
                    if manual_button.collidepoint(event.pos):
                        in_menu = False
                        gui.reset_board()
                    elif ai_button.collidepoint(event.pos):
                        in_menu = False
                        in_difficulty_menu = True
                elif in_difficulty_menu:
                    if easy_button.collidepoint(event.pos):
                        gui.set_generated_board("Easy")
                        in_difficulty_menu = False
                    elif medium_button.collidepoint(event.pos):
                        gui.set_generated_board("Intermediate")
                        in_difficulty_menu = False
                    elif hard_button.collidepoint(event.pos):
                        gui.set_generated_board("Hard")
                        in_difficulty_menu = False
                else:
                    gui.select_cell(event.pos)
                    if solve_button and solve_button.collidepoint(event.pos):
                        gui.solve_puzzle()

            if event.type == KEYDOWN and gui.manual_mode:
                if event.unicode.isdigit() and 1 <= int(event.unicode) <= 9:
                    gui.update_board(int(event.unicode))
                elif event.key == K_BACKSPACE:
                    gui.update_board(0)  # Clear the cell

        pygame.display.update()


if __name__ == "__main__":
    main()
