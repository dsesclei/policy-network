import random
import os
import gc
import keras
import numpy as np
from keras.utils import np_utils
from keras.models import Sequential
from keras.layers import Dense, Activation, Flatten
from keras.layers import Conv2D, ZeroPadding2D
from keras.layers.normalization import BatchNormalization


keras.backend.set_image_data_format('channels_first')

def generate_data():
  print('start')
  while True:
    files = [f for f in os.listdir('data/final') if f.endswith('.npz')]
    random.shuffle(files)
    for filename in files:
      print('loading data')
      data = np.load('data/final/%s' % filename)
      print('unpacking')
      examples = np.unpackbits(data['examples'], axis=1)
      print('categories')
      moves = np_utils.to_categorical(data['moves'], 361)
      indices = np.arange(len(examples))
      np.random.shuffle(indices)
      print(examples.shape)
      shuffled_examples = np.empty(examples.shape, dtype=bool)
      shuffled_moves = np.empty(moves.shape)
      for old, new in enumerate(indices):
        shuffled_examples[new] = examples[old]
        shuffled_moves[new] = moves[old]
      print('yielding data')
      yield(shuffled_examples, shuffled_moves)
    

if os.path.isfile('weights.h5'):
  model = keras.models.load_model('weights.h5')
else:
  model = Sequential()

  layers = [
    Conv2D(256, (5, 5), input_shape=(24, 19, 19), padding='same', activation='relu'),

    Conv2D(256, (3, 3), padding='same', activation='relu'),
    Conv2D(256, (3, 3), padding='same', activation='relu'),
    Conv2D(256, (3, 3), padding='same', activation='relu'),
    Conv2D(256, (3, 3), padding='same', activation='relu'),
    Conv2D(256, (3, 3), padding='same', activation='relu'),
    Conv2D(256, (3, 3), padding='same', activation='relu'),
    Conv2D(256, (3, 3), padding='same', activation='relu'),
    Conv2D(256, (3, 3), padding='same', activation='relu'),

    Flatten(),
    Dense(1024, activation='relu'),
    BatchNormalization(),
    Dense(361, activation='softmax'),
  ]

  for layer in layers:
    model.add(layer)

  model.compile(
    loss='categorical_crossentropy',
    optimizer=keras.optimizers.SGD(momentum=0.9),
    metrics=['accuracy', keras.metrics.categorical_accuracy],
  )


generator = generate_data()
while True:
  gc.collect()
  examples, moves = next(generator)
  model.fit(
    examples,
    moves,
    validation_split=0.1,
    batch_size=128,
    epochs=1,
  )

  model.save('weights.h5')

