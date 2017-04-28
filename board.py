import sys
import numpy as np

class Board(object):
  def __init__(self):
    self.points = np.zeros([19, 19])
    self.ko_point = None

  def is_valid_point(self, point):
    return point[0] >= 0 and point[1] >= 0 and point[0] < 19 and point[1] < 19

  def get_neighbors(self, point):
    neighbors = [
        (point[0] + 1, point[1]),
        (point[0] - 1, point[1]),
        (point[0], point[1] + 1),
        (point[0], point[1] - 1),
    ]
    return [n for n in neighbors if self.is_valid_point(n)]

  def count_liberties(self, point, visited_points=None):
    if visited_points is None:
      visited_points = set()
    player = self.points[point[0]][point[1]]
    visited_points.add(point)

    liberties = 0
    neighbors = self.get_neighbors(point)
    for neighbor in neighbors:
      if neighbor not in visited_points:
        value = self.points[neighbor[0]][neighbor[1]]
        if value == 0:
          visited_points.add(neighbor)
          liberties += 1
        elif value == player:
          liberties += self.count_liberties(neighbor, visited_points)
    return liberties

  def count_size(self, point, visited_points=None):
    if visited_points is None:
      visited_points = set()
    player = self.points[point[0]][point[1]]
    visited_points.add(point)

    size = 1
    for neighbor in self.get_neighbors(point):
      if neighbor not in visited_points and self.points[neighbor[0]][neighbor[1]] == player:
        size += self.count_size(neighbor, visited_points)
    return size

  def remove_group(self, point):
    player = self.points[point[0]][point[1]]
    self.points[point[0]][point[1]] = 0
    neighbors = self.get_neighbors(point)
    for neighbor in neighbors:
      if player == self.points[neighbor[0]][neighbor[1]]:
        self.remove_group(neighbor)

  def is_legal_move(self, player, point):
    if not self.is_valid_point(point):
      return False

    if self.points[point[0]][point[1]] != 0:
      return False

    if point == self.ko_point:
      return False

    neighbors = self.get_neighbors(point)
    for neighbor in neighbors:
      if self.points[neighbor[0]][neighbor[1]] == player * -1 and self.count_liberties(neighbor) == 1:
        return True

    self.points[point[0]][point[1]] = player
    has_liberties = self.count_liberties(point) > 0
    self.points[point[0]][point[1]] = 0
    if not has_liberties:
      return False

    return True

  def play(self, player, point):
    if not self.is_legal_move(player, point):
      print('Playing illegal move!')
      sys.exit(0)
    self.points[point[0]][point[1]] = player
    self.ko_point = None
    neighbors = self.get_neighbors(point)
    for neighbor in neighbors:
      if self.points[neighbor[0]][neighbor[1]] == player * -1:
        liberties = self.count_liberties(neighbor)
        if liberties == 0:
          size = self.count_size(neighbor)
          self.remove_group(neighbor)
          if size == 1:
            self.ko_point = neighbor

  def __str__(self):
    output = "   a b c d e f g h j k l m n o p q r s t\n"
    for r, row in enumerate(self.points):
      r = 19 - r
      line = str(r) + ' '
      if r < 10:
        line += ' '
      for value in row:
        if value == 0:
          line += '.'
        if value == 1:
          line += 'b'
        if value == -1:
          line += 'w'
        line += ' '
      output += line + "\n"
    return output
