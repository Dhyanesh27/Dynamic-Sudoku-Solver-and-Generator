
import tkinter as tk
from tkinter import font as tkfont
import time
import copy
import random

def is_valid_choice(board, row, col, num):
    if num in board[row]:
        return False
    for i in range(9):
        if board[i][col] == num:
            return False
    box_row, box_col = row // 3 * 3, col // 3 * 3
    for i in range(box_row, box_row + 3):
        for j in range(box_col, box_col + 3):
            if board[i][j] == num:
                return False
    return True

def find_empty_cell(board):
    for i in range(9):
        for j in range(9):
            if board[i][j] == 0:
                return (i, j)
    return None

def solve_sudoku_visual(board, delay=0.05, instant_mode=False):
    empty = find_empty_cell(board)
    if not empty:
        return True
    row, col = empty # storing empty cells in row,col
    for num in range(1, 10):
        if SudokuSolverGUI.stop_solving:
            return False
        if is_valid_choice(board, row, col, num):
            board[row][col] = num
            if not instant_mode:
                SudokuSolverGUI.update_display(board, (row, col))
                time.sleep(delay)
            if solve_sudoku_visual(board, delay, instant_mode):
                return True
            board[row][col] = 0
            if not instant_mode:
                SudokuSolverGUI.update_display(board, (row, col))
                time.sleep(delay)
    return False

def solve_instant(board):
    empty = find_empty_cell(board)
    if not empty:
        return True
    row, col = empty
    for num in random.sample(range(1, 10), 9):
        if is_valid_choice(board, row, col, num):
            board[row][col] = num
            if solve_instant(board):
                return True
            board[row][col] = 0
    return False

def generate_puzzle():
    if SudokuSolverGUI.solving:
        return
    new_board = [[0 for _ in range(9)] for _ in range(9)]
    for box in range(0, 9, 3):
        nums = random.sample(range(1, 10), 9)
        for i in range(3):
            for j in range(3):
                new_board[box+i][box+j] = nums.pop()
    solve_instant(new_board)
    cells_to_remove = random.randint(40, 55)
    removed = 0
    while removed < cells_to_remove:
        row = random.randint(0, 8)
        col = random.randint(0, 8)
        if new_board[row][col] != 0:
            new_board[row][col] = 0
            removed += 1
    SudokuSolverGUI.original_board = copy.deepcopy(new_board)
    SudokuSolverGUI.board = copy.deepcopy(new_board)
    SudokuSolverGUI.update_display()
    SudokuSolverGUI.status_label.config(text="NEW PUZZLE", fg="green")

