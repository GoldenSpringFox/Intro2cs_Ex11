from boggle_gui import BoggleGui
from boggle_model import BoggleModel
from boggle_board_randomizer import randomize_board

class BoggleController:
    def __init__(self) -> None:
        board = randomize_board()
        with open('boggle_dict.txt', 'r') as f:
            words = f.readlines()

        self.__gui = BoggleGui()
        self.__model = BoggleModel(board, words)


if __name__ == "__main__":
    BoggleController().run()
