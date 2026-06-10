import os
import json
import re
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, Input
from tensorflow.keras.optimizers import Adam
from typing import Dict, List, Any

# Path configurations
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODELS_DIR = os.path.join(BASE_DIR, "models")

# Ensure models directory exists
os.makedirs(MODELS_DIR, exist_ok=True)

def slugify(text: str) -> str:
    """
    Converts text to a clean snake_case slug suitable for filenames.
    """
    text = text.lower().strip()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[\s-]+', '_', text)
    return text

def train_and_save_model(
    series: List[float],
    city_name: str,
    var_name: str,
    lag: int = 3,
    epochs: int = 150,
    batch_size: int = 2,
    learning_rate: float = 0.01,
    dropout_rate: float = 0.1,
    hidden_neurons: List[int] = [16, 8]
) -> Dict[str, Any]:
    """
    Trains the ANN model and saves it to the models/ directory.
    Returns the training metadata.
    """
    from services.ann_service import prepare_sliding_window_data, MinMaxScaleHelper
    
    # 1. Prepare data
    X_raw, y_raw = prepare_sliding_window_data(series, lag)
    scaler_x = MinMaxScaleHelper()
    scaler_y = MinMaxScaleHelper()
    X_scaled = scaler_x.fit_transform(X_raw)
    y_scaled = scaler_y.fit_transform(y_raw)

    # 2. Build model
    model = Sequential()
    model.add(Input(shape=(lag,)))
    for neurons in hidden_neurons:
        model.add(Dense(neurons, activation="relu"))
        if dropout_rate > 0:
            model.add(Dropout(dropout_rate))
    model.add(Dense(1, activation="linear"))

    optimizer = Adam(learning_rate=learning_rate)

    # 3. Compiled training loop
    @tf.function
    def train_full_ann(X_data, y_data, epochs_val, batch_size_val):
        n_samples = tf.shape(X_data)[0]
        loss_history_tensor = tf.TensorArray(dtype=tf.float32, size=epochs_val)
        
        for epoch in tf.range(epochs_val):
            epoch_loss_sum = tf.constant(0.0)
            steps = tf.constant(0.0)
            
            for i in tf.range(0, n_samples, batch_size_val):
                x_batch = X_data[i:i+batch_size_val]
                y_batch = y_data[i:i+batch_size_val]
                
                with tf.GradientTape() as tape:
                    y_pred = model(x_batch, training=True)
                    loss = tf.reduce_mean(tf.square(y_batch - y_pred))
                grads = tape.gradient(loss, model.trainable_variables)
                optimizer.apply_gradients(zip(grads, model.trainable_variables))
                
                epoch_loss_sum += loss
                steps += 1.0
                
            loss_history_tensor = loss_history_tensor.write(epoch, epoch_loss_sum / steps)
            
        return loss_history_tensor.stack()

    # Convert to Tensors and execute training
    X_tensor = tf.convert_to_tensor(X_scaled, dtype=tf.float32)
    y_tensor = tf.convert_to_tensor(y_scaled, dtype=tf.float32)
    
    loss_history_vals = train_full_ann(X_tensor, y_tensor, epochs, batch_size)
    loss_history = [float(loss) for loss in loss_history_vals.numpy()]

    # Calculate train predictions
    scaled_train_pred = model(X_tensor, training=False)
    train_predictions = [scaler_y.inverse_transform(float(val[0])) for val in scaled_train_pred.numpy()]

    # Generate slugs
    city_slug = slugify(city_name)
    var_slug = slugify(var_name)
    
    model_path = os.path.join(MODELS_DIR, f"{city_slug}_{var_slug}.keras")
    meta_path = os.path.join(MODELS_DIR, f"{city_slug}_{var_slug}_meta.json")

    # 4. Save Keras Model
    model.save(model_path)

    # 5. Save Metadata and Scaler Parameters
    metadata = {
        "city": city_name,
        "variable": var_name,
        "loss_history": loss_history,
        "final_loss": float(loss_history[-1]),
        "train_predictions": train_predictions,
        "actual_values": [float(y) for y in y_raw],
        "scaler_x_min": float(scaler_x.min_val),
        "scaler_x_max": float(scaler_x.max_val),
        "scaler_y_min": float(scaler_y.min_val),
        "scaler_y_max": float(scaler_y.max_val),
        "parameters": {
            "lag": lag,
            "epochs": epochs,
            "batch_size": batch_size,
            "learning_rate": learning_rate,
            "dropout_rate": dropout_rate,
            "hidden_neurons": hidden_neurons
        }
    }
    
    with open(meta_path, "w") as f:
        json.dump(metadata, f, indent=2)

    print(f"[Trainer] Model and metadata successfully saved for {city_name} - {var_name}")
    return metadata
