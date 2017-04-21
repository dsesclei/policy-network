import numpy as np
import unittest
from board import Board
import feature_planes


class TestPlanes(unittest.TestCase):
  @classmethod
  def setUpClass(self):
    self.board = Board()
    self.player = 1
    self.move_history = []
    def play(row, col):
      self.board.play(self.player, (row, col))
      self.player *= -1
      self.move_history.append((row, col))

    play(0, 0)
    play(1, 1)
    play(0, 1)
    play(1, 0)
    play(2, 2)

    play(10, 10)
    play(12, 11)
    play(11, 10)
    play(12, 12)
    play(12, 10)

    play(7, 3)
    play(8, 4)
    play(8, 3)
    play(8, 5)
    play(9, 4)
    play(7, 4)
    play(9, 5)
    play(7, 5)
    play(8, 6)
    play(18, 18)
    play(7, 6)
    play(18, 18)
    play(6, 5)


    self.player = 1

    self.planes = feature_planes.generate(self.board, self.player, self.move_history)
    print(self.board)
    l = feature_planes.calculate_liberties_counts(self.board)
    print(np.array(feature_planes.calculate_capture_counts(self.board, 1, l), dtype=int))

  def test_player_values(self):
    self.assertEqual(self.planes[0][0][0], 1)
    self.assertEqual(self.planes[0][1][1], 0)
    self.assertEqual(self.planes[0][1][1], 0)

  def test_opponent_values(self):
    self.assertEqual(self.planes[1][0][0], 0)
    self.assertEqual(self.planes[1][1][1], 1)
    self.assertEqual(self.planes[1][1][1], 1)

  def test_empty_values(self):
    self.assertEqual(self.planes[2][0][0], 0)
    self.assertEqual(self.planes[2][1][1], 0)
    self.assertEqual(self.planes[2][1][1], 0)
    self.assertEqual(self.planes[2][2][1], 1)

  def test_player_liberties(self):
    # Check 1 liberties plane
    self.assertEqual(self.planes[4][0][0], 1)
    self.assertEqual(self.planes[4][0][1], 1)
    self.assertEqual(self.planes[4][1][0], 0)
    self.assertEqual(self.planes[4][1][1], 0)

    # Check >= 4 liberties plane
    self.assertEqual(self.planes[4][2][2], 0)
    self.assertEqual(self.planes[7][2][2], 1)
    self.assertEqual(self.planes[7][12][12], 1)

  def test_history(self):
    self.assertEqual(self.planes[12][self.move_history[-1][0]][self.move_history[-1][1]], 1)
    self.assertEqual(self.planes[13][self.move_history[-2][0]][self.move_history[-2][1]], 1)
    self.assertEqual(self.planes[14][self.move_history[-3][0]][self.move_history[-3][1]], 1)
    self.assertEqual(self.planes[15][self.move_history[-4][0]][self.move_history[-4][1]], 1)

  def test_captures(self):
    pass
if __name__ == '__main__':
  unittest.main()
