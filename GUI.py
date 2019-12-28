from sudoku import Board
from tkinter import Tk, Canvas, Frame, Button, Label, BOTH, TOP, BOTTOM, LEFT, RIGHT
from datetime import datetime

import time

MARGIN = 20  # Pixels around the board
SIDE = 60  # Width of every board cell.
WIDTH = HEIGHT = MARGIN * 2 + SIDE * 9  # Width and height of the whole board
HEIGHT + 1000

class SudokuUI(Frame):

    def __init__(self, parent):
        self.parent = parent
        board = Board([])
        self.start_puzzle = board.board
        self.board = [row[:] for row in self.start_puzzle]
        self.solved_puzzle = board.solution
        Frame.__init__(self, parent, bg="#FEF2B6")

        self.row, self.col = 0, 0

        self.__initUI()

    def __initUI(self):
        self.parent.title("Sudoku")
        self.pack(fill=BOTH, expand=1)
        self.canvas = Canvas(self, width=WIDTH, height=HEIGHT, bg="#FEF2B6")
        self.canvas.pack(fill=BOTH, side=TOP)
        
        frame = Frame(self, bg="#FEF2B6")
        frame.pack(side=LEFT, fill=BOTH)
        clear_button = Button(self, text="Clear", command=self.__clear_answers, bg="#007bff", fg="white")
        clear_button.grid(in_=frame, column=0, row=0)
        self.label = Label(text="", font=('Helvetica', 24), bg="#FEF2B6")
        self.label.grid(in_=frame, column=2, row=0)
        self.startTime = datetime.now()
        self.update_clock()

        self.__draw_grid()
        self.__draw_puzzle()

        self.canvas.bind("<Button-1>", self.__cell_clicked)
        self.canvas.bind("<Key>", self.__key_pressed)

    def update_clock(self):
        now = datetime.now()
        self.label.configure(text=str((now - self.startTime))[:7])
        if self.board != self.solved_puzzle:
            self.after(1000, self.update_clock)

    def __draw_grid(self):
        for i in range(10):
            color = "#925242" if i % 3 == 0 else "#CAA67E"

            x0 = MARGIN + i * SIDE
            y0 = MARGIN
            x1 = MARGIN + i * SIDE
            y1 = HEIGHT - MARGIN
            self.canvas.create_line(x0, y0, x1, y1, fill=color)

            x0 = MARGIN
            y0 = MARGIN + i * SIDE
            x1 = WIDTH - MARGIN
            y1 = MARGIN + i * SIDE
            self.canvas.create_line(x0, y0, x1, y1, fill=color)

    def __draw_puzzle(self):
        self.canvas.delete("numbers")
        for i in range(9):
            for j in range(9):
                answer = self.board[i][j]
                if answer != 0:
                    x = MARGIN + j * SIDE + SIDE // 2
                    y = MARGIN + i * SIDE + SIDE // 2
                    original = self.start_puzzle[i][j]
                    color = "black" if answer == original else "blue"
                    # Check for illegitimate value (it exists in that row/column/box) and highlight the duplicate values in red
                    for k in range(9):
                        if self.board[i][k] == self.board[i][j] and k != j:
                            color = "red"
                    for k in range(9):
                        if self.board[k][j] == self.board[i][j] and k != i:
                            color = "red"
                    for m in range(i - (i%3), i - (i%3) + 3):
                        for n in range(j - (j%3), j - (j%3) + 3):
                            if self.board[m][n] == self.board[i][j]:
                                if not (m == i and n == j):
                                    color = "red"
                    self.canvas.create_text(
                        x, y, text=answer, tags="numbers", fill=color
                    )

    def __clear_answers(self):
        self.canvas.delete("victory")
        self.canvas.delete("winner")
        self.board = [row[:] for row in self.start_puzzle]
        self.__draw_puzzle()
        self.startTime = datetime.now()
        self.update_clock()

    def __cell_clicked(self, event):

        x, y = event.x, event.y
        if (MARGIN < x < WIDTH - MARGIN and MARGIN < y < HEIGHT - MARGIN):
            self.canvas.focus_set()

            # get row and column numbers from x, y coordinates
            row, col = (y - MARGIN) // SIDE, (x - MARGIN) // SIDE

        # if cell was selected already - deselect it
            if (row, col) == (self.row, self.col):
                self.row, self.col = -1, -1
            elif self.start_puzzle[row][col] == 0:
                self.row, self.col = row, col

        self.__draw_cursor()

    def __draw_cursor(self):
        self.canvas.delete("cursor")
        if self.row >= 0 and self.col >= 0:
            x0 = MARGIN + self.col * SIDE + 1
            y0 = MARGIN + self.row * SIDE + 1
            x1 = MARGIN + (self.col + 1) * SIDE - 1
            y1 = MARGIN + (self.row + 1) * SIDE - 1
            self.canvas.create_rectangle(
                x0, y0, x1, y1,
                outline="red", tags="cursor"
            )

    def __key_pressed(self, event):
        # if self.game.game_over:
        #     return
        if self.row >= 0 and self.col >= 0 and event.char in "1234567890":
            self.board[self.row][self.col] = int(event.char)
            self.col, self.row = -1, -1
            self.__draw_puzzle()
            self.__draw_cursor()
            if self.board == self.solved_puzzle:
                self.__draw_victory()

    def __draw_victory(self):
        # create a oval (which will be a circle)
        x0 = y0 = MARGIN + SIDE * 2
        x1 = y1 = MARGIN + SIDE * 7
        self.canvas.create_oval(
            x0, y0, x1, y1,
            tags="victory", fill="dark orange", outline="orange"
        )
        # create text
        x = y = MARGIN + 4 * SIDE + SIDE // 2
        self.canvas.create_text(
            x, y,
            text="You win!", tags="winner",
            fill="white", font=("Arial", 32)
        )

if __name__ == '__main__':
    root = Tk()
    root.configure(bg="red")
    SudokuUI(root)
    root.geometry("%dx%d" % (WIDTH, HEIGHT + 40))
    root.mainloop()