# ===================== 3. GUI/VISUALIZATION LOGIC =====================
# Handles all GUI (Tkinter) setup, event logic, and visualization.
# ----------------------------------------------------------------------
class SudokuSolverGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Dynamic Sudoku Solver and Generator")
        self.original_board = [
            [5, 3, 0, 0, 7, 0, 0, 0, 0],
            [6, 0, 0, 1, 9, 5, 0, 0, 0],
            [0, 9, 8, 0, 0, 0, 0, 6, 0],
            [8, 0, 0, 0, 6, 0, 0, 0, 3],
            [4, 0, 0, 8, 0, 3, 0, 0, 1],
            [7, 0, 0, 0, 2, 0, 0, 0, 6],
            [0, 6, 0, 0, 0, 0, 2, 8, 0],
            [0, 0, 0, 4, 1, 9, 0, 0, 5],
            [0, 0, 0, 0, 8, 0, 0, 7, 9]
        ]
        self.board = copy.deepcopy(self.original_board)
        self.bg_color = "white"
        self.grid_color = "magenta"
        self.original_num_color = "Black"
        self.solved_num_color = "red"
        self.current_cell_color = "red"
        self.button_bg = "lightgray"
        self.slow_button_color = "lightblue"
        self.generate_button_color = "navajowhite2"
        self.instant_button_color = "lightgreen"
        self.input_button_color = "lightpink"
        self.cell_font = tkfont.Font(family='Arial', size=20, weight='bold')
        self.button_font = tkfont.Font(family='Arial', size=12)
        self.status_font = tkfont.Font(family='Arial', size=12)
        self.solving = False
        self.stop_solving = False
        self.input_mode = False
        self.selected_cell = None
        self.create_widgets()
        self.update_display()

    def create_widgets(self):
        self.grid_frame = tk.Frame(self.root, bg=self.bg_color)
        self.grid_frame.pack(pady=10)
        self.cells = []
        for i in range(9):
            row = []
            for j in range(9):
                cell = tk.Label(self.grid_frame, text="", width=3, height=1, 
                              font=self.cell_font, relief="solid", borderwidth=1,
                              bg=self.bg_color)
                cell.grid(row=i, column=j, ipadx=5, ipady=5)
                cell.bind("<Button-1>", lambda e, i=i, j=j: self.select_cell(i, j))
                if i % 3 == 0:
                    cell.grid(pady=(1.5, 1))
                if j % 3 == 0:
                    cell.grid(padx=(1.5, 1))
                row.append(cell)
            self.cells.append(row)
        self.button_frame = tk.Frame(self.root)
        self.button_frame.pack(pady=10)
        self.slow_button = tk.Button(self.button_frame, text="Slow-Solve", font=self.button_font, bg=self.slow_button_color, command=self.start_slow_solve)
        self.slow_button.grid(row=0, column=0, padx=5)
        self.generate_button = tk.Button(self.button_frame, text="Generate", font=self.button_font, bg=self.generate_button_color, command=generate_puzzle)
        self.generate_button.grid(row=0, column=1, padx=5)
        self.instant_button = tk.Button(self.button_frame, text="Instant-Solve", font=self.button_font, bg=self.instant_button_color, command=self.start_instant_solve)
        self.instant_button.grid(row=0, column=2, padx=5)
        self.input_button = tk.Button(self.button_frame, text="Input", font=self.button_font, bg=self.input_button_color, command=self.toggle_input_mode)
        self.input_button.grid(row=0, column=3, padx=5)
        self.reset_button = tk.Button(self.button_frame, text="Reset", font=self.button_font, bg=self.button_bg, command=self.reset_board)
        self.reset_button.grid(row=1, column=1, pady=10)
        self.clear_button = tk.Button(self.button_frame, text="Clear", font=self.button_font, bg=self.button_bg, command=self.clear_board)
        self.clear_button.grid(row=1, column=2, pady=10)
        self.status_label = tk.Label(self.root, text="", font=self.status_font)
        self.status_label.pack()
        self.root.bind("<Key>", self.handle_key_press)

    def select_cell(self, row, col):
        if self.input_mode and not self.solving:
            if self.selected_cell:
                prev_row, prev_col = self.selected_cell
                self.cells[prev_row][prev_col].config(bg=self.bg_color)
            self.selected_cell = (row, col)
            self.cells[row][col].config(bg="lightblue")
            self.status_label.config(text=f"Selected cell: ({row+1}, {col+1}). Enter a number (1-9) or 0 to clear.", fg="black")

    def handle_key_press(self, event):
        if self.input_mode and self.selected_cell and not self.solving:
            row, col = self.selected_cell
            if event.char.isdigit():
                num = int(event.char)
                if 0 <= num <= 9:
                    if num == 0 or self.is_valid_input(self.board, row, col, num):
                        self.board[row][col] = num
                        self.original_board[row][col] = num
                        self.update_display()
                        self.status_label.config(text=f"Set cell ({row+1}, {col+1}) to {num if num != 0 else 'empty'}", fg="green")
                    else:
                        self.status_label.config(text=f"INVALID NUMBER ON ({row+1}, {col+1})!", fg="red")

    def is_valid_input(self, board, row, col, num):
        if num in board[row] and board[row].index(num) != col:
            return False
        for i in range(9):
            if board[i][col] == num and i != row:
                return False
        box_row, box_col = row // 3 * 3, col // 3 * 3
        for i in range(box_row, box_row + 3):
            for j in range(box_col, box_col + 3):
                if board[i][j] == num and (i != row or j != col):
                    return False
        return True

    def toggle_input_mode(self):
        if self.solving:
            return
        self.input_mode = not self.input_mode
        if self.input_mode:
            self.input_button.config(bg="pink")
            self.status_label.config(text="PUZZLE INPUT KARO !", fg="blue")
            if self.selected_cell:
                row, col = self.selected_cell
                self.cells[row][col].config(bg=self.bg_color)
            self.selected_cell = None
        else:
            self.input_button.config(bg=self.input_button_color)
            if self.selected_cell:
                row, col = self.selected_cell
                self.cells[row][col].config(bg=self.bg_color)
            self.selected_cell = None

    def update_display(board, current_cell=None):
        for i in range(9):
            for j in range(9):
                value = board[i][j]
                original_value = SudokuSolverGUI.original_board[i][j]
                if value != 0:
                    SudokuSolverGUI.cells[i][j].config(text=str(value))
                    if original_value != 0:
                        SudokuSolverGUI.cells[i][j].config(fg=SudokuSolverGUI.original_num_color)
                    else:
                        SudokuSolverGUI.cells[i][j].config(fg=SudokuSolverGUI.solved_num_color)
                    if current_cell and current_cell == (i, j):
                        SudokuSolverGUI.cells[i][j].config(bg="yellow")
                    elif SudokuSolverGUI.selected_cell and SudokuSolverGUI.selected_cell == (i, j) and SudokuSolverGUI.input_mode:
                        SudokuSolverGUI.cells[i][j].config(bg="lightblue")
                    else:
                        SudokuSolverGUI.cells[i][j].config(bg=SudokuSolverGUI.bg_color)
                else:
                    SudokuSolverGUI.cells[i][j].config(text="", bg=SudokuSolverGUI.bg_color)
                    if current_cell and current_cell == (i, j):
                        SudokuSolverGUI.cells[i][j].config(bg="yellow")
                    elif SudokuSolverGUI.selected_cell and SudokuSolverGUI.selected_cell == (i, j) and SudokuSolverGUI.input_mode:
                        SudokuSolverGUI.cells[i][j].config(bg="lightblue")
        SudokuSolverGUI.root.update()

    def start_slow_solve(self):
        if not self.solving:
            self.solving = True
            self.stop_solving = False
            self.input_mode = False
            self.input_button.config(bg=self.input_button_color)
            self.status_label.config(text="SOLVING SLOWLY ...", fg="black")
            self.disable_buttons()
            solving_board = copy.deepcopy(self.original_board)
            self.board = solving_board
            self.root.after(100, lambda: self.run_solver(0.1, False))

    def start_instant_solve(self):
        if not self.solving:
            self.solving = True
            self.stop_solving = False
            self.input_mode = False
            self.input_button.config(bg=self.input_button_color)
            self.status_label.config(text="SOLVING INSTANTLY...", fg="black")
            self.disable_buttons()
            solving_board = copy.deepcopy(self.original_board)
            self.board = solving_board
            self.root.after(100, lambda: self.run_solver(0, True))

    def run_solver(self, delay, instant_mode):
        if solve_sudoku_visual(self.board, delay, instant_mode):
            self.status_label.config(text="Solved!", fg="green")
        else:
            self.status_label.config(text="No solution!", fg="red")
        self.update_display()
        self.solving = False
        self.enable_buttons()

    def reset_board(self):
        if not self.solving:
            self.board = copy.deepcopy(self.original_board)
            self.update_display()
            self.status_label.config(text="BOARD RESET !", fg="green")
            self.stop_solving = True
            self.input_mode = False
            self.input_button.config(bg=self.input_button_color)
            if self.selected_cell:
                row, col = self.selected_cell
                self.cells[row][col].config(bg=self.bg_color)
            self.selected_cell = None

    def clear_board(self):
        if not self.solving:
            self.original_board = [[0 for _ in range(9)] for _ in range(9)]
            self.board = copy.deepcopy(self.original_board)
            self.update_display()
            self.status_label.config(text="BOARD CLEAR. PUZZLE INPUT KARO", fg="green")
            self.stop_solving = True
            self.input_mode = True
            self.input_button.config(bg="pink")
            if self.selected_cell:
                row, col = self.selected_cell
                self.cells[row][col].config(bg=self.bg_color)
            self.selected_cell = None

    def disable_buttons(self):
        self.slow_button.config(state="disabled")
        self.generate_button.config(state="disabled")
        self.instant_button.config(state="disabled")
        self.input_button.config(state="disabled")
        self.reset_button.config(state="disabled")
        self.clear_button.config(state="disabled")

    def enable_buttons(self):
        self.slow_button.config(state="normal")
        self.generate_button.config(state="normal")
        self.instant_button.config(state="normal")
        self.input_button.config(state="normal")
        self.reset_button.config(state="normal")
        self.clear_button.config(state="normal")

if __name__ == "__main__":
    root = tk.Tk()
    app = SudokuSolverGUI(root)
    root.mainloop()
