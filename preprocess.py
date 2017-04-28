import sys
import threading
import time
import numpy as np
from sgfmill import sgf
from board import Board
import feature_planes

class Processor(object):
  def __init__(self):
    self.examples = []
    self.moves = []
    self.block_size = 500

  def process(self, start_block, end_block):
    current_block = start_block
    current_sgf = self.block_size * start_block
    while current_block < end_block:
      while current_sgf < self.block_size * (current_block + 1):
        self.process_sgf('data/sgf/%d.sgf' % current_sgf)
        current_sgf += 1
      self.flush(current_block)
      current_block += 1

  def process_sgf(self, filename):
    print(filename)
    print(len(self.moves))
    with open(filename, 'rb') as f:
      game = sgf.Sgf_game.from_bytes(f.read())

    winner = game.get_winner()
    if winner is None or game.get_handicap() is not None:
      print('Skipping game')
      return

    board = Board()
    move_history = []

    for node in game.get_main_sequence():
      color, point = node.get_move()
      if color is None or point is None:
        continue
      player = 1 if color == 'b' else -1
      point = (18 - point[0], point[1])

      if color == winner:
        planes = feature_planes.generate(board, player, move_history)
        self.examples.append(planes)
        self.moves.append(point[0] * 19 + point[1])

      move_history.append(point)

      if board.is_legal_move(player, point):
        board.play(player, point)
      else:
        print('Illegal move!')
        print(filename)
        print(node)
        break

  def flush(self, block):
    print('%d: Writing %d examples to disk' % (block, len(self.examples)))
    np.savez_compressed('data/processed/%d' % block, moves=self.moves, examples=np.packbits(np.array(self.examples, dtype=bool), axis=1))
    self.examples = []
    self.moves = []


if __name__ == '__main__':
  p = Processor()
  p.process(int(sys.argv[1]), int(sys.argv[2]))

