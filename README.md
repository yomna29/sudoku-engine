
# **Sudoku Solver and Interactive Game with GUI**

A **Python-based Sudoku Solver and Game** that provides an interactive gameplay experience with AI-driven solutions. This project uses **Backtracking** and **Arc Consistency** algorithms to solve Sudoku puzzles efficiently. Users can input puzzles, validate their entries, or watch the AI solve puzzles step-by-step.

---

## **1. Game Description**

**Sudoku** is a logic-based number-placement game. The objective is to complete a 9x9 grid such that:
- Each **row**, **column**, and **3x3 subgrid** contains all digits from `1 to 9`.
- Numbers cannot repeat in any row, column, or subgrid.

This project offers:
- **Interactive Sudoku gameplay** with real-time validation.
- An **AI Solver** that solves puzzles using **Backtracking** and **Arc Consistency**.
- The ability to generate random, solvable puzzles.

---

## **2. Features**

### **2.1 Game Modes**

- **Mode 1: AI Solver**
  - Watch the AI solve puzzles in real time using **Backtracking** or **Arc Consistency**.
  - Displays the solving process step-by-step in the GUI.

- **Mode 2: Interactive Sudoku**
  - Input custom puzzles using the interactive GUI.
  - Validate each entry for compliance with Sudoku rules.
  - Solve the puzzle automatically by clicking a button.

### **2.2 Algorithms**

#### **Backtracking**
- Recursively solves puzzles by trying all valid numbers for each empty cell.
- Backtracks when no valid placement is possible.
- Validates user-input puzzles for solvability.
- Generates random puzzles while ensuring they have solutions.

#### **Arc Consistency**
1. **Representation as a CSP**:
   - Each cell in the grid is a *variable*.
   - Each variable has a *domain* of possible values `[1–9]`.
   - Constraints ensure no repeated values in rows, columns, or subgrids.

2. **Defining Arcs**:
   - Arcs are binary constraints between connected variables:
     - All pairs of cells in the same row, column, or subgrid.

3. **Domain Reduction**:
   - Pre-filled cells have domains reduced to a single value.
   - Iteratively reduce the domains of other cells by enforcing constraints.

4. **Updating the Grid**:
   - Assign cells with singleton domains (only one possible value).

### **2.3 GUI Features**

- **Interactive Grid**:
  - Click on any cell to input numbers.
  - Invalid entries are highlighted with visual cues.

- **Buttons**:
  - **Solve Puzzle**: Lets the AI solve the puzzle step-by-step.
  - **Generate Puzzle**: Generates a random, solvable puzzle.

- **Real-Time Feedback**:
  - Ensures user inputs do not violate Sudoku rules.

---

## **3. Requirements**

### **3.1 Libraries**
- **Python 3.x**
- **PyQt5**:
  ```bash
  pip install PyQt5
  ```

---

## **4. Installation**

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/sudoku-solver.git
   cd sudoku-solver
   ```

2. Install dependencies:
   ```bash
   pip install PyQt5
   ```

3. Run the application:
   ```bash
   python main.py
   ```

---

## **5. Usage**

### **5.1 Running the Application**
- Launch the app by running:
  ```bash
  python main.py
  ```

### **5.2 Game Modes**

#### **Mode 1: AI Solver**
- Load a pre-defined or random puzzle.
- Click the **"Solve"** button to watch the AI solve the puzzle.

#### **Mode 2: Interactive Game**
- Input your own puzzle using the interactive grid.
- Validate entries in real-time:
  - Highlight invalid entries (e.g., red borders for rule violations).
- Click **"Solve"** to let the AI complete the puzzle.

---

## **6. Code Structure**

### **6.1 Classes**

1. **`SudokuGame`**
   - Manages the Sudoku board and provides:
     - Methods for validating rows, columns, and subgrids using bitmasking.
     - Functions for adding/removing numbers from the grid.

2. **`BacktrackingSolver`**
   - Solves puzzles using the Backtracking algorithm.
   - Validates whether user-input puzzles are solvable.
   - Supports random puzzle generation.

3. **`ArcConsistencySolver`** *(Placeholder for future updates)*
   - Represents Sudoku as a Constraint Satisfaction Problem (CSP).
   - Reduces cell domains iteratively using arc consistency.

4. **GUI**
   - Built with **PyQt5**.
   - Features:
     - Interactive 9x9 grid for user input.
     - Buttons for solving puzzles and generating random puzzles.

---

## **7. Example Outputs**

### **7.1 Initial Puzzle**
```plaintext
5 3 . | . 7 . | . . .
6 . . | 1 9 5 | . . .
. 9 8 | . . . | . 6 .
------+-------+-------
8 . . | . 6 . | . . 3
4 . . | 8 . 3 | . . 1
7 . . | . 2 . | . . 6
------+-------+-------
. 6 . | . . . | 2 8 .
. . . | 4 1 9 | . . 5
. . . | . 8 . | . 7 9
```

### **7.2 Solved Puzzle**
```plaintext
5 3 4 | 6 7 8 | 9 1 2
6 7 2 | 1 9 5 | 3 4 8
1 9 8 | 3 4 2 | 5 6 7
------+-------+-------
8 5 9 | 7 6 1 | 4 2 3
4 2 6 | 8 5 3 | 7 9 1
7 1 3 | 9 2 4 | 8 5 6
------+-------+-------
9 6 1 | 5 3 7 | 2 8 4
2 8 7 | 4 1 9 | 6 3 5
3 4 5 | 2 8 6 | 1 7 9
```

---

## **8. Future Enhancements**

- **Arc Consistency Visualization**:
  - Show step-by-step domain reductions for each cell.

- **Improved Variable Selection**:
  - Use heuristics like **Minimum Remaining Values (MRV)** to enhance Backtracking.

- **Interactive Features**:
  - Add themes, difficulty levels, and time tracking.

- **Scoring System**:
  - Track user performance and completion times.
