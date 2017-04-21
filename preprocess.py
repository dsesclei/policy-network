import uuid
import os
import numpy as np
from sgfmill import sgf
from board import Board
import plane_generator

examples = []
target_moves = []
for filename in os.listdir('data/sgf'):
  with open('data/sgf/%s' % filename, 'rb') as f:
    game = sgf.Sgf_game.from_bytes(f.read())
    if game.get_handicap():
      continue

  board = Board()
  move_history = []

  for node in game.get_main_sequence():
    color, point = node.get_move()
    if color is None or point is None:
      continue
    player = 1 if color == 'b' else -1
    point = (18 - point[0], point[1])

    liberties_counts = plane_generator.generate_liberties_counts(board)
    player_capture_counts = plane_generator.generate_capture_counts(board, player, liberties_counts)
    opponent_capture_counts = plane_generator.generate_capture_counts(board, player * -1, liberties_counts)

    planes = [
      plane_generator.value(board, player),
      plane_generator.value(board, player * -1),
      plane_generator.value(board, 0),
      np.full((19, 19), 1),
      plane_generator.liberties(board, player, liberties_counts, 1),
      plane_generator.liberties(board, player, liberties_counts, 2),
      plane_generator.liberties(board, player, liberties_counts, 3),
      plane_generator.liberties(board, player, liberties_counts, 4),
      plane_generator.liberties(board, player * -1, liberties_counts, 1),
      plane_generator.liberties(board, player * -1, liberties_counts, 2),
      plane_generator.liberties(board, player * -1, liberties_counts, 3),
      plane_generator.liberties(board, player * -1, liberties_counts, 4),
      plane_generator.history(move_history, 1),
      plane_generator.history(move_history, 2),
      plane_generator.history(move_history, 3),
      plane_generator.history(move_history, 4),
      plane_generator.capture_points(board, player, player_capture_counts, 1),
      plane_generator.capture_points(board, player, player_capture_counts, 2),
      plane_generator.capture_points(board, player, player_capture_counts, 3),
      plane_generator.capture_points(board, player, player_capture_counts, 4),
      plane_generator.capture_points(board, player * -1, opponent_capture_counts, 1),
      plane_generator.capture_points(board, player * -1, opponent_capture_counts, 2),
      plane_generator.capture_points(board, player * -1, opponent_capture_counts, 3),
      plane_generator.capture_points(board, player * -1, opponent_capture_counts, 4),
    ]

    examples.append(planes)
    target_moves.append(point)
    print(len(examples))
    if len(examples) == 10000:
      name = uuid.uuid4()
      print('Writing %d examples to disk' % len(examples))
      np.save('data/processed/examples.%s' % name, np.array(examples, dtype=np.uint8))
      np.save('data/processed/moves.%s' % name, np.array(target_moves, dtype=np.uint8))
      examples = []
      moves = []
    move_history.append(point)
    board.play(player, point)

