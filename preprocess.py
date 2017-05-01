import sys
import subprocess
import time
import random
import os
import numpy as np
from sgfmill import sgf
from board import Board
import feature_planes

class Processor(object):
  def __init__(self):
    self.examples = []
    self.moves = []
    self.block_size = 1000
    self.paths = list(sorted(os.listdir('data/sgf')))

  def process(self, start_block, end_block):
    current_block = start_block
    current_sgf = self.block_size * start_block
    while current_block < end_block:
      while current_sgf < self.block_size * (current_block + 1):
        self.process_sgf('data/sgf/{}'.format(self.paths[current_sgf]))
        current_sgf += 1
      self.flush(current_block)
      current_block += 1

  def process_sgf(self, filename):
    print(filename)
    with open(filename, 'rb') as f:
      game = sgf.Sgf_game.from_bytes(f.read())

    if game.get_winner() is None or game.get_handicap() is not None:
      return

    board = Board()
    move_history = []

    for node in game.get_main_sequence():
      color, point = node.get_move()
      if color is None or point is None:
        continue
      player = 1 if color == 'b' else -1
      point = (18 - point[0], point[1])

      if color == game.get_winner():
        planes = feature_planes.generate(board, player, move_history)
        self.examples.append(planes)
        self.moves.append(point[0] * 19 + point[1])

      move_history.append(point)

      if board.is_legal_move(player, point):
        board.play(player, point)
      else:
        print('Illegal move!')
        subprocess.call('gsutil cp .claim gs://policy-network/.illegal.{}'.format(filename).split())
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
  block = 0
  total_blocks = len(p.paths) // p.block_size
  while block < total_blocks:
    if subprocess.run('gsutil -q ls gs://policy-network/.claim.{}'.format(block).split()).returncode == 0:
      block += 1
    else:
      subprocess.call('gsutil cp .claim gs://policy-network/.claim.{}'.format(block).split())
      p.process(block, block+1)
      subprocess.call('gsutil cp data/processed/{}.npz gs://policy-network/work.{}.npz'.format(block, block).split())
