import re

class FormatError(Exception):
    pass

class Sudoku:
    """Sudoku class"""

    def __init__(self, filename):
        """(Sudoku, str) -> NoneType

        Reads Sudoku game field from a file.
        Raises FormatError exception if game field is incorrect.

        >>> Sudoku('game_field.txt')
        """
        self.field = []
        f = open(filename, 'r')
        count = 0
        pattern = re.compile('^[1-9*]{9}$')
        for line in f:
            if pattern.match(line):
                count += 1
                self.field.append([int(x) if x.isdigit() else 0 for x in line.strip()])
            else:
                f.close()
                raise FormatError("Line '" + str(line) + "' doesn't match pattern '" + str(pattern) + "'")

        if count < 9:
            f.close()
            raise FormatError("Number of lines is " + str(count) + ", but should be 9")

        f.close()

    def get_row(self, num):
        """(Sudoku, int) -> list of int

        Retrieve row[num] of game field

        >>> sudoku = Sudoku("test_game_ok.txt")
        >>> sudoku.get_row(0)
        [6,0,0,4,0,0,0,0,2]
        """
        return self.field[num]

    def get_col(self, num):
        """(Sudoku, int) -> list of int

        Retrieve col[num] of game field

        >>> sudoku = Sudoku("test_game_ok.txt")
        >>> sudoku.get_col(0)
        [6,0,1,0,3,2,0,8,4]
        """
        return [x[num] for x in self.field]

    def get_block(self, num):
        """(Sudoku, int) -> list of int

        Retrieve block[num] of game field
        
        >>> sudoku = Sudoku("test_game_ok.txt")
        >>> sudoku.get_block(0)
        [6,0,0,0,0,5,1,2,0]
        """
        row = 3 * (num / 3)
        col = 3 * (num % 3)
        return self.field[row][col : col + 3] + \
            self.field[row + 1][col : col + 3] + \
            self.field[row + 2][col : col + 3]

    def check_for_duplicates(self):
        """(Sudoku, int) -> bool

        Check Sudoku field for duplicate values in rows, cols and blocks

        >>> sudoku = Sudoku("test_game_ok.txt")
        >>> sudoku.check_row_duplicates(1)
        False
        """
        for i in range(0,9):
            list = self.get_row(i)
            if sum(list) != sum(set(list)):
                return True
            list = self.get_col(i)
            if sum(list) != sum(set(list)):
                return True
            list = self.get_block(i)
            if sum(list) != sum(set(list)):
                return True

        return False

if __name__ == '__main__':
    pass

