class CSP:
    def __init__(self, variables, domains, constraints):
        self.variables = variables  # List of variables
        self.domains = domains      # Dict of domains {var: [values]}
        self.constraints = constraints  # Dict {var: [neighbors]}

    def is_consistent(self, var, value, assignment):
        """Check if assigning value to var satisfies all constraints."""
        for neighbor in self.constraints[var]:
            if neighbor in assignment and assignment[neighbor] == value:
                return False
        return True

    def forward_checking(self, var, value):
        """Prune domains of neighbors based on assigned value."""
        inferences = {}
        for neighbor in self.constraints[var]:
            if value in self.domains[neighbor]:
                self.domains[neighbor].remove(value)
                inferences.setdefault(neighbor, []).append(value)
            if not self.domains[neighbor]:
                return False, inferences
        return True, inferences

    def restore_domains(self, inferences):
        """Undo domain pruning during backtracking."""
        for var, values in inferences.items():
            self.domains[var].extend(values)



class SudokuGame(CSP):
    def __init__(self, board):
        variables = [(r, c) for r in range(9) for c in range(9)]
        domains = {var: list(range(1, 10)) if board[var[0]][var[1]] == 0 else [board[var[0]][var[1]]]
                   for var in variables}
        constraints = self.define_constraints(variables)

        super().__init__(variables, domains, constraints)  # Initialize CSP superclass
        self.board = board

    def define_constraints(self, variables):
        """Define Sudoku constraints for neighbors."""
        constraints = {}
        for row, col in variables:
            neighbors = self.get_neighbors(row, col)
            constraints[(row, col)] = neighbors
        return constraints

    def get_neighbors(self, row, col):
        """Get all neighbors of a cell."""
        neighbors = set()

        # Row neighbors
        for c in range(9):
            if c != col:
                neighbors.add((row, c))

        # Column neighbors
        for r in range(9):
            if r != row:
                neighbors.add((r, col))

        # Box neighbors
        box_row, box_col = 3 * (row // 3), 3 * (col // 3)
        for r in range(box_row, box_row + 3):
            for c in range(box_col, box_col + 3):
                if (r, c) != (row, col):
                    neighbors.add((r, c))

        return neighbors

    def update_board(self, assignment):
        """Update the Sudoku grid based on assignment."""
        for (row, col), value in assignment.items():
            self.board[row][col] = value
    def print_board(self):
        for row in range(9):
            if row % 3 == 0 and row != 0:
                print("-" * 21)  # Horizontal line after every 3 rows
            for col in range(9):
                if col % 3 == 0 and col != 0:
                    print("|", end=" ")  # Vertical line after every 3 columns
                # Print cell value or a placeholder for empty cells
                print(self.board[row][col] if self.board[row][col] != 0 else ".", end=" ")
            print()  # Move to the next line

class BacktrackingSolver:
    def __init__(self, game):
        self.game = game

    def solve(self):
        return self.backtrack({})

    def backtrack(self, assignment):
        if len(assignment) == len(self.game.variables):
            self.game.update_board(assignment)  # Update board with the solution
            return assignment

        var = self.select_unassigned_variable(assignment)
        for value in self.order_domain_values(var, assignment):
            if self.game.is_consistent(var, value, assignment):
                assignment[var] = value
                success, inferences = self.game.forward_checking(var, value)
                if success:
                    result = self.backtrack(assignment)
                    if result:
                        return result
                del assignment[var]
                self.game.restore_domains(inferences)

        return None

    def select_unassigned_variable(self, assignment):
        unassigned = [v for v in self.game.variables if v not in assignment]
        return min(unassigned, key=lambda var: len(self.game.domains[var]))

    def order_domain_values(self, var, assignment):
        return self.game.domains[var]
    
if __name__ == "__main__":
    grid = [
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

    sudoku = SudokuGame(grid)
    solver = BacktrackingSolver(sudoku)

    print("Initial Sudoku Board:")
    sudoku.print_board()

    if solver.solve():
        print("\nSolved Sudoku Board:")
        sudoku.print_board()
    else:
        print("\nNo solution exists.")
