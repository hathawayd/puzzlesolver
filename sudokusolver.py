from copy import copy, deepcopy

class sudoku:
    def __init__(self, data):
        if type(data) == list:
            if len(data) != 9:
                raise(AttributeError('Not enough rows in data to construct valid Sudoku.'))
            for row in data:
                if len(row) != 9:
                    raise(AttributeError('Not enough columns in row all rows to construct valid Sudoku.'))
            self.__rows = data
            self.__guesses = deepcopy(getEmpty())

        elif type(data) == str:
            if len(data) != 81:
                raise(AttributeError('Valid Sudoku requre 81 characters.'))
            self.__rows = deepcopy(getEmpty())
            count = 0
            for x in range(9):
                for y in range(9):
                    if data[count] in ['1','2','3','4','5','6','7','8','9']:
                        self.__rows[x][y] = int(data[count])
                    count += 1
            self.__guesses = deepcopy(getEmpty())
        else:
            raise Exception

    def __str__(self) -> str:
        retStr = ''
        count1 = 0
        for row in self.__rows:
            if count1 == 3:
                retStr += '-------------------\n'
                count1 = 0
            count2 = 0
            for value in row:
                if count2 == 3:
                    retStr += '|'
                    count2 = 0
                if value:
                    retStr += str(value) + ' '
                else:
                    retStr += 'X '
                count2 += 1
            retStr = retStr[:-1]
            retStr +=  '\n'
            count1 += 1
        return retStr

    def _checkValue(self, x: int,y: int) -> list[int]:
        if self.__rows[x][y]:
            return [self.__rows[x][y]]
        values = list(range(1,10))
        # check row
        for i in range(9):
            if i != y:
                try:
                    values.remove(self.__rows[x][i])
                except ValueError:
                    pass
        # check column
        for i in range(9):
            if i != x:
                try:
                    values.remove(self.__rows[i][y])
                except ValueError:
                    pass
        # check block
        startx = (x//3) * 3
        starty = (y//3) * 3
        for i in range(startx, startx + 3):
            for j in range(starty, starty + 3):
                if i != x or j != y:
                    try:
                        values.remove(self.__rows[i][j])
                    except ValueError:
                        pass
        if (not self.__rows[i][j]) and (len(values) > 1):
            self.__guesses[i][j] = values
        else:
            self.__guesses[i][j] = None
        return values
    
    def _checkNegativeValue(self, x: int,y: int, value: int) -> bool:
        if self.__rows[x][y]:
            return False

        # Check if value can exist in any other spot in row
        found = False
        for i in range(9):
            if i != y:
                if value in self._checkValue(x,i):
                    found = True
        if not found:
            return True

        # Check if value can exist in any other spot in column
        found = False
        for i in range(9):
            if i != x:
                if value in self._checkValue(i,y):
                    found = True
        if not found:
            return True

        # Check if value can exist in any other spot in block
        found = False
        startx = (x//3) * 3
        starty = (y//3) * 3
        for i in range(startx, startx + 3):
            for j in range(starty, starty + 3):
                if i != x or j != y:
                    if value in self._checkValue(x=i, y=j):
                        found = True
        if not found:
            return True
        return False

    def _solveByElimination(self) -> bool:
        foundOne = False
        for i in range(9):
            for j in range(9):
                if not self.__rows[i][j]:
                    values = self._checkValue(i,j)
                    if len(values) == 1:
                        self.__rows[i][j] = values[0]
                        foundOne = True
        return foundOne
    
    def _solveByNegativeElimination(self) -> bool:
        foundOne = False
        for i in range(9):
            for j in range(9):
                if not self.__rows[i][j]:
                    for value in self._checkValue(i,j):
                        if self._checkNegativeValue(i,j,value):
                            self.__rows[i][j] = value
                            foundOne = True
                            break
        return foundOne

    def isSolved(self) -> bool:
        for i in range(9):
            for j in range(9):
                if not self.__rows[i][j]:
                    return False
        return True

    def _solveByEliminationLoop(self):
        found = True
        while found:
            found = self._solveByElimination()

    def _solveByNegativeEliminationLoop(self):
        found = True
        while found:
            self._solveByEliminationLoop()
            found = self._solveByNegativeElimination()

    def _solveByHintsLoop(self):
        found1 = True
        found2 = True
        while found1 or found2:
            self._solveByNegativeEliminationLoop()
            if self.isSolved():
                return self.isCorrect()
            #self._populateHints()
            found1 = self._pruneHints()
            found2 = self._pruneHints()

    def solve(self, guess=True) -> bool:
        self._solveByHintsLoop()

        if self.isCorrect(silent=True):
            return True

        if guess:
            print("Trial and Error phase")
            self._guess()

        if self.isCorrect(silent=True):
            print(self)
            return True
        return False
    
    def _guess(self):
        for x in range(9):
            for y in range(9):
                if not self.__rows[x][y]:
                    for val in self._checkValue(x,y):
                        backupRows = deepcopy(self.__rows)
                        self.__rows[x][y] = val
                        self.solve(guess=False)
                        if self.isCorrect(silent=True):
                            return True
                        else:
                            self.__rows = deepcopy(backupRows)
        return False

    def _populateHints(self):
        for i in range(9):
            for j in range(9):
                if not self.__rows[i][j]:
                    self.__guesses[i][j] = self._checkValue(i,j)
                else:
                    self.__guesses[i][j] = None

    def _pruneHints(self) -> bool:
        foundOne = False
        # look for pairs in rows
        for x in range(9):
            for i in range(8):
                for j in range(i+1,9):
                    if (self.__guesses[x][i] and self.__guesses[x][j] and 
                            (self.__guesses[x][i] == self.__guesses[x][j]) and 
                            (len(self.__guesses[x][i]) == len(self.__guesses[x][j]) == 2)):
                        # prune from other guesses in row
                        for k in range(9):
                            if k != i and k != j:
                                if self.__guesses[x][k]:
                                    for val in self.__guesses[x][i]:
                                        try:
                                            self.__guesses[x][k].remove(val)
                                        except ValueError:
                                            pass
                                    if len(self.__guesses[x][k]) == 1:
                                        self.__rows[x][k] = self.__guesses[x][k][0]
                                        self.__guesses[x][k] = None
                                        foundOne = True

        # look for pairs in columns
        for y in range(9):
            for i in range(8):
                for j in range(i+1,9):
                    if (self.__guesses[i][y] and self.__guesses[j][y] and 
                            (self.__guesses[i][y] == self.__guesses[j][y]) and 
                            (len(self.__guesses[i][y]) == len(self.__guesses[j][y]) == 2)):
                        # prune from other guesses in row
                        for k in range(9):
                            if k != i and k != j:
                                if self.__guesses[k][y]:
                                    for val in self.__guesses[i][y]:
                                        try:
                                            self.__guesses[k][y].remove(val)
                                        except ValueError:
                                            pass
                                    if len(self.__guesses[k][y]) == 1:
                                        self.__rows[k][y] = self.__guesses[k][y][0]
                                        self.__guesses[k][y] = None
                                        foundOne = True
        # look for pairs in blocks
        if (self._pruneHintsInBlock()):
            foundOne = True

        return foundOne
    
    def _pruneHintsInBlock(self) -> bool:
        foundOne = False

        for x in range(3):
            for y in range(3):
                startx = x * 3
                starty = y * 3
                for x1 in range(startx, startx + 3):
                    for y1 in range(starty, starty + 3):
                        for x2 in range(startx, startx + 3):
                            for y2 in range(starty, starty + 3):
                                if x1 != x2 or y1 != y2:
                                    if (
                                        self.__guesses[x1][y1] and
                                        self.__guesses[x2][y2] and
                                        len(self.__guesses[x1][y1]) == 2 and
                                        len(self.__guesses[x2][y2]) == 2 and
                                        self.__guesses[x1][y1] == self.__guesses[x2][y2]
                                    ):
                                        for x3 in range(startx, startx + 3):
                                            for y3 in range(starty, starty + 3):
                                                if ((x3 != x1 or y3 != y1) and
                                                    (x3 != x2 or y3 != y2)
                                                    ):
                                                    if self.__guesses[x3][y3]:
                                                        for val in self.__guesses[x1][y1]:
                                                            try:
                                                                self.__guesses[x3][y3].remove(val)
                                                            except ValueError:
                                                                pass
                                                        if len(self.__guesses[x3][y3]) == 1:
                                                            self.__rows[x3][y3] = self.__guesses[x3][y3][0]
                                                            self.__guesses[x3][y3] = None
                                                            foundOne = True
        return foundOne
    
    def printHints(self):
        retStr = ''
        count1 = 0
        for row in self.__guesses:
            if count1 == 3:
                retStr += '-------------------\n'
                count1 = 0
            count2 = 0
            for value in row:
                if count2 == 3:
                    retStr += '|'
                    count2 = 0
                if value:
                    retStr += str(value) + ' '
                else:
                    retStr += 'X '
                count2 += 1
            retStr = retStr[:-1]
            retStr +=  '\n'
            count1 += 1
        print(retStr)
    
    def isCorrect(self, silent=False):
        # Check Rows
        values = list(range(1,10))
        for x in range(9):
            values = list(range(1,10))
            for y in range(9):
                try:
                    values.remove(self.__rows[x][y])
                except ValueError:
                    if not silent:
                        print("Wrong in Row: " + str(x))
                    return False

        # Check Columns
        for y in range(9):
            values = list(range(1,10))
            for x in range(9):
                try:
                    values.remove(self.__rows[x][y])
                except ValueError:
                    if not silent:
                        print("Wrong in Column: " + str(y))
                    return False

        # Check Blocks
        for k in range(3):
            for m in range(3):
                startx = k * 3
                starty = m * 3
                values = list(range(1,10))
                for x in range(startx, startx + 3):
                    for y in range(starty, starty + 3):
                        try:
                            values.remove(self.__rows[x][y])
                        except ValueError:
                            if not silent:
                                print("Wrong in Block: " + str(startx) + "." + str(starty))
                            return False
        return True

def getEasy():
    return [
        [6,7,2,None,3,None,9,4,None],
        [8,None,None,6,None,None,None,7,5],
        [None,None,9,8,2,None,6,None,None],
        [1,None,None,None,None,None,None,2,None],
        [None,None,None,None,None,8,7,5,None],
        [2,8,4,7,5,3,1,None,9],
        [7,None,3,1,8,None,None,None,None],
        [4,None,5,None,None,None,3,None,None],
        [None,None,None,3,7,4,None,None,6]]

def getMedium():
    return [
        [3,None,None,None,None,1,7,None,None],
        [None,7,None,None,None,None,3,4,5],
        [None,None,None,None,None,3,None,9,None],
        [None,None,2,None,None,None,4,7,None],
        [None,None,None,3,None,None,1,None,2],
        [7,6,None,1,None,9,None,3,None],
        [None,None,None,None,5,None,None,1,3],
        [9,1,None,None,None,None,None,None,None],
        [6,8,3,9,None,None,None,None,4]]

def getHard():
    return [
        [9,None,None,None,6,2,3,None,1],
        [None,5,None,3,None,None,None,6,None],
        [None,None,None,4,None,None,2,None,None],
        [None,None,2,None,None,None,None,4,None],
        [None,9,None,8,None,None,None,None,None],
        [7,None,None,9,3,6,None,2,None],
        [5,6,None,None,None,None,None,3,None],
        [None,None,None,None,None,None,8,1,None],
        [3,7,8,None,None,5,None,None,None]]

def getExpert():
    return [
        [None,None,None,None,None,5,4,None,6],
        [None,None,None,None,None,None,None,None,None],
        [None,None,None,2,None,8,None,5,None],
        [None,1,3,None,9,None,8,None,7],
        [None,None,4,None,None,None,None,None,1],
        [None,None,None,8,None,None,None,None,9],
        [None,None,8,None,None,1,9,None,None],
        [None,2,None,7,3,None,None,None,None],
        [5,None,None,None,None,None,None,7,None]]

def getMaster():
    return [
        [None,None,8,None,9,3,None,7,2],
        [None,None,None,None,None,None,3,None,None],
        [None,1,None,None,None,6,None,None,None],
        [None,None,4,None,None,None,5,None,None],
        [None,None,None,None,3,None,8,None,None],
        [6,None,None,None,None,9,None,4,3],
        [None,None,7,None,2,None,None,9,4],
        [8,None,None,7,None,None,None,None,None],
        [None,None,None,None,None,None,None,5,None]]

def getEmpty():
    return [
        [None,None,None,None,None,None,None,None,None],
        [None,None,None,None,None,None,None,None,None],
        [None,None,None,None,None,None,None,None,None],
        [None,None,None,None,None,None,None,None,None],
        [None,None,None,None,None,None,None,None,None],
        [None,None,None,None,None,None,None,None,None],
        [None,None,None,None,None,None,None,None,None],
        [None,None,None,None,None,None,None,None,None],
        [None,None,None,None,None,None,None,None,None]]
