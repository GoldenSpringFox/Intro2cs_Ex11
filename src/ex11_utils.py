########################################
#              Imports                 #
########################################

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


def get_word_from_path(board: Board, path: Path):
    return is_valid_path(board, path, None)


def find_length_n_paths(n: int, board: Board, words: Iterable[str]) -> List[Path]:
    paths = _find_paths_for_words(board, words, n)
    return list(filter(lambda path: len(path) == n, paths))


def find_length_n_words(n: int, board: Board, words: Iterable[str]) -> List[Path]:
    length_n_words = list(filter(lambda word: len(word) == n, words))
    return _find_paths_for_words(board, length_n_words, n)


def max_score_paths(board: Board, words: Iterable[str]) -> List[Path]:
    paths = _find_paths_for_words(board, words)
    if not paths:
        return []
    paths = _unique_path_per_word(board, paths)
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

def _find_paths_for_words(board: Board, words: Iterable[str], max_path_length: int = -1, current_path: Path = None, paths_found: List[Path] = None) -> List[Path]:
    # Initialize dynamic arguments
    if current_path is None:
        return [path for i, row in enumerate(board) for j in range(len(row)) for path in _find_paths_for_words(board, words, max_path_length - 1, [(i,j)])] if max_path_length != 0 else []
    
    if paths_found is None:
        paths_found = []
    
    # Break conditions
    word = get_word_from_path(board, current_path)
    if not word:
        return paths_found
    
    words = _get_words_with_prefix(word, words)
    if not words:
        return paths_found
    
    if word in words:
        paths_found.append(current_path)
    
    if max_path_length == 0:
        return paths_found

    # Recursive calls
    for cell in _get_surrounding_cells(current_path[-1]):
        _find_paths_for_words(board, words, max_path_length - 1, current_path + [cell], paths_found)
    
    return paths_found


def _get_words_with_prefix(prefix: str, words: Iterable[str]) -> List[str]:
    return list(filter(lambda word: prefix == word[:len(prefix)], words))

def _get_surrounding_cells(cell: Cell) -> List[Cell]:
    return [(cell[0] + i, cell[1] + j) for i in range(-1,2) for j in range(-1,2) if not i == j == 0]


# ----------------------- #
# --- max_score_paths --- #
# ----------------------- #

def _path_score(path: Path):
    return len(path) ** 2

def _unique_path_per_word(board: Board, paths: List[Path]) -> List[Path]:
    word_path_dict = {}
    for path in paths:
        word = get_word_from_path(board, path)
        if word not in word_path_dict:
            word_path_dict[word] = path
    return list(word_path_dict.values())