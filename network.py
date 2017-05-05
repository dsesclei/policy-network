import subprocess
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
  i = 326
  while i < 1500:
    if subprocess.run('gsutil -q ls gs://policy-network/work.{}.npz'.format(i).split()).returncode != 0:
      i += 1
      continue
    subprocess.call('gsutil cp gs://policy-network/work.{}.npz data/processed/.'.format(i).split())

    print('Loading dataset {}'.format(i))
    data = np.load('data/processed/work.{}.npz'.format(i))
    examples = np.unpackbits(data['examples'], axis=1)
    moves = np_utils.to_categorical(data['moves'], 361)
    i += 1
    yield(examples, moves)
    
if os.path.isfile('weights.h5'):
  model = keras.models.load_model('weights.h5')
else:
  model = Sequential()
  
  model.add(Conv2D(96, (5, 5), input_shape=(24, 19, 19), padding='same', activation='elu'))
  for i in range(17):
    model.add(Conv2D(96, (3, 3), padding='same', activation='elu'))
  model.add(Flatten())
  model.add(Dense(361, activation='softmax'))
  
model.compile(
  loss='categorical_crossentropy',
  optimizer='sgd',
  metrics=['accuracy', keras.metrics.top_k_categorical_accuracy],
  callbacks=[keras.callbacks.ModelCheckpoint('/home/dave/policy-network/checkpoints/weights.{epoch:02d}-{val_loss:.2f}.h5')],
)

print(model.summary())
generator = generate_data()
while True:
  gc.collect()
  examples, moves = next(generator)
  history = model.fit(
    examples,
    moves,
    validation_split=0.1,
    epochs=1,
    shuffle=True,
  )
  with open('log.txt', 'a') as log:
    log.write(str(history.history) + "\n")
  model.save('weights.h5')


