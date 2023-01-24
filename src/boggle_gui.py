import tkinter as tk
import boggle_board_randomizer

class BoggleGui:

    def __init__(self):
        self.__root = tk.Tk()
        self.__root.title('Boggle')
        self._image1 = tk.PhotoImage(file='./images/Boogle.png')
        self.__canvas = tk.Canvas(self.__root, width=400,
                                  height=400)
        self.__canvas.create_image(0, 0, image=self._image1,
                                   anchor="nw")
        self.__button = tk.Button(self.__root, text='Start', font=('Comic Sans MS', 20), command=self._start_game)
        button_canvas = self.__canvas.create_window(150, 300,
                                                    anchor="nw",
                                                    window=self.__button)
        self.__canvas.pack()

        self.__game = tk.Toplevel()
        self.__game.title("Boggle")
        self.__image2 = tk.PhotoImage(file='./images/board3.png')
        self.__canvas2 = tk.Canvas(self.__game, width=400,
                                   height=400)
        self.__canvas2.create_image(0, 0, image=self.__image2,
                                    anchor="nw")
        self.__canvas2.pack()
        self.__game.withdraw()
        board = boggle_board_randomizer.randomize_board()
        self.__btn_lst = []

        for _ in board:
            for letter in _:
                self.__btn_lst.append(tk.Button(self.__game, text=str(letter), bg='white', width=8, height=2))
        inx = self.__btn_lst[:]
        for j in range(0, 280, 70):
            for i in range(0, 240, 60):
                buttons_canvas = self.__canvas2.create_window(40 + j, 160 + i,
                                                              anchor="nw",
                                                              window=inx[0])
                del inx[0]

        for btn in self.__btn_lst:
            btn.config(command=lambda button=btn, letter=btn['text']: self._add_to_lst(letter, button))

        self.__boggle_list = []
        self.__boggle_text = tk.Text(self.__game, height=1, width=30)
        self.__canvas2.create_window(50, 40,
                                     anchor="nw",
                                     window=self.__boggle_text)

        self.__clear_button = tk.Button(self.__game, text='clear answer', width=10, height=2, bg='grey', fg='red',
                                        command=self._clear)
        self.__canvas2.create_window(300, 40,
                                     anchor="nw",
                                     window=self.__clear_button)

        self.__countdown = tk.Label(self.__game, font='Arial', text='')
        self.__countdown.pack()
        self.__lose_screen = tk.Toplevel()
        self.__lose_screen.title('Boggle')
        self.__image_lose = tk.PhotoImage(file='./images/lose.png')
        self.__canvas3 = tk.Canvas(self.__lose_screen, width=360,
                                   height=360)
        self.__canvas3.create_image(0, 0, image=self.__image_lose,
                                    anchor="nw")
        self.__canvas3.pack()
        self.__lose_screen.withdraw()
        self.__restart_button = tk.Button(self.__lose_screen, text='Restart?', command=self._restart_game, width=12,
                                          height=3)
        buttons_restart = self.__canvas3.create_window(80, 300,
                                                       anchor="nw",
                                                       window=self.__restart_button)
        self.__quit_button = tk.Button(self.__lose_screen, text='Quit?', command=self._quit, width=12, height=3)
        buttons_quit = self.__canvas3.create_window(220, 300,
                                                    anchor="nw",
                                                    window=self.__quit_button)

    def _start_game(self):
        self.__root.withdraw()
        self._openNewWindow()
        self._clock(180)

    def _openNewWindow(self):
        self.__game.deiconify()

    def _clear(self):
        self.__boggle_list = []
        self.__boggle_text.delete("1.0", "end")
        for btn in self.__btn_lst:
            btn.config(bg='white')


    def _add_to_lst(self, letter, button):
        if button['bg'] == 'green':
            button.config(bg='white')
            del self.__boggle_list[-1]
        else:
            self.__boggle_list.append(letter)
            button.config(bg='green')
        self.__boggle_text.delete("1.0", "end")
        for ltr in self.__boggle_list:
            self.__boggle_text.insert(tk.INSERT, ltr)

    def _lost(self):
        self.__game.withdraw()
        self.__lose_screen.deiconify()

    def _restart_game(self):
        self.__root.deiconify()
        self._start_game()

    def _quit(self):
        self.__root.destroy()

    def _clock(self, time):
        self.__countdown.configure(text='time left: ' + str(time))
        if time >= 0:
            self.__game.after(1000, self._clock, time - 1)
        else:
            self._lost()

    def start(self):
        self.__root.mainloop()


if __name__ == "__main__":
    b = BoggleGui()
    b.start()
