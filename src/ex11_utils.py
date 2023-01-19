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
    if n < 1:
        return
    for i, row in enumerate(board):
        for j in range(len(row)):
            find_length_n_paths_helper([(i,j)], n, board, words)


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


    if paths_found is None:
        paths_found = []
    if not is_valid_path(board, current_path, words):
        return paths_found
    if len(current_path) == max_length:
        paths_found.append(current_path)
        return paths_found
    for i in range(-1,2):
        for j in range(-1,2):
            if (i,j) in current_path:
                continue
            
            find_length_n_paths_helper(current_path + [(i,j)], max_length, board, words, paths_found)





