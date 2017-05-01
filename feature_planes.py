import numpy as np

def value(board, value):
  plane = np.zeros([19, 19], dtype=bool)
  for r in range(19):
    for c in range(19):
      if board.points[r][c] == value:
        plane[r][c] = True
  return plane

def history(moves, n):
  plane = np.zeros([19, 19], dtype=bool)
  if len(moves) >= n:
    point = moves[-n]
    plane[point[0]][point[1]] = True
  return plane

def calculate_liberties_counts(board):
  plane = np.zeros([19, 19], dtype=int)
  for row in range(19):
    for col in range(19):
      if plane[row][col] == 0 and board.points[row][col] != 0:
        visited_points = set()
        count = board.count_liberties((row, col), visited_points)
        for point in visited_points:
          if board.points[point[0]][point[1]] != 0:
            plane[point[0]][point[1]] = count
  return plane

def calculate_capture_counts(board, player, liberties_counts):
  plane = np.zeros([19, 19], dtype=int)
  for row in range(19):
    for col in range(19):
      if board.points[row][col] == 0:
        count = 0
        visited_points = set()
        for neighbor in board.get_neighbors((row, col)):
          if board.points[neighbor[0]][neighbor[1]] == player * -1 and \
             liberties_counts[neighbor[0]][neighbor[1]] == 1 and \
             neighbor not in visited_points:
               count += board.count_size(neighbor, visited_points)
        plane[row][col] = count
  return plane

def liberties(board, player, liberties_counts, count):
  plane = np.zeros([19, 19], dtype=bool)
  for row in range(19):
    for col in range(19):
      if board.points[row][col] == player:
        if liberties_counts[row][col] == count or (count == 4 and liberties_counts[row][col] >= 4):
          plane[row][col] = True
  return plane

def capture_points(board, player, capture_counts, count):
  plane = np.zeros([19, 19], dtype=bool)
  for row in range(19):
    for col in range(19):
      if board.points[row][col] == player:
        if capture_counts[row][col] == count or (count == 4 and capture_counts[row][col] >= 4):
          plane[row][col] = True
  return plane

def generate(board, player, move_history):
  liberties_counts = calculate_liberties_counts(board)
  player_capture_counts = calculate_capture_counts(board, player, liberties_counts)
  opponent_capture_counts = calculate_capture_counts(board, player * -1, liberties_counts)

  return [
    value(board, player),
    value(board, player * -1),
    value(board, 0),
    np.full((19, 19), 1, dtype=bool),
    liberties(board, player, liberties_counts, 1),
    liberties(board, player, liberties_counts, 2),
    liberties(board, player, liberties_counts, 3),
    liberties(board, player, liberties_counts, 4),
    liberties(board, player * -1, liberties_counts, 1),
    liberties(board, player * -1, liberties_counts, 2),
    liberties(board, player * -1, liberties_counts, 3),
    liberties(board, player * -1, liberties_counts, 4),
    history(move_history, 1),
    history(move_history, 2),
    history(move_history, 3),
    history(move_history, 4),
    capture_points(board, player, player_capture_counts, 1),
    capture_points(board, player, player_capture_counts, 2),
    capture_points(board, player, player_capture_counts, 3),
    capture_points(board, player, player_capture_counts, 4),
    capture_points(board, player * -1, opponent_capture_counts, 1),
    capture_points(board, player * -1, opponent_capture_counts, 2),
    capture_points(board, player * -1, opponent_capture_counts, 3),
    capture_points(board, player * -1, opponent_capture_counts, 4),
  ]
