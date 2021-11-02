from kfp.v2.dsl import *

@component(
    packages_to_install=["tensorflow", "numpy"],
    output_component_file="evaluate_models.yaml"
)
def evaluate_models(
    dataset: Input[Dataset],
    model_linear: Input[Model],
    model_cnn: Input[Model],
    model_best: Output[Model]
):
    import tensorflow as tf
    import numpy as np
    from tensorflow.keras.models import clone_model
    
    with open(dataset.path, "rb") as f:
        mnist = np.load(f)
        train_x, train_y = mnist["train_x"], mnist["train_y"]
        test_x, test_y = mnist["test_x"], mnist["test_y"]
    
    # evaluate Linear Model
    linear_model = tf.keras.models.load_model(model_linear.path)
    linear_loss, linear_acc = linear_model.evaluate(test_x, test_y)
    
    # evaluate CNN Model
    test_x = test_x.reshape(-1, 28, 28, 1)
    cnn_model = tf.keras.models.load_model(model_cnn.path)
    cnn_loss, cnn_acc = cnn_model.evaluate(test_x, test_y)
    
    best_model = cnn_model if cnn_acc > linear_acc else linear_model
    best_model.save(model_best.path)
    
