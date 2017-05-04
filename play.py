import pexpect
import random
import socket
import sys
import time
import keras
import numpy as np
import feature_planes
from board import Board


class TCPConnection(object):
  def __init__(self, server, port):
    self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    while True:
      try:
        self.sock.connect((server, port))
        break
      except ConnectionRefusedError:
        time.sleep(3)
    self.sock.settimeout(10)

  def send(self, message):
    self.sock.send('{}\n\n'.format(message).encode())

  def listen(self):
    try:
      message = self.sock.recv(4096).decode().strip()
      return message
    except socket.timeout:
      return None


class ServerBridge(object):
  def __init__(self):
    self.model = keras.models.load_model('weights.h5')
    self.board = Board()
    self.move_history = []
    self.commands = {
      'name': self.name,
      'version': self.version,
      'boardsize': self.boardsize,
      'clear_board': self.clear_board,
      'list_commands': self.list_commands,
      'play': self.play,
      'genmove': self.genmove,
      'kgs-genmove_cleanup': self.kgs_genmove_cleanup,
      'final_status_list': self.send_gnu_response,
      'komi': self.send_gnu_response,
      'showboard': self.send_gnu_response,
    }

    self.gnugo = pexpect.spawn('gnugo --mode gtp')
    self.server = TCPConnection('127.0.0.1', 4901)

  def listen(self):
    message = self.server.listen()
    if message:
      parts = message.split(' ')
      command = parts[0]
      args = parts[1:] if len(parts) > 1 else []
      if command in self.commands:
        self.commands[command](args, self.get_gnu_response(message))
      else:
        self.server.send('? Unknown command')

  def get_gnu_response(self, message):
    self.gnugo.sendline(message)
    self.gnugo.expect('\n')
    self.gnugo.expect('\r\n\r\n')
    return self.gnugo.before.decode().strip()


  ################
  # GTP Commands #
  ################
  def boardsize(self, args, gnu_response):
    if args[0] == '19':
      self.server.send('=')
    else:
      self.server.send('? Invalid board size')

  def play(self, args, gnu_response):
    m = ''.join(args).lower()
    if 'pass' in m or 'resign' in m:
      self.server.send('=')
      return
    col = ord(args[1][0]) - ord('a')
    row = 19 - int(args[1][1:])
    if col > 7:
      col -= 1
    move = (row, col)
    self.move_history.append(move)
    player = 1 if args[0] == 'b' else -1
    self.board.play(player, move)
    self.get_gnu_response('play {} {}'.format(args[0], args[1]))
    self.server.send('=')

  def name(self, args, gnu_response):
    self.server.send('= DaveBot')

  def version(self, args, gnu_response):
    self.server.send('= 1')

  def quit(self, args, gnu_response):
    sys.exit(0)

  def genmove(self, args, gnu_response):
    gnu_response = gnu_response.lower()
    if 'pass' in gnu_response:
      self.server.send('= pass')
      return
    if 'resign' in gnu_response:
      self.server.send('= resign')
      return
    # Undo genmove so that the board is consistent with GnuGo
    self.get_gnu_response('undo')

    player = 1 if args[0] == 'b' else -1
    planes = feature_planes.generate(self.board, player, self.move_history)
    predictions = self.model.predict(np.array([planes])).tolist()[0]
    for i, prediction in enumerate(predictions):
      predictions[i] = (i, prediction)
    predictions = sorted(predictions, key=lambda p: p[1], reverse=True)
    for prediction in predictions:
      move = (prediction[0] // 19, prediction[0] % 19)
      if self.board.is_legal_move(player, move):
        row = 19 - move[0]
        col = 'abcdefghjklmnopqrst'[move[1]]
        self.board.play(player, move)
        self.move_history.append(move)
        self.server.send('= {}{}'.format(col.upper(), row))
        self.get_gnu_response('play {} {}{}'.format(args[0], col.upper(), row))
        return
    self.server.send('= pass')

  def _kgs_genmove_cleanup(self, args, gnu_response):
    self.genmove(args, gnu_response)

  def _genmove(self, args, gnu_response):
    self.genmove(args, gnu_response)

  def _list_commands(self, args, gnu_response):
    self.server.send('= {}'.format('\n'.join(self.commands.keys())))

  def _clear_board(self, args, gnu_response):
    self.board = Board()
    self.move_history = []
    self.server.send('=')

  def send_gnu_response(self, args, gnu_response):
    self.server.send(gnu_response)

if __name__ == '__main__':
  bridge = ServerBridge()
  while True:
    bridge.listen()

