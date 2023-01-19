from functools import reduce
from typing import List, Tuple, Iterable, Optional

Board = List[List[str]]
Path = List[Tuple[int, int]]


def is_valid_path(board: Board, path: Path, words: Iterable[str]) -> Optional[str]:
    for i in range(len(path)):
        if not ((0 <= path[i][0] <= 3) and (0 <= path[i][1] <= 3)):
            return
        
        if i == len(path) - 1:
            continue
        if (abs(path[i][0] - path[i+1][0]) > 1) or (abs(path[i][1] - path[i+1][1]) > 1):
            return
    
    word = reduce(lambda word,cell: word + board[cell[0]][cell[1]], path, '')
    if word in words:
        return True    


def find_length_n_paths(n: int, board: Board, words: Iterable[str]) -> List[Path]:
    if n < 1:
        return
    for i, row in enumerate(board):
        for j in range(len(row)):
            find_length_n_paths_helper([(i,j)], n, board, words)

def find_length_n_paths_helper(current_path: Path, max_length: int, board: Board, words: Iterable[str], paths_found: List[Path]=None) -> List[Path]:
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



def find_length_n_words(n: int, board: Board, words: Iterable[str]) -> List[Path]:
    pass


def max_score_paths(board: Board, words: Iterable[str]) -> List[Path]:
    pass
