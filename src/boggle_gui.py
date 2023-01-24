import tkinter as tk
from typing import List, Tuple, Callable

Board = List[List[str]]
Cell = Tuple[int, int]

BUTTON_HOVER_COLOR = 'gray'
REGULAR_COLOR = 'lightgray'
BUTTON_ACTIVE_COLOR = 'slateblue'
BUTTON_HIGHLIGHT_COLOR = 'orange'

TEXT_FONT = ("Courier", 30)

BUTTON_STYLE = {
    "font": TEXT_FONT,
    "borderwidth": 1,
    "relief": tk.RAISED,
    "bg": REGULAR_COLOR,
    "activebackground": BUTTON_ACTIVE_COLOR
}

class BoggleGui:

    def __init__(self, board: Board):
        root = tk.Tk()
        root.title('Boggle')
        root.geometry("640x480")
        root.resizable(False, False)
        self._main_window = root
        
        self._outer_frame = tk.Frame(self._main_window, bg=REGULAR_COLOR, highlightbackground=REGULAR_COLOR, highlightthickness=5)
        self._outer_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self._current_word_label = tk.Label(self._outer_frame, font=TEXT_FONT, bg=REGULAR_COLOR, height=2, relief=tk.RIDGE)
        self._current_word_label.pack(side=tk.TOP, fill=tk.BOTH)

        self._main_container = tk.Frame(self._outer_frame)
        self._main_container.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self._board = tk.Frame(self._main_container)
        self._board.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self._button_panel = tk.Frame(self._main_container)
        self._button_panel.pack(side=tk.BOTTOM, fill=tk.BOTH)

        self._submit_button = tk.Button(self._button_panel, text="Submit", font=('Courier', 20))
        self._submit_button.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self._reset = tk.Button(self._button_panel, text="Reset", height=2)
        self._reset.pack(side=tk.LEFT, fill=tk.Y)

        self._cells = dict()
        self._initialize_board(board)

        self._sidebar = tk.Frame(self._outer_frame)
        self._sidebar.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self._score_label = tk.Label(self._sidebar, font=TEXT_FONT, bg=REGULAR_COLOR, relief=tk.RIDGE)
        self._score_label.pack(side=tk.TOP, fill=tk.X)

        self._completed_words = tk.StringVar()
        self._completed_words_label = tk.Label(self._sidebar, font=("Courier", 12), bg=REGULAR_COLOR, relief=tk.RIDGE, textvariable=self._completed_words)
        self._completed_words_label.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self._timer = tk.Label(self._sidebar, font=('Courier', 30), bg=REGULAR_COLOR, relief=tk.RIDGE)
        self._timer.pack(side=tk.BOTTOM, fill=tk.X)


    def _initialize_board(self, board: Board):
        for i, row in enumerate(board):
            for j, cell_text in enumerate(row):
                self._board.grid_rowconfigure(i, weight=1)
                self._board.grid_columnconfigure(j, weight=1)
                self._make_cell((i,j), cell_text)
    
    def _make_cell(self, coordinates: Cell, text: str):
        button = tk.Button(self._board, text=text, **BUTTON_STYLE)

        def _on_enter(event):
            if button['background'] != BUTTON_ACTIVE_COLOR:
                button['background'] = BUTTON_HOVER_COLOR
        button.bind("<Enter>", _on_enter)

        def _on_leave(event):
            if button['background'] != BUTTON_ACTIVE_COLOR:
                button['background'] = REGULAR_COLOR
        button.bind("<Leave>", _on_leave)
        
        button.grid(row=coordinates[0], column=coordinates[1], sticky=tk.NSEW)
        self._cells[coordinates] = button

    def _update_cell_active(self, cell: Cell, activate: bool):
        self._cells[cell]['background'] = BUTTON_ACTIVE_COLOR if activate else REGULAR_COLOR

    def set_path(self, path: List[Cell]):
        for cell in self._cells:
            self._update_cell_active(cell, cell in path)

    def set_current_word(self, word: str):
        self._current_word_label["text"] = word
    
    def set_score(self, score: int):
        self._score_label["text"] = str(score)

    def start_timer(self, time=180):
        self._timer['text'] = time
        self._main_window.after(1000, self.start_timer(time-1))
    def set_cell_command(self, cell_coordinates: Cell, command: Callable[[], None]):
        self._cells[cell_coordinates].configure(command=command)

    def get_cell_coordinates(self) -> List[Cell]:
        return list(self._cells.keys())

    def run(self):
        self._main_window.mainloop()


if __name__ == "__main__":
    board = [
        ['a', 'b', 'c', 'd'],
        ['a', 'b', 'c', 'd'],
        ['a', 'b', 'c', 'd'],
        ['a', 'b', 'c', 'd']
    ]
    b = BoggleGui(board)
    b.run()
