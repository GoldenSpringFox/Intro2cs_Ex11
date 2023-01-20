########################################
#              Imports                 #
########################################

from functools import reduce
from typing import List, Tuple, Iterable, Optional

########################################
#          Constants / Types           #
########################################

Board = List[List[str]]
Cell = Tuple[int, int]
Path = List[Cell]

########################################
#            Public Methods            #
########################################

def is_valid_path(board: Board, path: Path, words: Iterable[str]) -> Optional[str]:
    board_height = len(board)
    board_width = len(board[0])

    word = ""
    for i, current_cell in enumerate(path):
        if not _are_cells_on_board(board_height, board_width, current_cell) or \
            not _are_cells_sequencially_touching(*path[i:i+2]) or \
            _is_cell_repeating(*path[i:]):
            return
        word += board[current_cell[0]][current_cell[1]]
    

    return word if words is None or word in words else None


def find_length_n_paths(n: int, board: Board, words: Iterable[str]) -> List[Path]:
    paths = []
    if n < 1:
        return paths
    
    for i, row in enumerate(board):
        for j in range(len(row)):
            paths += _find_paths_for_words([(i,j)], n-1, board, words)
    
    return paths


def find_length_n_words(n: int, board: Board, words: Iterable[str]) -> List[Path]:
    length_n_words = list(filter(lambda word: len(word) == n, words))
    return find_length_n_paths(n, board, length_n_words)


def max_score_paths(board: Board, words: Iterable[str]) -> List[Path]:
    # the current implementation relies on the fact that score is uniquely identified by the word's length
    word_lengths = list(set(map(lambda word: len(word), words)))
    word_lengths.sort(reverse=True)
    paths = []
    if word_lengths is None:
        return paths
    
    for length in word_lengths:
        paths += find_length_n_paths(length, board, words)
        if len(paths) > 0:
            return paths
    return paths



########################################
#           Private Methods            #
########################################

# --------------------- #
# --- is_valid_path --- #
# --------------------- #

def _are_cells_on_board(board_height: int, board_width: int, *cells: Cell):
    return all((0 <= cell[0] < board_height) and (0 <= cell[1] < board_width) for cell in cells)

def _are_cells_sequencially_touching(*cells: Cell):
    for i in range(len(cells) - 1):
        if (abs(cells[i][0] - cells[i+1][0]) > 1) or (abs(cells[i][1] - cells[i+1][1]) > 1):
            return False
    return True

def _is_cell_repeating(*cells: Cell):
    for i in range(len(cells)):
        if cells[i] in cells[i+1:]:
            return True
    return False


# --------------------------- #
# --- find_length_n_paths --- #
# --------------------------- #

def _find_paths_for_words(current_path: Path, remaining_cells: int, board: Board, words: Iterable[str], paths_found: List[Path] = None) -> List[Path]:
    if paths_found is None:
        paths_found = []
    
    word = is_valid_path(board, current_path, None)
    if word is None:
        return paths_found
    
    words = _get_words_with_prefix(word, words)    
    if remaining_cells == 0:
        for word in words:
            paths_found.append(current_path)
        return paths_found
    
    for cell in _get_surrounding_cells(current_path[-1]):
        _find_paths_for_words(current_path + [cell], remaining_cells - 1, board, words, paths_found)
    
    return paths_found


def _get_words_with_prefix(prefix: str, words: Iterable[str]) -> List[str]:
    return list(filter(lambda word: prefix == word[:len(prefix)], words))

def _get_surrounding_cells(cell: Cell) -> List[Cell]:
    return [(cell[0] + i, cell[1] + j) for i in range(-1,2) for j in range(-1,2) if not i == j == 0]


# ----------------------- #
# --- max_score_paths --- #
# ----------------------- #

def _word_score(word):
    return len(word) ** 2
