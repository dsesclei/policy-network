import numpy as np

def value(board, value):
  plane = np.zeros([19, 19], dtype=np.uint8)
  for r in range(19):
    for c in range(19):
      if board.points[r][c] == value:
        plane[r][c] = 1
  return plane

def point(p):
  plane = np.zeros([19, 19], dtype=np.uint8)
  if p is not None:
    plane[p[0]][p[1]] = 1
  return plane

def history(moves, n):
  plane = np.zeros([19, 19], dtype=np.uint8)
  if len(moves) >= n:
    point = moves[-n]
    plane[point[0]][point[1]] = 1
  return plane

def liberties(board, player, count):
  plane = np.zeros([19, 19], dtype=np.uint8)
  return plane

def capture_points(board, player, count):
  plane = np.zeros([19, 19], dtype=np.uint8)
  return plane

