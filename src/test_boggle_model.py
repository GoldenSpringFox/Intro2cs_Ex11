from boggle_model import *

def test_soft_path_update():
    board = [['a'] * 4 for _ in range(4)]
    assert not BoggleModel(board, []).soft_path_update((-1,0))
    assert not BoggleModel(board, []).soft_path_update((99,0))
    assert not BoggleModel(board, []).soft_path_update((0,-1))
    assert not BoggleModel(board, []).soft_path_update((0,99))
    
    assert not BoggleModel(board, [], [(1,1), (1,2)]).soft_path_update((3,2))
    assert not BoggleModel(board, [], [(1,1), (1,2)]).soft_path_update((1,0))

    model = BoggleModel(board, [])
    assert model.soft_path_update((0,0))
    model.current_path == [(0,0)]

    model = BoggleModel(board, [], [(1,1), (1,2)])
    assert model.soft_path_update((2,1))
    model.current_path == [(1,1), (1,2), (2,1)]

    model = BoggleModel(board, [], [(1,1), (1,2)])
    assert model.soft_path_update((1,1))
    model.current_path == [(1,1)]


def test_submit():
    board = [['a'] * 4 for _ in range(4)]
    words = ['a', 'aa']
    assert not BoggleModel(board, words, []).submit()
    assert not BoggleModel(board, words, [(0,0), (0,1), (0,2)]).submit()

    model = BoggleModel(board, words, [(0,0)])
    assert model.submit()
    assert model.current_path == []
    assert model.score == 1

    model = BoggleModel(board, words, [(1,2), (2,1)])
    assert model.submit()
    assert model.score == 4

