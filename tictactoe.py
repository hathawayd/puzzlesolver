from enum import Enum
from utils.utils import optionalPrint


class Player(Enum):
    X = 'X'
    O = 'O'

class ticTacToe():
    def __init__(self):
        self.__board = [[None,None,None],[None,None,None],[None,None,None]]
    
    def __str__(self):
        retStr = ''
        for row in self.__board:
            for val in row:
                if val:
                    retStr += val.name + ' | '
                else:
                    retStr += '  | '
            retStr = retStr[:-3]
            retStr += '\n---------\n'
        retStr = retStr[:-10]
        return retStr

    def select(self, x: int, y: int, val: Player, verbose: bool=True):
        self.__board[x][y] = val
        if not self._checkWin():
            optionalPrint(self, verbose)

    def _checkWin(self, verbose=True) -> bool:
        for row in self.__board:
            if row[0] == row[1] == row[2]:
                optionalPrint("Player " + row[0].name + " wins!\n" + str(self), verbose)
                return True
        for i in range(3):
            if self.__board[i][0] == self.__board[i][1] == self.__board[i][2]:
                optionalPrint("Player " + self.__board[i][0].name + " wins!\n" + str(self), verbose)
                return True
        if self.__board[0][0] == self.__board[1][1] == self.__board[2][2]:
            optionalPrint("Player " + self.__board[0][0].name + " wins!\n" + str(self), verbose)
            return True
        if self.__board[2][0] == self.__board[1][1] == self.__board[0][2]:
            optionalPrint("Player " + self.__board[2][0].name + " wins!\n" + str(self), verbose)
            return True
        return False
