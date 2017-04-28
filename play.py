import time
import random
import keras
import numpy as np
import feature_planes
from board import Board

global model
model = keras.models.load_model('weights.h5')

class Player(object):
  def __init__(self, ptype):
    self.ptype = ptype
    if ptype == 'computer':
      global model
      self.model = model
 
  def move(self, board, player, move_history):
    if self.ptype == 'computer':
      planes = feature_planes.generate(board, player, move_history)
      predictions = self.model.predict(np.array([planes])).tolist()[0]
      for i, prediction in enumerate(predictions):
        predictions[i] = (i, prediction)
      predictions = sorted(predictions, key=lambda p: p[1], reverse=True)
      n = 0
      while True:
        prediction = predictions[n]
        row = prediction[0] // 19
        col = prediction[0] % 19
        yield(row, col)
        n += 1
    else:
      coords = input()
      col = ord(coords[0]) - 97
      row = 19 - int(coords[1:])
      if col > 7:
        col -= 1
      yield(row, col)

moving_player = 1
board = Board()
move_history = []

players = [Player('computer'), Player('computer')]
#players = [Player('computer'), Player('human')]

while True:
  for player in players:
    generator = player.move(board, moving_player, move_history)
    for move in generator:
      print(move)
      if board.is_legal_move(moving_player, move):
        move_history.append(move)
        board.play(moving_player, move)
        moving_player *= -1
        print(board)
        time.sleep(1)
        break
     

