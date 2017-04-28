import random
import os
import gc
import keras
import numpy as np
from keras.utils import np_utils
from keras.models import Sequential
from keras.layers import Dense, Activation, Flatten, Dropout
from keras.layers import Conv2D, ZeroPadding2D
from keras.layers.normalization import BatchNormalization

keras.backend.set_image_data_format('channels_first')

def generate_data():
  print('start')
  while True:
    files = [f for f in os.listdir('data/processed') if f.endswith('.npz')]
    random.shuffle(files)
    for filename in files:
      print('loading data')
      data = np.load('data/processed/%s' % filename)
      examples = np.unpackbits(data['examples'], axis=1)
      moves = np_utils.to_categorical(data['moves'], 361)
      yield(examples, moves)
    
if os.path.isfile('weights.h5'):
  model = keras.models.load_model('weights.h5')
else:
  model = Sequential()
  
  F = 64
  model.add(Conv2D(F, (5, 5), input_shape=(24, 19, 19), padding='same', activation='elu'))
  model.add(Conv2D(F, (3, 3), padding='same', activation='elu'))
  model.add(Conv2D(F, (3, 3), padding='same', activation='elu'))
  model.add(Conv2D(F, (3, 3), padding='same', activation='elu'))
  model.add(Conv2D(F, (3, 3), padding='same', activation='elu'))
  model.add(Conv2D(F, (3, 3), padding='same', activation='elu'))
  model.add(Flatten())
  model.add(Dense(361, activation='softmax'))
  
model.compile(
  loss='categorical_crossentropy',
  optimizer='sgd',
  metrics=['accuracy', keras.metrics.top_k_categorical_accuracy],
  callbacks=[keras.callbacks.TensorBoard()],
)

generator = generate_data()
while True:
  gc.collect()
  examples, moves = next(generator)
  model.fit(
    examples,
    moves,
    validation_split=0.1,
    epochs=1,
    shuffle=True,
  )

  model.save('weights.h5')

