from functools import reduce
from ex11_utils import *
from boggle_board_randomizer import randomize_board

class BoggleModel:
    def __init__(self, board: Board, words: Iterable[str], current_path: Path = None) -> None:
        self.__board = board
        self.__words = words
        self.__current_path: Path = current_path if current_path else []
        self.__score = 0
        self.__completed_words = []

    @property
    def score(self):
        return self.__score
    
    def _add_score(self, word: str):
        self.__score += len(word) ** 2

    @property
    def current_path(self):
        return self.__current_path
    
    @property
    def current_word(self):
        return reduce(lambda word,cell: word + self.__board[cell[0]][cell[1]], self.current_path, "")

    def reset_path(self):
        self.__current_path = []

    def _is_valid_word(self, word: str):
        return word in self.__words and word not in self.__completed_words

    def is_current_path_valid_word(self):
        word = is_valid_path(self.__board, self.__current_path)
        return self._is_valid_word(word)

    def submit(self) -> bool:
        word = is_valid_path(self.__board, self.__current_path)
        self.reset_path()
        if self._is_valid_word(word):
            self.__completed_words.append(word)
            self._add_score(word)
            return True
        return False

    def forced_path_update(self, cell: Cell):
        if cell in self.__current_path:
            if cell == self.__current_path[-1]:
                self.__current_path.pop()
            else:
                index = self.__current_path.index(cell)
                self.__current_path = self.__current_path[:index+1]
            return True
        
        new_path = self.__current_path + [cell]
        if is_valid_path(self.__board, new_path, None):
            self.__current_path = new_path
            return True
        
        return False
        

    def soft_path_update(self, cell: Cell) -> bool:
        if len(self.__current_path) >= 2 and cell == self.__current_path[-2]:
            self.__current_path.pop()
            return True

        new_path = self.__current_path + [cell]
        if is_valid_path(self.__board, new_path, None):
            self.__current_path = new_path
            return True
        
        return False
        
        