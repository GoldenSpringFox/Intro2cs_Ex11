from boggle_gui import BoggleGui
from boggle_model import BoggleModel
from boggle_board_randomizer import randomize_board
from ex11_utils import Cell
import random

class BoggleController:
    def __init__(self) -> None:
        board = randomize_board()
        with open('boggle_dict.txt', 'r') as f:
            words = [line.rstrip() for line in f]

        self.__model = BoggleModel(board, words)
        self.__gui = BoggleGui(board)

        for cell in self.__gui.get_cell_coordinates():
            action = self.create_button_action(cell)
            self.__gui.set_cell_command(cell, action)
        
        self.__gui.set_submit_command(self.create_submit_action())
        self.__gui.set_reset_command(self.create_reset_action())
        self.__gui.set_hint_command(self.create_hint_action())

        self.__gui.set_current_word(self.__model.current_word)
        self.__gui.set_score(self.__model.score)
    
    def create_button_action(self, cell: Cell):
        def action():
            successful = self.__model.forced_path_update(cell)
            if successful:
                self.__gui.set_path(self.__model.current_path, self.__model.is_current_path_valid_word())
                self.__gui.set_current_word(self.__model.current_word)
        return action
    
    def create_reset_action(self):
        def action():
            self.__model.reset_path()
            self.__gui.set_path(self.__model.current_path)
            self.__gui.set_current_word(self.__model.current_word)
        return action

    def create_submit_action(self):
        def action():
            word = self.__model.current_word
            successful = self.__model.submit()
            if successful:
                self.__gui.add_correct_word(word)
            self.__gui.set_path(self.__model.current_path)
            self.__gui.set_current_word(self.__model.current_word)
            self.__gui.set_score(self.__model.score)
        return action
    
    def create_hint_action(self):
        def action():
            possible_paths = self.__model.all_possible_paths
            if not possible_paths:
                self.__gui.set_current_word("Found all words!")
                return
            self.__gui.set_current_word(self.__model.get_word_from_path(random.choice(possible_paths)))
        return action

    def run(self):
        self.__gui.run()


if __name__ == "__main__":
    BoggleController().run()
