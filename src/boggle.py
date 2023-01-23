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

        for cell in self._gui.get_button_coordinates():
            action = self.create_button_action(cell)
            self.__gui.set_button_command(cell, action)
        self.__gui.set_display(self.__model.current_word)
    
    def create_button_action(self, cell: Cell):
        def action():
            self.__model.soft_path_update(cell)
            self.__gui.set_display(self.__model.current_word)
        
        return action

    def run(self):
        self.__gui.run()


if __name__ == "__main__":
    BoggleController().run()
