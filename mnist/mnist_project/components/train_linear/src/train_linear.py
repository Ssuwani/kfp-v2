from kfp.v2.dsl import *

@component(
    packages_to_install=["tensorflow", "numpy"],
    output_component_file="train_linear.yaml"
)
def train_linear(
    dataset: Input[Dataset],
    output_model: Output[Model],
    metrics: Output[Metrics]
):
    import tensorflow as tf
    import numpy as np
    
    
    with open(dataset.path, "rb") as f:
        mnist = np.load(f)
        train_x, train_y = mnist["train_x"], mnist["train_y"]
        test_x, test_y = mnist["test_x"], mnist["test_y"]
    print(f"train x shape: {train_x.shape}")
    print(f"train y shape: {train_y.shape}")
    print(f"test x shape: {test_x.shape}")
    print(f"test y shape: {test_y.shape}")
    model = tf.keras.Sequential(
        [
            tf.keras.layers.Flatten(input_shape=(28, 28)),
            tf.keras.layers.Dense(128, activation='relu'),
            tf.keras.layers.Dense(10, activation='softmax')
        ]
    )
    model.compile(
        loss='sparse_categorical_crossentropy',
        optimizer='adam',
        metrics=['acc']
    )
    model.fit(train_x, train_y)
    loss, acc = model.evaluate(test_x, test_y)

    metrics.log_metric("accuracy",(acc * 100.0))
    metrics.log_metric("framework", "Tensorflow")
    metrics.log_metric("Model", "LinearModel")
    metrics.log_metric("dataset_size", len(train_x))
    
    model.save(output_model.path)
