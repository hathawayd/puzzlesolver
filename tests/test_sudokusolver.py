from sudokusolver import sudoku, getEasy, getExpert, getHard, getMaster, getMedium
import pytest

def test_sudoku():
    puzzle = sudoku(getEasy())
    assert not puzzle.isSolved()
    assert not puzzle.isCorrect()
    puzzleStr = str(puzzle)
    assert puzzleStr == \
'6 7 2 |X 3 X |9 4 X\n\
8 X X |6 X X |X 7 5\n\
X X 9 |8 2 X |6 X X\n\
-------------------\n\
1 X X |X X X |X 2 X\n\
X X X |X X 8 |7 5 X\n\
2 8 4 |7 5 3 |1 X 9\n\
-------------------\n\
7 X 3 |1 8 X |X X X\n\
4 X 5 |X X X |3 X X\n\
X X X |3 7 4 |X X 6\n'

    puzzle.solve()
    assert puzzle.isCorrect()
    assert puzzle.isSolved()
    puzzleStr = str(puzzle)
    assert puzzleStr == \
'6 7 2 |5 3 1 |9 4 8\n\
8 3 1 |6 4 9 |2 7 5\n\
5 4 9 |8 2 7 |6 3 1\n\
-------------------\n\
1 5 7 |4 9 6 |8 2 3\n\
3 9 6 |2 1 8 |7 5 4\n\
2 8 4 |7 5 3 |1 6 9\n\
-------------------\n\
7 6 3 |1 8 5 |4 9 2\n\
4 1 5 |9 6 2 |3 8 7\n\
9 2 8 |3 7 4 |5 1 6\n'

@pytest.mark.parameterize("data", [getEasy(),getExpert(),getHard(),getMaster(),getMaster()])
def test_sudoku_guesses(data):
    puzzle = sudoku(data)
    assert not puzzle.isSolved()
    assert not puzzle.isCorrect()
    puzzle.solve()
    assert puzzle.isCorrect()
    assert puzzle.isSolved()

def test_sudoku_from_string():
    puzzle = sudoku(data=".....54.6............2.8.5..13.9.8.7..4.....1...8....9..8..19...2.73....5......7.")
    assert not puzzle.isSolved()
    assert not puzzle.isCorrect()
    puzzle.solve()
    assert puzzle.isCorrect()
    assert puzzle.isSolved()
    puzzleStr = str(puzzle)
    assert puzzleStr == \
'8 3 2 |1 7 5 |4 9 6\n\
7 4 5 |3 6 9 |2 1 8\n\
1 9 6 |2 4 8 |7 5 3\n\
-------------------\n\
6 1 3 |5 9 4 |8 2 7\n\
9 8 4 |6 2 7 |5 3 1\n\
2 5 7 |8 1 3 |6 4 9\n\
-------------------\n\
3 7 8 |4 5 1 |9 6 2\n\
4 2 9 |7 3 6 |1 8 5\n\
5 6 1 |9 8 2 |3 7 4\n'

def test_sudoku_bad_data():
    data = [[1,2,3,4,5,6,7,8,9],[2,3,4,5,6,7,8,9,10],[1],[1],[1],[1],[1],[1],[1]]
    with pytest.raises(AttributeError):
        puzzle = sudoku(data)
    
    data = "bad sudoku string"
    with pytest.raises(AttributeError):
        puzzle = sudoku(data)
