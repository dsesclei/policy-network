import numpy as np
from sgfmill import sgf
from board import Board
import feature_planes

class Processor(object):
  def __init__(self):
    self.examples = []
    self.target_moves = []
    self.block_size = 100

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
    with open(filename, 'rb') as f:
      game = sgf.Sgf_game.from_bytes(f.read())

    board = Board()
    move_history = []

    for node in game.get_main_sequence():
      color, point = node.get_move()
      if color is None or point is None:
        continue
      player = 1 if color == 'b' else -1
      point = (18 - point[0], point[1])

      planes = feature_planes.generate(board, player, move_history)
      self.examples.append(planes)
      self.target_moves.append(point[0] * 19 + point[1])

      move_history.append(point)
      board.play(player, point)

  def flush(self, block):
    print('Writing %d examples to disk' % len(self.examples))
    np.save('data/processed/%d' % block, np.array(self.examples, dtype=bool))
    np.save('data/processed/%d.moves' % block, np.array(self.target_moves, dtype=np.uint8))
    self.examples = []
    self.target_moves = []


if __name__ == '__main__':
  p = Processor()
  p.process(0, 1)

