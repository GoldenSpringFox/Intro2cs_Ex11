from boggle_gui import BoggleGui
from boggle_model import BoggleModel
from boggle_board_randomizer import randomize_board
from ex11_utils import Cell

class BoggleController:
    def __init__(self) -> None:
        board = randomize_board()
        with open('boggle_dict.txt', 'r') as f:
            words = f.readlines()

        self.__model = BoggleModel(board, words)
        self.__gui = BoggleGui(board)

        for cell in self.__gui.get_button_coordinates():
            action = self.create_button_action(cell)
            self.__gui.set_button_command(cell, action)
        self.__gui.set_display(self.__model.current_word)
        submit_cmd = self.submit_button()
        self.__gui.set_cmd_for_submit(submit_cmd)

    def submit_button(self):
        def submit():
            if self.__model.submit():
                self.__gui.submited(True)
            else:
                self.__gui.submited(False)
        return submit
    def create_button_action(self, cell: Cell):
        def action():
            if self.__gui.check_bg(cell):
                self.__model.soft_path_update(cell)
                self.__gui.set_display(self.__model.current_word)
        
        return action

    def run(self):
        self.__gui.run()


if __name__ == "__main__":
    BoggleController().run()
