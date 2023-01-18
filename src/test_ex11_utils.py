from ex11_utils import *

def test_is_valid_path():
    board = [
        ['a', 'b', 'c', 'd'],
        ['a', 'b', 'c', 'd'],
        ['e', 'e', 'f', 'f'],
        ['h', 'h', 'g', 'g']
    ]
    assert is_valid_path(board, [(0,0), (0,1)], ['ab'])
    assert not is_valid_path(board, [(0,0), (0,1)], ['a', 'aa', 'abc'])
    assert is_valid_path(board, [(0,0), (1,0)], ['a', 'aa', 'abc'])
    assert is_valid_path(board, [(0,0), (0,1), (1,1), (1,0), (2,0), (2,1), (2,2)], ['abbaeef'])
    assert is_valid_path(board, [(0,0), (1,1), (0,1), (1,0), (2,1), (3,1), (2,0)], ['abbaehe'])
    assert not is_valid_path(board, [(0,0), (0,3)], ['ad'])
    assert not is_valid_path(board, [(0,0), (1,1), (0,1), (1,0), (1,3), (2,1), (3,1), (2,0)], ['abbadehe'])
    assert not is_valid_path(board, [(-1,0)], ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h'])
    assert not is_valid_path(board, [(0,-1)], ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h'])
    assert not is_valid_path(board, [(4,0)], ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h'])
    assert not is_valid_path(board, [(0,4)], ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h'])
    