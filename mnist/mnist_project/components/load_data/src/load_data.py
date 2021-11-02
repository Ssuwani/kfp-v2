from kfp.v2.dsl import *

@component(
    packages_to_install=["tensorflow", "numpy"],
    output_component_file="load_data.yaml"
)
def load_data(
    dataset: Output[Dataset]
):
    import tensorflow as tf
    import numpy as np
    
    mnist = tf.keras.datasets.mnist
    (train_x, train_y), (test_x, test_y) = mnist.load_data()
    train_x = train_x / 255.0
    test_x = test_x / 255.0
    
    with open(dataset.path, "wb") as f:
        np.savez(
            f,
            train_x=train_x,
            train_y=train_y,
            test_x=test_x,
            test_y=test_y
        )
    print(f"Saved on : {dataset.path}")
