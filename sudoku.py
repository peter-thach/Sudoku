import random

# board = [
#     [0, 0, 0, 0, 0, 0, 0, 0, 0] * 9
# ]

board = [
    [3,7,0,0,0,9,0,0,6],
    [8,0,0,1,0,3,0,7,0],
    [0,0,0,0,0,0,0,0,8],
    [0,2,0,0,8,0,0,0,5],
    [1,8,7,0,0,0,6,4,2],
    [5,0,0,0,2,0,0,1,0],
    [7,0,0,0,0,0,0,0,0],
    [0,5,0,6,0,2,0,0,7],
    [2,0,0,3,0,0,0,6,1]
]

def generateBoard():
    """
    Generate a solvable board randomly. The steps are as follows:
        1. Choose the empty cell with the fewest possible candidates. If no such cell exists, the grid is filled
        and the algorithm should terminate.
        2. Choose a candidate at random and place it in the cell. Try to recursively fill the grid. If this fails,
        choose a different candidate at random and retry.
        3. If all candidates are exhausted, signal failure to the caller.
        
    """

    # Initialize the board
    board = [[0 for i in range (9)] for j in range (9)]

    # Fill out the first box randomly as there are no constraints on what its values can be yet.
    nums = [i for i in range(1, 10)]
    random.shuffle(nums)
    for i in range(3):
        for j in range(3):
            board[i][j] = nums.pop()

    # Fill out first 2 rows of box in the top row middle column.
    nums = [i for i in range(1, 10)]
    random.shuffle(nums)
    for i in range(2):
        # Remove numbers already used for that row by first box.
        removed = []
        for k in board[i][:3]:
            if k in nums:
                removed.append(k)
                nums.remove(k)
        # Fill out row
        for j in range(3, 6):
            board[i][j] = nums.pop()

        # Add back the removed numbers into a random index.
        for k in removed:
            if len(nums) <= 1:
                nums.insert(len(nums), k)
            else:
                nums.insert(random.choice([x for x in range(len(nums) - 1)]), k)
    # If the remaining nums are taken by the last row already then keep going back and changing 2nd row so we have 3 for last row
    enoughForLast = False
    while enoughForLast == False:
        for j in range(3, 6):
            nums.append(board[1][j])
            board[i][j] = 0
        random.shuffle(nums)
        # Remove numbers already used for that row by first box.
        removed = []
        for k in board[1][:3]:
            if k in nums:
                removed.append(k)
                nums.remove(k)
        # Fill out row
        for j in range(3, 6):
            board[1][j] = nums.pop()
        # Add back the removed numbers into a random index.
        for k in removed:
            if len(nums) <= 1:
                nums.insert(len(nums), k)
            else:
                nums.insert(random.choice([x for x in range(len(nums) - 1)]), k)
        # Check if there are 3 candidates for the last row
        enoughForLast = True
        for x in range(3):
            if board[2][x] in nums:
                enoughForLast = False
    board[2][3:6] = nums

    # The top right box's rows are determined by the other 6 values in the previous boxes' rows.
    for i in range(3):
        nums = [i for i in range(1, 10)]
        random.shuffle(nums)
        # Remove the 6 used numbers in that row
        for k in board[i][:6]:
            nums.remove(k)
        # Fill in the remaining 3 numbers
        board[i][6:] = nums

    nums = [i for i in range(1, 10)]
    random.shuffle(nums)
    # Remove the numbers used in the first column by the first box.
    for i in range(3):
        nums.remove(board[i][0])
    # Fill out the rest of the first column of the board.    
    for i in range(3, len(board)):
        board[i][0] = nums.pop()

    # Use the solver to fill in the rest of the board.
    return solve(board)[1]        

def solve(board):
    """
    The backtracking algorithm to solve a Sudoku puzzle is as follows:
        1. Generate, for each cell, a list of candidate values by starting with the set of all possible values and eliminating
        those which appear in the same row, column, and box as the cell being examined.
        2. Choose one empty cell. If none are available, the puzzle is solved.
        3. If the cell has no candidate values, the puzzle is unsolveable.
        4. For each candidate value in the cell, place the value in the cell and try to recursively solve the puzzle.
    
    There are two optimizations for this algorithm:
        1. When choosing a cell, always pick the one with the fewest candidate values. This reduces the branching factor. As 
        values are added to the grid, the number of candidates for other cells reduces too.
        2. When analyzing the candidate values for empty cells, it's much quicker to start with the analysis of the previous step 
        and modify it by removing values along the row, column, and box of the last-modified cell. This is O(N) in the size of the
        puzzle whereas analyzing from scratch is O(N^3).
    """

    # Generate the list of candidate values for each cell while keeping track of the cell with the fewest candidate values
    values = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    candidates = [[[1,2,3,4,5,6,7,8,9] for i in range (9)] for j in range (9)]
    for i in range(9):
        for j in range(9):
            candidates[i][j] = values.copy()

    fewest, fewestIndex = float("inf"), (-1, -1)
    for i in range(9):
        for j in range(9):
            if board[i][j] > 0:
                candidates[i][j] = []
            else:
                # print(f'j: {j}')
                # Remove used values in that row, column, and box
                for k in range(9):
                    if board[i][k] > 0:
                        # print(candidates[i][j])
                        # print(board[i][k])
                        candidates[i][j].remove(board[i][k])
                for l in range(9):
                    if board[l][j] > 0 and board[l][j] in candidates[i][j]:
                        candidates[i][j].remove(board[l][j])
                # Find the top left corner of the current subbox to start iterating it by finding its distance from the current cell
                for m in range(i - (i%3), i - (i%3) + 3):
                    for n in range(j - (j%3), j - (j%3) + 3):
                        if board[m][n] > 0 and board[m][n] in candidates[i][j]:
                            candidates[i][j].remove(board[m][n])
                # Update the cell with the fewest candidates
                if len(candidates[i][j]) < fewest:
                    fewest = len(candidates[i][j])
                    fewestIndex = (i, j)

    # Check for empty cell whose candidates list is the smallest.
    # If all cells are nonzero, puzzle is solved. If a zero cell has no candidate values, puzzle is unsolvable.
    if fewestIndex == (-1, -1):
        return (True, board)
    else:
        # Try all candidates.
        for i in candidates[fewestIndex[0]][fewestIndex[1]]:
            board[fewestIndex[0]][fewestIndex[1]] = i
            
            if solve(board)[0]:
                return (True, board)
            
            # Set it back to 0 so backtracking isn't thrown off.
            board[fewestIndex[0]][fewestIndex[1]] = 0
        return (False, [])

def main():
    print(generateBoard())

if __name__ == "__main__":
    main()