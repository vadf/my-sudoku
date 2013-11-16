import unittest
import sudoku
import os

class TestSudoku(unittest.TestCase):
    """Sudoku testing class"""

    test_game = "test_game_ok.txt"
    dir_path = os.path.dirname(os.path.realpath(__file__))

    def setUp(self):
        self.sudoku = sudoku.Sudoku(self.dir_path + '/' + self.test_game)

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

    def test_check_row_ok(self):
        """Test that row X doesn't contain duplicate values"""
        self.assertTrue(self.sudoku.check_row_duplicates(1))
        self.assertTrue(self.sudoku.check_row_duplicates(4))


if __name__ == '__main__':
    unittest.main()
    
