import unittest
import sudoku


class TestSudoku(unittest.TestCase):
    """Sudoku testing class"""

    def setUp(self):
        self.sudoku = sudoku.Sudoku()

    def tearDown(self):
        self.sudoku = None

    def test_one(self):
        self.assertTrue(True)

if __name__ == '__main__':
    unittest.main()
