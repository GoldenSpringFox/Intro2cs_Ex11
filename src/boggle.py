from gui.boggle_gui import BoggleGui
from boggle_model import BoggleModel

class BoggleController:
    def __init__(self) -> None:
        self.__gui = BoggleGui()
        self.__model = BoggleModel()


if __name__ == "__main__":
    BoggleController.run()
