import time
import keras
import numpy as np
import feature_planes
from board import Board

model = keras.models.load_model('weights.h5')

player = 1
board = Board()
move_history = []

def pa(na):
  for r in na:
    line = ''
    for c in r:
      if c:
        c = 1
      else:
        c = '.'
      line += c + ' '
    print(line)

while True:
  planes = feature_planes.generate(board, player, move_history)
  predictions = model.predict(np.array([planes])).tolist()[0]
  for i, prediction in enumerate(predictions):
    predictions[i] = (i, prediction)
  predictions = sorted(predictions, key=lambda p: p[1])
  n = 0
  while True:
    prediction = predictions[n]
    row = prediction[0] // 19
    col = prediction[0] % 19
    if board.is_legal_move(player, (row, col)):
      move_history.append((row, col))
      board.play(player, (row, col))
      player *= -1
      break
    n += 1
  time.sleep(1)
  print(board)

