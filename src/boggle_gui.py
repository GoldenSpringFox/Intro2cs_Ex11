import tkinter as tk


class BoggleGui:

    def __init__(self, board):
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
        self.__board = board
        self.__btn_dct = {}
        row = 0
        for _ in self.__board:
            col = 0
            for letter in _:
                self.__btn_dct[(row,col)] = tk.Button(self.__game, text=str(letter), bg='white', width=8, height=2)
                col += 1
            row += 1
        lst = []
        for i in self.__btn_dct.values():
            lst.append(i)
        inx = lst[:]
        for j in range(0, 280, 70):
            for i in range(0, 240, 60):
                buttons_canvas = self.__canvas2.create_window(40 + j, 160 + i,
                                                              anchor="nw",
                                                              window=inx[0])
                del inx[0]
        self.__command_dct = {}

        self.__boggle_text = tk.Text(self.__game, height=1, width=30)
        self.__canvas2.create_window(50, 40,
                                     anchor="nw",
                                     window=self.__boggle_text)

        self.__clear_button = tk.Button(self.__game, text='clear answer', width=10, height=2, bg='grey', fg='red',
                                        command=self._clear)
        self.__canvas2.create_window(300, 40,
                                     anchor="nw",
                                     window=self.__clear_button)
        self.__submit_btn = tk.Button(self.__game, text='submit answer', width=10, height=2, bg='grey', fg='red')
        self.__canvas2.create_window(300, 90,
                                     anchor="nw",
                                     window=self.__submit_btn)
        self.__sub_label = tk.Label(self.__game, text='', height=1, width=20)
        self.__canvas2.create_window(50, 70,
                                     anchor="nw",
                                     window=self.__sub_label)

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


    def get_button_coordinates(self):
        lst = []
        for i in self.__btn_dct:
            lst.append(i)
        return lst

    def _clear(self):
        self.__boggle_text.delete("1.0", "end")
        for btn in self.__btn_dct.values():
            btn.config(bg='white')

    def check_bg(self, cell):
        btn = self.__btn_dct[cell]
        if btn['bg'] == 'green':
            return True
        return False
    def set_display(self, word):
        if len(word) == 0:
            pass
        else:
            self.__boggle_text.insert(tk.INSERT, word[-1])

    def set_button_command(self, cell, command):
        btn = self.__btn_dct[cell]
        self.__command_dct[btn] = command
        btn.config(command=lambda : [self._add_to_lst(btn),command()])

    def _add_to_lst(self, button):
        if button['bg'] == 'green':
            button.config(bg='white')
        else:
            button.config(bg='green')

    def set_cmd_for_submit(self, command):
        self.__submit_btn.config(command=command)
    def _clear_label(self):
        self.__sub_label['text'] = ''

    def submited(self, bool):
        if bool:
            self._clear()
            self.__sub_label.config(fg='green')
            self.__sub_label['text'] = 'correct word!'
            self.__game.after(2000, self._clear_label)
        else:
            self._clear()
            self.__sub_label.config(fg='red')
            self.__sub_label['text'] = 'try another word'
            self.__game.after(2000, self._clear_label)




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

    def run(self):
        self.__root.mainloop()


# b = BoggleGui(boggle_board_randomizer.randomize_board())
# b.start()
