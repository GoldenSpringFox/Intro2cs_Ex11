from ex11_utils import *
from ex11_utils import _are_cells_on_board, _are_cells_sequencially_touching, _is_cell_repeating, _get_surrounding_cells, _get_words_with_prefix

def test__are_cells_on_board():
    assert not _are_cells_on_board(0, 1, (0,0))
    assert not _are_cells_on_board(1, 0, (0,0))
    assert _are_cells_on_board(1, 1, (0,0))
    assert not _are_cells_on_board(1, 3, (1,0))
    assert not _are_cells_on_board(1, 3, (0,-1))
    assert not _are_cells_on_board(1, 3, (0,3))
    assert _are_cells_on_board(1, 3, (0,2))

    assert not _are_cells_on_board(3, 1, (0,1))
    assert not _are_cells_on_board(3, 1, (-1,0))
    assert not _are_cells_on_board(3, 1, (3,0))
    assert _are_cells_on_board(3, 1, (2,0))


def test__are_cells_sequencially_linked():
    assert _are_cells_sequencially_touching((0,0))
    assert _are_cells_sequencially_touching((0,0), (1,0))
    assert _are_cells_sequencially_touching((0,0), (0,1))
    assert _are_cells_sequencially_touching((0,0), (1,1))
    assert _are_cells_sequencially_touching((0,0), (-1,-1))
    assert not _are_cells_sequencially_touching((0,0), (2,0))
    assert not _are_cells_sequencially_touching((0,0), (-2,0))
    assert not _are_cells_sequencially_touching((0,0), (0,2))
    assert not _are_cells_sequencially_touching((0,0), (0,-2))
    assert not _are_cells_sequencially_touching((1,4), (4,1))

    assert _are_cells_sequencially_touching((0,0), (1,0), (2,0), (3,1), (2,2), (1,1))
    assert not _are_cells_sequencially_touching((0,0), (1,0), (3,1))
    assert not _are_cells_sequencially_touching((0,0), (1,0), (3,1), (3,2))
    assert not _are_cells_sequencially_touching((0,0), (1,0), (3,1), (2,1))

def test__is_cell_repeating():
    assert not _is_cell_repeating()
    assert not _is_cell_repeating((0,0))
    assert not _is_cell_repeating((0,0), (1,1), (1,0), (0,1))
    assert _is_cell_repeating((0,0), (0,0))
    assert _is_cell_repeating((0,0), (0,0), (1,1))
    assert _is_cell_repeating((0,0), (1,1), (0,0))
    assert _is_cell_repeating((0,0), (1,1), (1,0), (0,1), (1,1), (2,0), (3,0))


def test_is_valid_path():
    board = [
        ['a', 'b', 'c', 'd'],
        ['a', 'b', 'c', 'd'],
        ['e', 'e', 'f', 'f'],
        ['h', 'h', 'g', 'g']
    ]
    assert is_valid_path(board, [(0,0), (0,1)], ['ab']) == 'ab'
    assert is_valid_path(board, [(0,0), (0,1)], ['a', 'aa', 'abc']) is None
    assert is_valid_path(board, [(0,0), (1,0)], ['a', 'aa', 'abc']) == 'aa'
    assert is_valid_path(board, [(0,0), (0,1), (1,1), (1,0), (2,0), (2,1), (2,2)], None) == 'abbaeef'
    assert is_valid_path(board, [(0,0), (1,1), (0,1), (1,0), (2,1), (3,1), (2,0)], None) == 'abbaehe'
    assert is_valid_path(board, [(0,0), (0,3)], ['ad']) is None
    assert is_valid_path(board, [(0,0), (1,1), (0,1), (1,0), (1,3), (2,1), (3,1), (2,0)], ['abbadehe']) is None
    assert is_valid_path(board, [(-1,0)], ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']) is None
    assert is_valid_path(board, [(0,-1)], ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']) is None
    assert is_valid_path(board, [(4,0)], ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']) is None
    assert is_valid_path(board, [(0,4)], ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']) is None


def test__get_surrounding_cells():
    assert set(_get_surrounding_cells((1,3))) == set([(0,2), (0,3), (0,4), (1,2), (1,4), (2,2), (2,3), (2,4)])


def test_find_length_n_paths():
    board = [
        ['a', 'b', 'c', 'd'],
        ['a', 'b', 'c', 'd'],
        ['e', 'e', 'f', 'f'],
        ['h', 'h', 'g', 'g']
    ]
    assert find_length_n_paths(0, board, ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']) == []
    assert find_length_n_paths(1, [[]], ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']) == []
    assert find_length_n_paths(1, board, []) == []
    assert find_length_n_paths(1, board, ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']) == [
            [(0,0)], [(0,1)], [(0,2)], [(0,3)],
            [(1,0)], [(1,1)], [(1,2)], [(1,3)],
            [(2,0)], [(2,1)], [(2,2)], [(2,3)],
            [(3,0)], [(3,1)], [(3,2)], [(3,3)]
            ]
    
    board = [
        ['a', 'b'],
        ['c', 'd']
    ]
    assert find_length_n_paths(2, board, ['aa', 'ab', 'ac', 'ad', 'ba', 'bb', 'bc', 'bd', 'ca', 'cb', 'cc', 'cd', 'da', 'db', 'dc', 'dd']) == [
        [(0,0), (0,1)], [(0,0), (1,0)], [(0,0), (1,1)],
        [(0,1), (0,0)], [(0,1), (1,0)], [(0,1), (1,1)],
        [(1,0), (0,0)], [(1,0), (0,1)], [(1,0), (1,1)],
        [(1,1), (0,0)], [(1,1), (0,1)], [(1,1), (1,0)]
    ]


def test__get_words_with_prefix():
    assert set(_get_words_with_prefix('', [])) == set()
    assert set(_get_words_with_prefix('a', [])) == set()
    assert set(_get_words_with_prefix('', ['e', 'he', 'hell', 'hello'])) == set(['e', 'he', 'hell', 'hello'])
    assert set(_get_words_with_prefix('h', ['e', 'he', 'hell', 'hello'])) == set(['he', 'hell', 'hello'])
    assert set(_get_words_with_prefix('e', ['e', 'he', 'hell', 'hello'])) == set(['e'])
    assert set(_get_words_with_prefix('hel', ['e', 'he', 'hell', 'hello'])) == set(['hell', 'hello'])

def test_find_length_n_words():
    board = [['a', 'b'], 
             ['c', 'd']]
    assert find_length_n_words(0, board, ['a', 'b', 'c', 'd']) == []
    assert find_length_n_words(1, [[]], ['a', 'b', 'c', 'd']) == []
    assert find_length_n_words(1, board, []) == []
    assert find_length_n_words(1, board, ['a', 'b', 'c', 'd']) == [[(0,0)], [(0,1)], [(1,0)], [(1,1)]]
    assert find_length_n_words(1, board, ['b', 'c']) == [[(0,1)], [(1,0)]]

    words = ['ba', 'bb', 'bd', 'db']
    assert find_length_n_words(1, board, words) == []
    assert find_length_n_words(2, board, words) == [[(0,1), (0,0)], [(0,1), (1,1)], [(1,1), (0,1)]]
    assert find_length_n_words(3, board, words) == []
    
    board = [['a', 'a'], ['b', 'a']]
    assert find_length_n_words(1, board, ['a', 'c']) == [[(0,0)], [(0,1)], [(1,1)]]