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
        
        Retrieve row num of game field 
        
        >>> sudoku = Sudoku("test_game_ok.txt")
        >>> sudoku.get_row(0)
        [6,0,0,4,0,0,0,0,2]
        """
        return self.field[num]

    def check_row_duplicates(self, num):
        """(Sudoku, int) -> bool
        
        Check row num in Sudoku field for duplicate values
        
        >>> sudoku = Sudoku("test_game_ok.txt")
        >>> sudoku.check_row_duplicates(1)
        False
        """
        row = self.get_row(num)
        if sum(row) == sum(set(row)):
            return True
        else:
            return False

if __name__ == '__main__':
    pass

