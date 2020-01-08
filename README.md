# Sudoku
An implementation of the game Sudoku with tkinter.

## Rules of the Game
Sudoku is played on a 9x9 grid made up of 9 3x3 squares. The goal is to fill each space with a number, 1-9, such that there are no repeating
numbers in any row, column, or square. A given puzzle has a certain amount of spaces already filled in and the player must fill in the 
remaining spaces to obtain the unique solution.

## Solver
The Sudoku solver uses backtracking to solve the board. The steps are as follows:

1. Generate, for each cell, a list of candidate values by starting with the set of all possible values and eliminating
   those which appear in the same row, column, and box as the cell being examined.
2. Choose one empty cell. If none are available, the puzzle is solved.
3. If the cell has no candidate values, the puzzle is unsolveable.
4. For each candidate value in the cell, place the value in the cell and try to recursively solve the puzzle.

This algorithm is also optimized by choosing the space with the fewest candidate values at each iteration. This reduces the branching
factor.

## Board Generator
This implementation of Sudoku automatically generates a new puzzle at the start of each game. The steps are as follows:

### 1. Generate the solved board
1. Fill the top left square with numbers 1-9 in a randomized order. Since the other 8 squares are not filled yet, the top left square
   is not bound by any row or column restrictions as long as it does not reuse numbers.
2. Fill the top middle square similarly, but this time each of its rows are limited by the 3 numbers chosen in each row of the first square.
3. Then the last square of the top row will be filled according to the 6 numbers already chosen in the first two squares.
4. Fill the rest of the grid using the backtracking solver.

### 2. Generate the puzzle by removing numbers
1. Shuffle the list of 81 spaces.
2. For each space in the shuffled order, remove its value and check if the grid is uniquely solvable. That is, the backtracking solver
   returns exactly one solution for the puzzle. If not, add the value back.
   
## Built With
* Python
* tkinter

## Authors
Peter Thach

[Github](https://github.com/peter-thach)
