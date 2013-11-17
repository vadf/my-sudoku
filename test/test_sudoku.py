import unittest
import sudoku
import os

class TestSudoku(unittest.TestCase):
    """Sudoku testing class"""

    test_game_ok = "test_game_ok.txt"
    dir_path = os.path.dirname(os.path.realpath(__file__))

    def setUp(self):
        self.sudoku = sudoku.Sudoku(self.dir_path + '/' + self.test_game_ok)

    def tearDown(self):
        self.sudoku = None

    def test_init_wrong_format1(self):
        """Test load game file with incorrect field size (expected 9*9)"""
        self.assertRaises(sudoku.FormatError, sudoku.Sudoku, self.dir_path + '/' + 'test_game_nok1.txt')

    def test_init_wrong_format2(self):
        """Test load game file with incorrect field size (expected 9*9)"""
        self.assertRaises(sudoku.FormatError, sudoku.Sudoku, self.dir_path + '/' + 'test_game_nok2.txt')

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
        self.sudoku = sudoku.Sudoku(self.dir_path + '/' + 'test_game_dup1.txt')
        self.assertTrue(self.sudoku.check_for_duplicates())

    def test_check_for_duplicates2(self):
        """Test duplicates in column"""
        self.sudoku = sudoku.Sudoku(self.dir_path + '/' + 'test_game_dup2.txt')
        self.assertTrue(self.sudoku.check_for_duplicates())

    def test_check_for_duplicates3(self):
        """Test duplicates in block"""
        self.sudoku = sudoku.Sudoku(self.dir_path + '/' + 'test_game_dup3.txt')
        self.assertTrue(self.sudoku.check_for_duplicates())


if __name__ == '__main__':
    unittest.main()
    
