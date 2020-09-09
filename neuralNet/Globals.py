from keras import metrics

# general parameters
NUM_GROUPS = 6
channels = NUM_GROUPS*2 - 1


# parameters for training
no_animal_ratio = 0
batch_size = 2


# loss={'heatmap': 'mse', 
#       'classification': 'categorical_crossentropy'}
#activation_outLayer = "softmax"

loss = {"heatmap":"categorical_crossentropy", 
        "connection":"binary_crossentropy"}

optimizer = 'adam'
#metrics = ['mae']
# metrics = {'heatmap':['mae'],
#             'classification':['acc']}
#metrics = [ "mae", "acc", "categorical_crossentropy", "tp", "fp", "tn", "fn", "precision", "recall", "auc"]
#       metrics.MeanAbsoluteError(name='mae'),
#       metrics.CategoricalCrossentropy(name="categorical_crossentropy"),
#       metrics.TruePositives(name='tp'),
#       metrics.FalsePositives(name='fp'),
#       metrics.TrueNegatives(name='tn'),
#       metrics.FalseNegatives(name='fn'), 
#       metrics.BinaryAccuracy(name='accuracy'),
#       metrics.Precision(name='precision'),
#       metrics.Recall(name='recall'),
#       metrics.AUC(name='auc'),
# ]


epochs_L = 1
epochs_H = 1
