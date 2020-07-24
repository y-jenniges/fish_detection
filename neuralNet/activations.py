# import tensorflow.compat.v2 as tf
# import tensorflow_datasets as tfds


# (ds_train, ds_test), ds_info = tfds.load(
#     'mnist',
#     split=['train', 'test'],
#     shuffle_files=True,
#     as_supervised=True,
#     with_info=True,
# )


# def normalize_img(image, label):
#   """Normalizes images: `uint8` -> `float32`."""
#   return tf.cast(image, tf.float32) / 255., label

# ds_train = ds_train.map(
#     normalize_img, num_parallel_calls=tf.data.experimental.AUTOTUNE)
# ds_train = ds_train.cache()
# ds_train = ds_train.shuffle(ds_info.splits['train'].num_examples)
# ds_train = ds_train.batch(128)
# ds_train = ds_train.prefetch(tf.data.experimental.AUTOTUNE)


# ds_test = ds_test.map(
#     normalize_img, num_parallel_calls=tf.data.experimental.AUTOTUNE)
# ds_test = ds_test.batch(128)
# ds_test = ds_test.cache()
# ds_test = ds_test.prefetch(tf.data.experimental.AUTOTUNE)


# model = tf.keras.models.Sequential([
#   tf.keras.layers.Flatten(input_shape=(28, 28, 1)),
#   tf.keras.layers.Dense(128,activation='relu'),
#   tf.keras.layers.Dense(10, activation='softmax')
# ])
# model.compile(
#     loss='sparse_categorical_crossentropy',
#     optimizer=tf.keras.optimizers.Adam(0.001),
#     metrics=['accuracy'],
# )

# model.fit(
#     ds_train,
#     epochs=6,
#     validation_data=ds_test,
# )
#---------------------------------------------------------------------------
import keras

path="../data/output/32/"

model = keras.models.load_model(f"{path}model-L")


# https://stackoverflow.com/questions/41711190/keras-how-to-get-the-output-of-each-layer
# from keras import backend as K
# import numpy as np

# inp = model.input                                           # input placeholder
# outputs = [layer.output for layer in model.layers]          # all layer outputs
# functor = K.function([inp, K.learning_phase()], outputs )   # evaluation function

# # Testing
# test = np.random.random(inp.shape[1:])[np.newaxis,:]
# layer_outs = functor([test, 1.])
# print (layer_outs)


#---------------------------------------------------------------------------
import numpy as np
from keras import Input, Model
from keras.layers import Dense, concatenate
from keract import get_activations
import keract

# # model definition
# i1 = Input(shape=(10,), name='i1')
# i2 = Input(shape=(10,), name='i2')

# a = Dense(1, name='fc1')(i1)
# b = Dense(1, name='fc2')(i2)

# c = concatenate([a, b], name='concat')
# d = Dense(1, name='out')(c)
# model = Model(inputs=[i1, i2], outputs=[d])

# # inputs to the model
# x = [np.random.uniform(size=(32, 10)), np.random.uniform(size=(32, 10))]

# # call to fetch the activations of the model.
# activations = get_activations(model, x, auto_compile=True)

# # print the activations shapes.
# #[print(k, '->', v.shape, '- Numpy array') for (k, v) in activations.items()]

# # Print output:
# # i1 -> (32, 10) - Numpy array
# # i2 -> (32, 10) - Numpy array
# # fc1 -> (32, 1) - Numpy array
# # fc2 -> (32, 1) - Numpy array
# # concat -> (32, 2) - Numpy array
# # out -> (32, 1) - Numpy array

# keract.display_activations(activations, cmap=None, save=False, directory='.', data_format='channels_last')
# #keract.display_heatmaps(activations, input_image, save=False)
# #keract.get_gradients_of_trainable_weights(model, x, y)
# #keract.get_gradients_of_activations(model, x, y, layer_name=None, output_format='simple')



# # activations = get_activations(model, x, auto_compile=True)
# # [print(k, '->', v.shape, '- Numpy array') for (k, v) in activations.items()]

# import matplotlib.pyplot as plt
# fig_size=(24, 24)


# plt.imshow(activations.get("i2"),  interpolation='nearest')
# plt.show()

import HelperFunctions as helpers
#filename = "../data/maritime_dataset_25/training_data_animals/60.jpg"
filename = "G:/Universität/UniBremen/Semester4/Data/maritime_dataset_25/test_data/51.jpg"
image = helpers.loadImage(filename)
x = 2.*image/np.max(image) - 1
x = x.reshape(1,736, 1088, 3)

#x = helpers.downsample(x)

activations = get_activations(model, x, auto_compile=True)
keract.display_activations(activations, save=True, directory=f"{path}activations")


keract.display_heatmaps(activations, x, save=True, directory=f"{path}activationHeatmapsWithImage")