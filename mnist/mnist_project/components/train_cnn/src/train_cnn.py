from kfp.v2.dsl import *

@component(
    packages_to_install=["tensorflow", "numpy"],
    output_component_file="train_cnn.yaml"
)
def train_cnn(
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
    train_x = train_x.reshape(-1, 28, 28, 1)
    test_x = test_x.reshape(-1, 28, 28, 1)
    model = tf.keras.Sequential(
        [
            tf.keras.layers.Conv2D(32, (3, 3), activation='relu', input_shape=(28, 28, 1)),
            tf.keras.layers.MaxPooling2D((2, 2)),
            tf.keras.layers.Conv2D(64, (3, 3), activation='relu'),
            tf.keras.layers.MaxPooling2D((2, 2)),
            tf.keras.layers.Conv2D(64, (3, 3), activation='relu'),
            tf.keras.layers.Flatten(),
            tf.keras.layers.Dense(64, activation='relu'),
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
    metrics.log_metric("Model", "CNNModel")
    metrics.log_metric("dataset_size", len(train_x))
    
    model.save(output_model.path)
