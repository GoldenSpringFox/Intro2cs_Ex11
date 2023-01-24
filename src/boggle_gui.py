import tkinter as tk
from typing import List, Tuple, Callable

Board = List[List[str]]
Cell = Tuple[int, int]

SECONDS_IN_MINUTE = 60

BACKGROUND = '#2A2D2D'
BUTTON_HOVER_COLOR = 'gray'
REGULAR_COLOR = 'lightgray'
BUTTON_ACTIVE_COLOR = '#577D7D'
BUTTON_HIGHLIGHT_COLOR = 'orange'
TEXT_FONT = ("Courier", 30)
BUTTON_STYLE = {
    "font": TEXT_FONT,
    "borderwidth": 1,
    "relief": tk.RAISED,
    "bg": REGULAR_COLOR,
    "activebackground": BUTTON_ACTIVE_COLOR
}
FRAME_STYLE = {
    "font": ("Courier", 12), 
    "background": BACKGROUND,
    "foreground": 'white',
    "highlightbackground": REGULAR_COLOR, 
    "highlightcolor": REGULAR_COLOR,
    "highlightthickness": 5,
    "relief":tk.FLAT
}

class BoggleGui:

    def __init__(self, board: Board, time: int = -1):
        self._time_remaining = time

        root = tk.Tk()
        root.title('Boggle')
        root.geometry("720x540")
        root.resizable(False, False)
        self._main_window = root
        
        self._outer_frame = tk.Frame(self._main_window, bg=BACKGROUND, padx=10, pady=10)
        self._outer_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self._current_word_label = tk.Label(self._outer_frame, font=TEXT_FONT, bg=REGULAR_COLOR, height=2, relief=tk.RIDGE)
        self._current_word_label.pack(side=tk.TOP, fill=tk.BOTH, padx=(10,0))

        self._main_container = tk.Frame(self._outer_frame, background=BACKGROUND)
        self._main_container.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self._board = tk.Frame(self._main_container, background=BACKGROUND)
        self._board.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=10, pady=10)

        self._button_panel = tk.Frame(self._main_container)
        self._button_panel.pack(side=tk.BOTTOM, fill=tk.BOTH, padx=10, pady=(5,0))

        self._submit_button = tk.Button(self._button_panel, text="Submit", font=('Courier', 20))
        self._submit_button.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self._reset_button = tk.Button(self._button_panel, text="Reset", height=2)
        self._reset_button.pack(side=tk.LEFT, fill=tk.Y)

        self._cells: dict[Cell, tk.Button] = dict()
        self._initialize_board(board)

        self._sidebar = tk.Frame(self._outer_frame)
        self._sidebar.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        self._sidebar.pack_propagate(False)

        self._score_label = tk.Label(self._sidebar, font=TEXT_FONT, bg=REGULAR_COLOR, relief=tk.RIDGE)
        self._score_label.pack(side=tk.TOP, fill=tk.X)

        self._completed_words = tk.StringVar()
        self._completed_words_label = tk.Label(self._sidebar, FRAME_STYLE, textvariable=self._completed_words)
        self._completed_words_label.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        
        self._timer_label = tk.Label(self._sidebar, font=('Courier', 20), bg=REGULAR_COLOR, relief=tk.RIDGE)
        self._timer_label.pack(side=tk.BOTTOM, fill=tk.X)

        self._create_welcome_screen(root)

        self._main_window.withdraw()
    
    def _create_welcome_screen(self, root):
        self._start_window = tk.Toplevel(root)
        self._bg = tk.PhotoImage(file='./images/boggle_start.png')
        self._canvas = tk.Canvas(self._start_window, width=640,
                                  height=480)
        self._canvas.create_image(0, 0, image=self._bg,
                                   anchor="nw")
        self._button = tk.Button(self._start_window, text='Sandbox', font=('Courier', 20), command=self._set_start_button)
        self._canvas.create_window(120, 350,
                                    anchor="nw",
                                    window=self._button)
        self._timed_button = tk.Button(self._start_window, text='timed', font=('Courier', 20), command=self._set_timed_button)
        self._canvas.create_window(400, 350,
                                   anchor="nw",
                                   window=self._timed_button)
        self._canvas.pack()

    def _show_end_screen(self, root):
        self._finish_screen = tk.Toplevel(root)
        self._finish_screen.geometry("640x480")
        self._finish_screen['bg'] = REGULAR_COLOR
        self._final_score = tk.Label(self._finish_screen, text='your final score is: ' + str(self._score_label['text']),
                                     font=('Courier', 20),
                                     height=2, width=60,
                                     bg='lightgrey')
        self._final_score.pack(side=tk.TOP, fill=tk.BOTH)
        self._show_completed_words = tk.Label(self._finish_screen, textvariable=self._completed_words,
                                              font=('Courier', 15),
                                              height=15, width=30,
                                              bg='lightgrey')
        self._show_completed_words.pack(side=tk.LEFT, fill=tk.BOTH)
        self._btn_frame = tk.Frame(self._finish_screen, bg=REGULAR_COLOR, highlightbackground=REGULAR_COLOR, highlightthickness=5)
        self._btn_frame.pack(fill=tk.BOTH)
        self._restart_btn = tk.Button(self._btn_frame, text='restart', font=('Courier', 20),
                                                                command=self._set_restart_button)
        self._restart_btn.pack(side=tk.TOP, fill=tk.BOTH)
        self._quit_button = tk.Button(self._btn_frame, text='quit', font=('Courier', 20), command=self.quit)
        self._quit_button.pack(side=tk.BOTTOM, fill=tk.BOTH)
        self.fill = tk.Frame(self._finish_screen, bg=REGULAR_COLOR)
        self.fill.pack()




    def _initialize_board(self, board: Board):
        for i, row in enumerate(board):
            for j, cell_text in enumerate(row):
                self._board.grid_rowconfigure(i, weight=1)
                self._board.grid_columnconfigure(j, weight=1)
                self._make_cell((i,j), cell_text)
    
    def _make_cell(self, coordinates: Cell, text: str):
        button = tk.Button(self._board, text=text, **BUTTON_STYLE)

        def _on_enter(event):
            if button['background'] not in [BUTTON_ACTIVE_COLOR, BUTTON_HIGHLIGHT_COLOR]:
                button['background'] = BUTTON_HOVER_COLOR
        button.bind("<Enter>", _on_enter)

        def _on_leave(event):
            if button['background'] not in [BUTTON_ACTIVE_COLOR, BUTTON_HIGHLIGHT_COLOR]:
                button['background'] = REGULAR_COLOR
        button.bind("<Leave>", _on_leave)
        
        button.grid(row=coordinates[0], column=coordinates[1], sticky=tk.NSEW)
        self._cells[coordinates] = button

    # button commands
    def set_cell_command(self, cell_coordinates: Cell, command: Callable[[], None]):
        self._cells[cell_coordinates].configure(command=command)

    def set_submit_command(self, command: Callable[[], None]):
        self._submit_button.configure(command=command)

    def set_reset_command(self, command: Callable[[], None]):
        self._reset_button.configure(command=command)

    def _set_restart_button(self):
        self._finish_screen.withdraw()
        self._main_window.deiconify()
        self._time_remaining = 180
        self.start_timer()
        self._score_label['text'] = '0'
        self._completed_words = tk.StringVar()

    def _set_start_button(self):
        self._start_window.withdraw()
        self._main_window.deiconify()
        self.start_timer()

    def _set_timed_button(self):
        self._time_remaining = 180
        self._set_start_button()

    # setters / getters
    def _update_cell_color(self, cell: Cell, activate: bool, is_path_valid_word: bool):
        self._cells[cell]['background'] = REGULAR_COLOR if not activate else BUTTON_HIGHLIGHT_COLOR if is_path_valid_word else BUTTON_ACTIVE_COLOR

    def set_path(self, path: List[Cell], is_path_valid_word = False):
        for cell in self._cells:
            self._update_cell_color(cell, cell in path, is_path_valid_word)

    def set_current_word(self, word: str):
        self._current_word_label["text"] = word
    
    def set_score(self, score: int):
        self._score_label["text"] = str(score)

    def get_cell_coordinates(self) -> List[Cell]:
        return list(self._cells.keys())

    def add_correct_word(self, word: str):
        self._completed_words.set(self._completed_words.get() + f"\n{word}")

    # timer
    def display_time(self):
        return "Unlimited" if self._time_remaining < 0 else f"{self._time_remaining // SECONDS_IN_MINUTE}:{str(self._time_remaining % SECONDS_IN_MINUTE).zfill(2)}"

    def start_timer(self):
        if self._time_remaining == 0:
            self._show_end_screen(self._main_window)
            return
        self._timer_label.configure(text=self.display_time())
        self._time_remaining -= 1
        self._main_window.after(1000, self.start_timer)

    def quit(self):
        self._main_window.destroy()

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
