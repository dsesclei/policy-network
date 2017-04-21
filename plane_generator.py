import numpy as np

def value(board, value):
  plane = np.zeros([19, 19], dtype=np.uint8)
  for r in range(19):
    for c in range(19):
      if board.points[r][c] == value:
        plane[r][c] = 1
  return plane

def history(moves, n):
  plane = np.zeros([19, 19], dtype=np.uint8)
  if len(moves) >= n:
    point = moves[-n]
    plane[point[0]][point[1]] = 1
  return plane

def generate_liberties_counts(board):
  plane = np.zeros([19, 19], dtype=np.uint8)
  for row in range(19):
    for col in range(19):
      if plane[row][col] == 0 and board.points[row][col] != 0:
        visited_points = set()
        count = board.count_liberties((row, col), visited_points)
        for point in visited_points:
          if board.points[point[0]][point[1]] != 0:
            plane[point[0]][point[1]] = count
  return plane

def generate_capture_counts(board, player, liberties_counts):
  plane = np.zeros([19, 19], dtype=np.uint8)
  for row in range(19):
    for col in range(19):
      if board.points[row][col] == 0:
        count = 0
        neighbors = board.get_neighbors((row, col))
        visited_points = set()
        for neighbor in neighbors:
          if board.points[neighbor[0]][neighbor[1]] == player * -1 and neighbor not in visited_points:
              liberties = liberties_counts[neighbor[0]][neighbor[1]]
              if liberties == 1:
                count += board.count_size(neighbor, visited_points)
        plane[row][col] = count
  return plane

def liberties(board, player, liberties_counts, count):
  plane = np.zeros([19, 19], dtype=np.uint8)
  for row in range(19):
    for col in range(19):
      if liberties_counts[row][col] == count:
        plane[row][col] = 1
  return plane

def capture_points(board, player, capture_counts, count):
  plane = np.zeros([19, 19], dtype=np.uint8)
  for row in range(19):
    for col in range(19):
      if capture_counts[row][col] == count:
        plane[row][col] = 1
  return plane