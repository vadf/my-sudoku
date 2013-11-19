import re

class FormatError(Exception):
    pass

def get_block_num(row, col):
    """ (int, int) -> int

    Returns the number of block in game field for specified row and col.

    >>> get_block_num(0,0)
    0
    >>> get_block_num(6,3)
    5
    """
    if row >= 0 and col >= 0 and row < 3 and col < 3:
        return 0
    elif row >= 0 and col >=3 and row < 3 and col < 6:
        return 1
    elif row >= 0 and col >=6 and row < 3 and col < 9:
        return 2
    elif row >= 3 and col >=0 and row < 6 and col < 3:
        return 3
    elif row >= 3 and col >=3 and row < 6 and col < 6:
        return 4
    elif row >= 3 and col >=6 and row < 6 and col < 9:
        return 5
    elif row >= 6 and col >=0 and row < 9 and col < 3:
        return 6
    elif row >= 6 and col >=3 and row < 9 and col < 6:
        return 7
    elif row >= 6 and col >=6 and row < 9 and col < 9:
        return 8
    else:
        return -1

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
        """(Sudoku, list of in of int) -> bool

        Check Sudoku field for duplicate values in rows, cols and blocks

        >>> sudoku = Sudoku("test_game_ok.txt")
        >>> sudoku.check_row_duplicates()
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

    def get_possible_values(self, field):
        """ (Sudoku, list of list of int) -> dictionary {int : dictionary {(int,int) : list of int}}

        Returns the possible values of empty (= 0) field cells in format of Dictionary with key='number \
        of possible values', value='Dictionary with key=field cell(int,int) and value=list of possible \
        values'

        >>> get_possible_values(field)
        {1: {(1, 2): (1, 2, 3)}}
        """
        result = {}
        max_set = set(range(1,10))

        for row, line in enumerate(field):
            for col, cell in enumerate(line):
                if cell == 0:
                    cell_pos_values = max_set - set(self.get_row(row)) - set(self.get_col(col)) - \
                        set(self.get_block(get_block_num(row,col))) - set([0])
                    key = len(cell_pos_values)
                    if key in result:
                        result[key][(row,col)] = cell_pos_values
                    else:
                        result[key] = {}
                        result[key][(row,col)] = cell_pos_values
        return result

    def solve(self, field=None):
        if field == None:
            field = self.field
        pos_values = self.get_possible_values(field)
        if 1 in pos_values:
            for key in pos_values[1]:
                field[key[0]][key[1]] = pos_values[1][key].pop()
            return self.solve(field)
        else:
            return field

if __name__ == '__main__':
    pass

