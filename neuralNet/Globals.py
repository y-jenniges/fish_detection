# general parameters
NUM_GROUPS = 6
channels = NUM_GROUPS*2 - 1


# parameters for training
no_animal_ratio = 0
batch_size = 4


# loss={'heatmap': 'mse', 
#       'classification': 'categorical_crossentropy'}
loss = "categorical_crossentropy"
optimizer = 'adam'
metrics = ['mae']
# metrics = {'heatmap':['mae'],
#            'classification':['acc']}

epochs = 15