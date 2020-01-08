import random

class Board():
    def __init__(self, board):
        self.numSolutions = 0
        self.solution = []
        if not board:
            self.board = self.generateBoard()
        else:
            self.board = board
            self.solver(board)

    def generateBoard(self):

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
        self.solver(board)
        solvedBoard = [row[:] for row in self.solution]

        # Test all cells in a random order to see if removing it still allows for a unique solution
        cells = list(range(81))
        random.shuffle(cells)

        for c in cells:
            i, j = divmod(c, 9)
            tmp = solvedBoard[i][j]
            solvedBoard[i][j] = 0
            tempBoard = Board([row[:] for row in solvedBoard])
            if tempBoard.numSolutions != 1:
                solvedBoard[i][j] = tmp
        return solvedBoard

    def solver(self, boardCopy):

        board = [row[:] for row in boardCopy]

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
                    # Remove used values in that row, column, and box
                    for k in range(9):
                        if board[i][k] > 0:
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
            self.solution = board
            if self.numSolutions == 0:
                self.numSolutions += 1
                return False
            else:
                self.numSolutions += 1
                return True
        else:
            # Try all candidates.
            for i in candidates[fewestIndex[0]][fewestIndex[1]]:
                board[fewestIndex[0]][fewestIndex[1]] = i
                
                if self.solver(board):
                    return True

                # Set it back to 0 so backtracking isn't thrown off.
                board[fewestIndex[0]][fewestIndex[1]] = 0
            return False

def main():
    print()

if __name__ == "__main__":
    main()