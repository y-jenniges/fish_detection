# general parameters
NUM_GROUPS = 6


# parameters for training
no_animal_ratio = 0.3
batch_size = 4


loss={'heatmap': 'mse', 
      'classification': 'categorical_crossentropy'}
optimizer = 'adam'
metrics = {'heatmap':['mae'],
           'classification':['acc']}

epochs = 3