from keras import backend as K
"""
Modules containing custom losses. 
"""


def weighted_categorical_crossentropy(weights):
    """
    A weighted version of keras.objectives.categorical_crossentropy
    
    Variables:
        weights: numpy array of shape (C,) where C is the number of classes
    
    Usage:
        weights = np.array([0.5,2,10]) # Class one at 0.5, class 2 twice the normal weights, class 3 10x.
        loss = weighted_categorical_crossentropy(weights)
        model.compile(loss=loss,optimizer='adam')
    Taken from:
        https://gist.github.com/wassname/ce364fddfc8a025bfab4348cf5de852d
    """
    
    weights = K.variable(weights)
        
    def loss(y_true, y_pred):
        # scale predictions so that the class probas of each sample sum to 1
        y_pred /= K.sum(y_pred, axis=-1, keepdims=True)
        
        # clip to prevent NaN's and Inf's
        y_pred = K.clip(y_pred, K.epsilon(), 1 - K.epsilon())

        loss = y_true * K.log(y_pred) * weights
        loss = -K.sum(loss, -1)
        return loss
    
    return loss

def weighted_mean_squared_error(y_true, y_pred):
    """
    MSE loss for heads and tail vector fields. All arrows that are not at 
    the head or tail are ignored in this loss
    """
    head_weights = K.expand_dims(y_true[:,:,:,4], axis=3) # expand dimension
    head_weights = K.repeat_elements(head_weights, 2, axis=3) # repeat factor

    tail_weights = K.expand_dims(y_true[:,:,:,5], axis=3) # expand dimension
    tail_weights = K.repeat_elements(tail_weights, 2, axis=3) # repeat factor

    weighted_head_error = y_pred[:,:,:,0:2]*head_weights - y_true[:,:,:,0:2]
    weigthed_tail_error = y_pred[:,:,:,2:4]*tail_weights - y_true[:,:,:,2:4]
    error = K.concatenate([weighted_head_error, weigthed_tail_error], axis=2)
    
    return K.mean(K.square(error), axis=-1)