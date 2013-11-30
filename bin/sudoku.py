import re
import copy
import argparse
import random

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
    field_list = []
    tmp_pos_values = {}
    solved = False
    complexity_levels = {'easy': 70, 'medium': 110, 'hard' : 150, 'evil': 190}

    def __init__(self, filename=None):
        """(Sudoku, str) -> NoneType

        Initiate Sudoku game from a file if provided.

        >>> Sudoku('game_field.txt')
        >>> Sudoku()
        """
        if filename == None:
            self.work_field = []
            for i in range(0,9):
                self.work_field.append([0 for x in range(0,9)])
        else:
            self.read_game(filename)

    def read_game(self, filename):
        """ (Sudoku, str) -> NoneType

        Reads Sudoku game field from a file.
        Raises FormatError exception if game field is incorrect.

        >>> sudoku = Sudoku()
        >>> sudoku.read_game('game_field.txt')
        """
        self.work_field = []
        f = open(filename, 'r')
        count = 0
        pattern = re.compile('^[1-9*]{9}$')
        for line in f:
            if pattern.match(line):
                count += 1
                self.work_field.append([int(x) if x.isdigit() else 0 for x in line.strip()])
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
        return self.work_field[num]

    def get_col(self, num):
        """(Sudoku, int) -> list of int

        Retrieve col[num] of game field

        >>> sudoku = Sudoku("test_game_ok.txt")
        >>> sudoku.get_col(0)
        [6,0,1,0,3,2,0,8,4]
        """
        return [x[num] for x in self.work_field]

    def get_block(self, num):
        """(Sudoku, int) -> list of int

        Retrieve block[num] of game field

        >>> sudoku = Sudoku("test_game_ok.txt")
        >>> sudoku.get_block(0)
        [6,0,0,0,0,5,1,2,0]
        """
        row = 3 * (num / 3)
        col = 3 * (num % 3)
        return self.work_field[row][col : col + 3] + \
            self.work_field[row + 1][col : col + 3] + \
            self.work_field[row + 2][col : col + 3]

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

    def get_possible_values(self):
        """ (Sudoku) -> dictionary {int : dictionary {(int,int) : list of int}}

        Returns the possible values of empty (= 0) field cells for self.work_field in format of \
        Dictionary with key='number of possible values', value='Dictionary with key=field \
        cell(int,int) and value=set of possible values'

        >>> sudoku = Sudoku('test_game_ok.txt')
        >>> sudoku.get_possible_values()
        {1: {(1, 2): set([5])}, ...}
        """
        result = {}
        max_set = set(range(1,10))

        for row, line in enumerate(self.work_field):
            for col, cell in enumerate(line):
                if cell == 0:
                    cell_pos_values = max_set - set(self.get_row(row)) - set(self.get_col(col)) - \
                        set(self.get_block(get_block_num(row,col))) - set([0])
                    key = len(cell_pos_values)
                    if key == 0:
                        return {0:0}
                    if key in result:
                        result[key][(row,col)] = cell_pos_values
                    else:
                        result[key] = {}
                        result[key][(row,col)] = cell_pos_values
        return result

    def get_game_complexity(self):
        """ (Sudoku) -> int

        Returns value of game complexity.

        >>> sudoku = Sudoku('test_game_ok.txt')
        >>> sudoku.get_game_complexity()
        100
        >>> sudoku = Sudoku()
        >>> sudoku.get_game_complexity()
        729
        >>> sudoku = Sudoku('test_game_ok.txt')
        >>> sudoku.solve()
        >>> sudoku.get_game_complexity()
        0
        """
        pos_values = self.get_possible_values()
        complexity = 0
        for key in pos_values:
            complexity += key * len(pos_values[key])
        return complexity

    def solve(self):
        """ (Sudoku) -> list of list of int

        Returns the solved sudoku field

        >>> sudoku = new Sudoku('test_game_ok.txt')
        >>> sudoku.solve()
        [[6, 3, 7, 4, 1, 5, 9, 8, 2], ...]
        """

        cur_pos_values = self.get_possible_values()
        if len(cur_pos_values) == 0:
            self.solved = True
            return self.work_field

        if 0 in cur_pos_values:
            return None

        # get the first cell and its possible values (hope that it is cell with the most minimum values)
        min_value = cur_pos_values.keys()[0]
        cell = cur_pos_values[min_value].keys()[0]

        if min_value > 1:
            self.field_list.append(copy.deepcopy(self.work_field))

        for value in cur_pos_values[min_value][cell]:
            self.work_field[cell[0]][cell[1]] = value
            self.solve()
            if self.solved:
                return self.work_field
            self.work_field = copy.deepcopy(self.field_list[-1])

        if min_value > 1:
            self.work_field = self.field_list.pop(-1)

    def create_new_game(self, level):
        """ (Sudoku, str) -> NoneType

        Creates new Sudoku game with provided complexity level (easy, medium, hard, evil).
        Another Sudoku game can be used as template for new one.

        >>> sudoku = Sudoku()
        >>> sudoku.create_new_game('easy')

        >>> sudoku = Sudoku('test_game_ok.txt')
        >>> sudoku.create_new('medium')
        """
        border = self.complexity_levels[level]
        self.solve()

        complexity = 0
        random.seed()
        while complexity <= border:
            row = random.randint(0,8)
            col = random.randint(0,8)
            self.work_field[row][col] = 0
            complexity = self.get_game_complexity()

    def print_field(self):
        """ (Sudoku) -> None
        Prints the current sudoku field
        """
        print '   ' + str(range(1,10))[1:-1]
        for row, line in enumerate(self.work_field):
            print row + 1, line

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Sudoku arguments')
    parser.add_argument('-s', '--solve', metavar='/path/to/file', help='solve Sudoku game')
    parser.add_argument('-n', '--new', metavar='None or /path/to/file', nargs='?', const='no', \
        help='create new Sudoku game, other sudoku game can be used as template')
    parser.add_argument('-l', '--level', choices=['easy', 'medium', 'hard', 'evil'], \
        default='medium', help='level of complexity for new Sudoku game')
    args = parser.parse_args()

    if args.solve == None and args.new == None:
        parser.print_help()
        exit()

    if args.solve != None:
        sudoku = Sudoku(args.solve)
        print 'Game to solve:'
        sudoku.print_field()
        sudoku.solve()
        print 'Solved game:'
        sudoku.print_field()

    if args.new != None:
        print 'Create new game with level of complexity: ' + args.level
        print 'Use other Game as template: ' + args.new
        sudoku = Sudoku()
        if args.new != 'no':
            sudoku.read_game(args.new)
            sudoku.print_field()
            print 'New Game'
        sudoku.create_new_game(args.level)
        sudoku.print_field()
