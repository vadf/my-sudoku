import unittest
import sudoku
import os
import xmlrunner
import copy

class TestSudoku(unittest.TestCase):
    """Sudoku testing class"""

    test_game_ok = "test_game_ok.txt"
    dir_path = os.path.dirname(os.path.realpath(__file__))

    def setUp(self):
        self.sudoku = sudoku.Sudoku(self.dir_path + '/' + self.test_game_ok)

    def tearDown(self):
        self.sudoku = None

    def test_init_none(self):
        """Test that if no Game file provided, empty Sudoku field will be created"""
        self.sudoku = sudoku.Sudoku()
        complexity = self.sudoku.get_game_complexity()
        self.assertEqual(complexity, 729)
        # check that all cells are 0
        for line in self.sudoku.work_field:
            self.assertEqual(sum(line), 0)

    def test_init_wrong_format1(self):
        """Test load game file with incorrect field size (expected 9*9)"""
        self.assertRaises(sudoku.FormatError, sudoku.Sudoku, self.dir_path + '/' + 'test_game_nok1.txt')

    def test_init_wrong_format2(self):
        """Test load game file with incorrect field size (expected 9*9)"""
        self.sudoku = sudoku.Sudoku()
        self.assertRaises(sudoku.FormatError, self.sudoku.read_game, self.dir_path + '/' + 'test_game_nok2.txt')

    def test_init_wrong_format3(self):
        """Test load game file with incorrect character (expected [0-9*])"""
        self.assertRaises(sudoku.FormatError, sudoku.Sudoku, self.dir_path + '/' +'test_game_nok3.txt')

    def test_get_row(self):
        """Test that specific row can be retrieved"""
        expected = [6,0,0,4,0,0,0,0,2]
        actual = self.sudoku.get_row(0)
        self.assertEqual(actual, expected)
        expected = [4,0,0,0,0,1,0,0,8]
        actual = self.sudoku.get_row(8)
        self.assertEqual(actual, expected)

    def test_get_col(self):
        """Test that specific column can be retrieved"""
        expected = [6,0,1,0,3,2,0,8,4]
        actual = self.sudoku.get_col(0)
        self.assertEqual(actual, expected)
        expected = [2,1,0,7,4,0,6,0,8]
        actual = self.sudoku.get_col(8)
        self.assertEqual(actual, expected)

    def test_get_block(self):
        """Test that specific block can be retrieved"""
        expected = [6,0,0,0,0,5,1,2,0]
        actual = self.sudoku.get_block(0)
        self.assertEqual(actual, expected)
        expected = [0,1,6,3,0,0,0,0,8]
        actual = self.sudoku.get_block(8)
        self.assertEqual(actual, expected)

    def test_check_for_duplicates(self):
        """Test that game field doesn't contain duplicate values in rows, cols and blocks"""
        self.assertFalse(self.sudoku.check_for_duplicates())

    def test_check_for_duplicates1(self):
        """Test duplicates in row"""
        self.sudoku = sudoku.Sudoku()
        self.sudoku.read_game(self.dir_path + '/' + 'test_game_dup1.txt')
        self.assertTrue(self.sudoku.check_for_duplicates())

    def test_check_for_duplicates2(self):
        """Test duplicates in column"""
        self.sudoku.read_game(self.dir_path + '/' + 'test_game_dup2.txt')
        self.assertTrue(self.sudoku.check_for_duplicates())

    def test_check_for_duplicates3(self):
        """Test duplicates in block"""
        self.sudoku = sudoku.Sudoku(self.dir_path + '/' + 'test_game_dup3.txt')
        self.assertTrue(self.sudoku.check_for_duplicates())

    def test_get_block_num0(self):
        """Test that block number = 0"""
        expected = 0
        actual = sudoku.get_block_num(0, 0)
        self.assertEqual(actual, expected)
        actual = sudoku.get_block_num(2, 2)
        self.assertEqual(actual, expected)
        actual = sudoku.get_block_num(2, 0)
        self.assertEqual(actual, expected)
        actual = sudoku.get_block_num(0, 2)
        self.assertEqual(actual, expected)


    def test_get_block_num4(self):
        """Test that block number = 4"""
        expected = 4
        actual = sudoku.get_block_num(3, 3)
        self.assertEqual(actual, expected)
        actual = sudoku.get_block_num(5, 5)
        self.assertEqual(actual, expected)
        actual = sudoku.get_block_num(3, 5)
        self.assertEqual(actual, expected)
        actual = sudoku.get_block_num(5, 3)
        self.assertEqual(actual, expected)

    def test_get_possible_value(self):
        """Test method get_possible_values that returns list of possible values for each empty cell"""
        result = self.sudoku.get_possible_values()
        self.assertEqual(result[1][(8,1)], set([6]))
        self.assertEqual(result[2][(0,1)], set([8,3]))
        self.assertEqual(result[3][(5,4)], set([1,5,6]))

    def test_solve_medium(self):
        """Test that medium level sudoku is solved"""
        origin_field = copy.deepcopy(self.sudoku.work_field)
        complexity = self.sudoku.get_game_complexity()
        self.assertEqual(complexity, 117)
        result = self.sudoku.solve()
        complexity = self.sudoku.get_game_complexity()
        self.assertEqual(complexity, 0)

        # check that all 0 are replaced by real values
        for line in result:
            self.assertFalse(0 in line)
        # check that there are no duplicate values in field
        self.assertFalse(self.sudoku.check_for_duplicates())
        # check that origin cells on its place
        for row, line in enumerate(origin_field):
            for col, cell in enumerate(line):
                if cell != 0:
                    self.assertEqual(cell, result[row][col])

    def test_solve_evil(self):
        """Test that evil level sudoku is solved"""
        self.sudoku = sudoku.Sudoku(self.dir_path + '/' +'test_game_evil.txt')
        origin_field = copy.deepcopy(self.sudoku.work_field)
        complexity = self.sudoku.get_game_complexity()
        self.assertEqual(complexity, 204)
        result = self.sudoku.solve()
        complexity = self.sudoku.get_game_complexity()
        self.assertEqual(complexity, 0)
        # check that all 0 are replaced by real values
        for line in result:
            self.assertFalse(0 in line)
        # check that there are no duplicate values in field
        self.assertFalse(self.sudoku.check_for_duplicates())
        # check that origin cells on its place
        for row, line in enumerate(origin_field):
            for col, cell in enumerate(line):
                if cell != 0:
                    self.assertEqual(cell, result[row][col])

    @unittest.skip("you can be lucky or can have a rest and watch movie")
    def test_solve_mad(self):
        """Test that sudoku with only few init values can be solved"""
        self.sudoku = sudoku.Sudoku(self.dir_path + '/' +'test_game_mad.txt')
        origin_field = copy.deepcopy(self.sudoku.work_field)
        complexity = self.sudoku.get_game_complexity()
        self.assertEqual(complexity, 644)
        result = self.sudoku.solve()
        complexity = self.sudoku.get_game_complexity()
        self.assertEqual(complexity, 0)
        # check that all 0 are replaced by real values
        for line in result:
            self.assertFalse(0 in line)
        # check that there are no duplicate values in field
        self.assertFalse(self.sudoku.check_for_duplicates())
        # check that origin cells on its place
        for row, line in enumerate(origin_field):
            for col, cell in enumerate(line):
                if cell != 0:
                    self.assertEqual(cell, result[row][col])

    def test_create_new_game_easy(self):
        """Test that easy Sudoku game can be created (based on template game)"""
        level = 'easy'
        self.sudoku.create_new_game(level)
        complexity = self.sudoku.get_game_complexity()
        self.assertTrue(complexity > self.sudoku.complexity_levels[level])

    def test_create_new_game_medium(self):
        """Test that medium Sudoku game can be created"""
        level = 'medium'
        self.sudoku = sudoku.Sudoku()
        self.sudoku.create_new_game(level)
        complexity = self.sudoku.get_game_complexity()
        self.assertTrue(complexity > self.sudoku.complexity_levels[level])

    def test_create_new_game_hard(self):
        """Test that hard Sudoku game can be created"""
        level = 'hard'
        self.sudoku = sudoku.Sudoku()
        self.sudoku.create_new_game(level)
        complexity = self.sudoku.get_game_complexity()
        self.assertTrue(complexity > self.sudoku.complexity_levels[level])

    def test_create_new_game_evil(self):
        """Test that evil Sudoku game can be created (based on template game)"""
        level = 'evil'
        self.sudoku = sudoku.Sudoku(self.dir_path + '/' +'test_game_evil.txt')
        self.sudoku.create_new_game(level)
        complexity = self.sudoku.get_game_complexity()
        self.assertTrue(complexity > self.sudoku.complexity_levels[level])

if __name__ == '__main__':
    unittest.main(testRunner=xmlrunner.XMLTestRunner(output='test-reports'))
    
