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
    neighbors = self.get_neighbors(point)
    for neighbor in neighbors:
      if neighbor not in visited_points:
        if self.points[neighbor[0]][neighbor[1]] == player:
          size += self.count_liberties(neighbor, visited_points)
    return size

  def remove_group(self, point):
    player = self.points[point[0]][point[1]]
    self.points[point[0]][point[1]] = 0
    neighbors = self.get_neighbors(point)
    for neighbor in neighbors:
      if player == self.points[neighbor[0]][neighbor[1]]:
        self.remove_group(neighbor)

  def play(self, player, point):
    self.points[point[0]][point[1]] = player
    neighbors = self.get_neighbors(point)
    for neighbor in neighbors:
      if self.points[neighbor[0]][neighbor[1]] == player * -1:
        liberties = self.count_liberties(neighbor)
        if liberties == 0:
          self.remove_group(neighbor)

  def __str__(self):
    output = ''
    for row in self.points:
      line = ''
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